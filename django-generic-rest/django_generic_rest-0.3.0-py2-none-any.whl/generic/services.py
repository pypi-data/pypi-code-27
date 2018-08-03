from django.contrib.auth.hashers import make_password
from rest_framework.utils import model_meta


def generic_retrieve_single_service(repository):
    """
    Returns an instance by user and pk
    """

    def _retrieve(pk, user):
        instance = repository.get_by_id(pk, user)
        return instance

    return _retrieve


def generic_retrieve_all_service(repository):
    """
    Returns all stored instances
    """

    def _retrieve(user=None):
        instances = repository.list_all()
        return instances

    return _retrieve


def generic_retrieve_all_by_owner_service(repository):
    """
    Returns all stored instances owned by user
    """

    def _retrieve(user):
        instances = repository.find_by_user(user)
        return instances

    return _retrieve


def generic_delete_service(repository):
    """
    Deletes an instance by pk
    """

    def _delete(pk, user):
        instance = repository.get_by_id(pk, user)
        repository.delete_by_id(pk, user)
        return instance

    return _delete


def generic_update_service(repository, validator):
    """
    Updates an existing instance
    """

    def _update(pk, user, **kwargs):
        # Get instance and meta info
        info = model_meta.get_field_info(repository.model_class)
        instance = repository.get_by_user_and_id(pk, user)

        # One-to-many relations
        for field_name, relation_info in info.relations.items():
            if (not relation_info.to_many
                    and field_name in kwargs.keys()
                    and kwargs[field_name] is not None):
                Model = relation_info.related_model
                related_instance = Model.objects.get(id=kwargs[field_name])
                setattr(instance, field_name, related_instance)

        # TODO: Many-to-many relations

        # Set regular fields and validate
        for field_name, field_info in info.fields.items():
            if field_name in kwargs.keys():
                setattr(instance, field_name, kwargs[field_name])

        validator(instance)

        # Set hashed password
        if hasattr(repository.model_class, 'password') and 'password' in kwargs:
            instance.password = make_password(kwargs['password'])

        # Save and return
        repository.persist(instance)
        return instance

    return _update


def generic_create_service(repository, validator, factory):
    """
    Returns and persists a new instance
    """

    def _create(user, **kwargs):
        # Get user and meta info
        info = model_meta.get_field_info(repository.model_class)
        if hasattr(repository.model_class, 'owner'):
            kwargs['owner'] = user.id

        # One-to-many relations
        for field_name, relation_info in info.relations.items():
            if (not relation_info.to_many
                    and field_name in kwargs.keys()
                    and kwargs[field_name] is not None):
                Model = relation_info.related_model
                related_instance = Model.objects.get(id=kwargs[field_name])
                kwargs[field_name] = related_instance

        # TODO: Many-to-many relations

        # Create instance and validate
        instance = factory(repository.model_class, **kwargs)
        validator(instance)

        # Set hashed password
        if hasattr(repository.model_class, 'password') and 'password' in kwargs:
            instance.password = make_password(kwargs['password'])

        # Save and return
        repository.persist(instance)
        return instance

    return _create
