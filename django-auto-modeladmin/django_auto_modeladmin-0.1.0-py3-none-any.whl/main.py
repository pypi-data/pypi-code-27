from django.contrib import admin
from django.db.models.fields.reverse_related import ManyToOneRel
from .utils import filter_list, capitalize

IDENTIFIER_FIELD_NAMES = ["id", "uuid"]
DATE_FIELD_NAMES = ["created_on", "modified_on"]
READONLY_FIELD_NAMES =  IDENTIFIER_FIELD_NAMES + DATE_FIELD_NAMES + ["slug"]
LIST_DISPLAY_FIELD_NAMES = ["name", "title", "user"]

inlined_model_names = []

def create_model_admin_inline(model):
    name = '{}AdminInline'.format(capitalize(model.__name__))
    bases = (admin.TabularInline,)
    attrs = {"model": model}
    return type(name, bases, attrs)

def create_model_admin(model, config=None):
    """ Dynamically generate ModelAdmin classes for installed models.
        Display the form field based on the field name used.
        https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    """

    name = '{}ModelAdmin'.format(capitalize(model.__name__))
    bases = (admin.ModelAdmin,)

    field_names_found = []
    inlines_found = []

    # orgnanize the fields, field_names based on teh field type.
    for field in model._meta.get_fields():
        # Reverse relationships
        if field.auto_created and not field.concrete:
            # Only create inlines for reverse-relationship FK fields attached to this model instance. (reverse FK relationships only)
            if isinstance(field, ManyToOneRel):
                inlines_found.append(create_model_admin_inline(field.related_model))
        else:
            field_names_found.append(field.name)

    # get property fields that are provided
    property_field_names = config.get("property_fields", [])

    # fields to exclude_field_names from model admin
    exclude_field_names = config.get("exclude", [])

    # create a list of readonly fields to use that are on the model.
    readonly_field_names_found = filter_list(field_names_found, READONLY_FIELD_NAMES)
    readonly_field_names_found += config.get("readonly_fields", [])
    readonly_field_names_found += property_field_names
    readonly_field_names_found = list(set(readonly_field_names_found))

    # create our list of list display field names to use that are on the model.
    list_display_field_names_found = filter_list(field_names_found, LIST_DISPLAY_FIELD_NAMES)
    # if we got passed extra list display field names to use, add them.
    list_display_field_names_found += config.get("list_display", [])
    list_display_field_names_found = list(set(list_display_field_names_found))

    # if there arent any list_display fields to use, then default to the identifier field names
    if not len(list_display_field_names_found):
        list_display_field_names_found = filter_list(field_names_found, IDENTIFIER_FIELD_NAMES)

    fieldsets = []

    identifier_field_names = filter_list(field_names_found, IDENTIFIER_FIELD_NAMES)
    if len(identifier_field_names):
        fieldsets.append(("Identifiers", {
            "fields": identifier_field_names
        }))

    dates_field_names = filter_list(field_names_found, DATE_FIELD_NAMES)
    if len(dates_field_names):
        fieldsets.append(("Dates", {
            "fields": dates_field_names
        }))

    fieldsets.append(("Details", {
        "fields": [
            field_name for field_name in field_names_found + property_field_names
            if field_name not in \
                dates_field_names + identifier_field_names + exclude_field_names
        ]
    }))

    attrs = {
        "readonly_fields": readonly_field_names_found,
        "list_display": list_display_field_names_found,
        "fieldsets": tuple(fieldsets),
        "inlines": inlines_found,
        "exclude": exclude_field_names,
    }

    return type(name, bases, attrs)


def autoregister(list_of_models):
    for model in list_of_models:
        if isinstance(model, tuple):
            model_instance = model[0]
            extra_list_display_field_names_found = model[1]
            model_admin = create_model_admin(
                model_instance, extra_list_display_field_names_found)
            admin.site.register(model_instance, model_admin)
        else:
            model_admin = create_model_admin(model)
            admin.site.register(model, model_admin)
