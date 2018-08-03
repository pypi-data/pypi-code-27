from django.db.models import Max, Count


def pks_from_iterable(iterable, unique_output=False):
    """
    Return pks list based on iterable
    :param iterable: list of django model objects OR django queryset
    :param unique_output: if True returned list will be unique
    :return: list of int
    """
    pks = list()
    for obj in iterable:
        try:
            pks.append(int(getattr(obj, 'pk', obj)))
        except (TypeError, ValueError):
            raise TypeError("Iterable %s is not any of Queryset, list with django Model objects or ints" % iterable)
    return list(set(pks)) if unique_output else pks


def remove_duplicates_from_model(model_class, unique_fields):
    """
    Remove duplicates objects based on unique_fields in model_class
    :param model_class: Django model class
    :param unique_fields: list of strings
    """
    duplicates = (model_class.objects.values(*unique_fields).order_by().annotate(
        max_id=Max('id'), count_id=Count('id')).filter(count_id__gt=1))

    for duplicate in duplicates:
        (model_class.objects.filter(
            **{x: duplicate[x] for x in unique_fields}).exclude(
            id=duplicate['max_id']).delete())
