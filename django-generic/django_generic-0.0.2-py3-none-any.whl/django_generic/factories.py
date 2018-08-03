class ConcreteModelFactoryMixin(object):
    """
    FactoryMixin for creation concrete models with OneToOne relation to abstract model.
    You can also user kwargs lookups with '__'
    Using example:
    ```
        @classmethod
        def _create(cls, model_class, *args, **kwargs):
            switch_field = 'some_field_from_abstract_model'
            switch_field = 'some_field__from_other_model_connected_to_abstract'
            relation_field = 'name_of_OneToOne_relation_field'
            factories_map = {
                'some_value_from_switch_field: SomeFactory,
                'other_value_from_switch_field: OtherFactory,
            }
            abstract = cls.create_with_concrete(
                factories_map=factories_map, switch_field=switch_field,
                relation_field=relation_field, model_class=model_class,
                *args, **kwargs
            )
            return abstract
    ```
    """

    @classmethod
    def create_with_concrete(cls, factories_map, switch_field, relation_field, model_class, *args, **kwargs):
        abstract_fields = [field.name for field in cls._meta.model._meta.fields]
        abstract_kwargs = {key: val for key, val in kwargs.items() if key.split('__')[0] in abstract_fields}
        abstract = super(ConcreteModelFactoryMixin, cls)._create(model_class, *args, **abstract_kwargs)
        # Split switch_field if switcher value is in other model.
        switcher = abstract
        for last_field in switch_field.split('__'):
            switcher = getattr(switcher, last_field)

        concrete_factory = factories_map[switcher]
        concrete_fields = [field.name for field in concrete_factory._meta.model._meta.fields]
        concrete_kwargs = {key: val for key, val in kwargs.items() if key.split('__')[0] in concrete_fields}
        concrete_kwargs[relation_field] = abstract
        concrete_factory(**concrete_kwargs)
        return abstract
