from pypika import JoinType, Order
from pypika import PostgreSQLQuery as Query
from pypika import Table
from pypika.functions import Count

from tortoise import fields
from tortoise.aggregation import Aggregate
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import FieldError
from tortoise.query_utils import Prefetch, Q
from tortoise.utils import AsyncIteratorWrapper


class AwaitableQuery:
    def __init__(self):
        self._joined_tables = []
        self.query = None
        self.model = None

    def _filter_from_related_table(self, table, param, value):
        if param['table'] not in self._joined_tables:
            self.query = self.query.join(
                param['table'], how=JoinType.left_outer
            ).on(table.id == getattr(param['table'], param['backward_key']))
        self.query = self.query.where(
            param['operator'](getattr(param['table'], param['field']), value)
        )

    def resolve_filters(self, model, filter_kwargs, q_objects, having, annotations, custom_filters):
        table = Table(model._meta.table)
        for node in q_objects:
            criterion, required_joins = node.resolve_for_model(model)
            for join in required_joins:
                if join[0] not in self._joined_tables:
                    self.query = self.query.join(join[0], how=JoinType.left_outer).on(join[1])
                    self._joined_tables.append(join[0])
            self.query = self.query.where(criterion)
        for key, value in filter_kwargs.items():
            param = model._meta.filters[key]
            if param.get('table'):
                self._filter_from_related_table(table, param, value)
            else:
                field_object = model._meta.fields_map[param['field']]
                value_encoder = (
                    param['value_encoder']
                    if param.get('value_encoder') else field_object.to_db_value
                )
                self.query = self.query.where(
                    param['operator'](getattr(table, param['field']), value_encoder(value))
                )
        for key, value in having.items():
            having_info = custom_filters[key]
            aggregation = annotations[having_info['field']]
            aggregation_info = aggregation.resolve_for_model(self.model)
            self.query = self.query.having(
                having_info['operator'](aggregation_info['field'], value)
            )

    def _join_table_by_field(self, table, related_field_name, related_field):
        if isinstance(related_field, fields.ManyToManyField):
            related_table = Table(related_field.type._meta.table)
            through_table = Table(related_field.through)
            if through_table not in self._joined_tables:
                self.query = self.query.join(
                    through_table, how=JoinType.left_outer
                ).on(table.id == getattr(through_table, related_field.backward_key))
                self._joined_tables.append(through_table)
            if related_table not in self._joined_tables:
                self.query = self.query.join(
                    related_table, how=JoinType.left_outer
                ).on(getattr(through_table, related_field.forward_key) == related_table.id)
                self._joined_tables.append(related_table)
        elif isinstance(related_field, fields.BackwardFKRelation):
            related_table = Table(related_field.type._meta.table)
            if related_table not in self._joined_tables:
                self.query = self.query.join(
                    related_table, how=JoinType.left_outer
                ).on(table.id == getattr(related_table, related_field.relation_field))
                self._joined_tables.append(related_table)
        else:
            related_table = Table(related_field.type._meta.table)
            if related_table not in self._joined_tables:
                related_id_field_name = '{}_id'.format(related_field_name)
                self.query = self.query.join(
                    related_table, how=JoinType.left_outer
                ).on(related_table.id == getattr(table, related_id_field_name))
                self._joined_tables.append(related_table)

    def resolve_ordering(self, model, orderings, annotations):
        table = Table(model._meta.table)
        for ordering in orderings:
            field_name = ordering[0]
            if field_name in model._meta.fetch_fields:
                raise ValueError(
                    "Filtering by relation is not possible filter by nested field of related model"
                )
            elif field_name.split('__')[0] in model._meta.fetch_fields:
                related_field_name = field_name.split('__')[0]
                related_field = model._meta.fields_map[related_field_name]
                self._join_table_by_field(table, related_field_name, related_field)
                self.resolve_ordering(
                    related_field.type, [('__'.join(field_name.split('__')[1:]), ordering[1])], {}
                )
            elif field_name in annotations:
                aggregation = annotations[field_name]
                aggregation_info = aggregation.resolve_for_model(self.model)
                self.query = self.query.orderby(aggregation_info['field'], order=ordering[1])
            else:
                if field_name not in model._meta.fields:
                    raise FieldError(
                        'Unknown field {} for model {}'.format(
                            field_name,
                            self.model.__name__,
                        )
                    )
                self.query = self.query.orderby(getattr(table, ordering[0]), order=ordering[1])

    def __await__(self):
        return self._execute().__await__()

    async def _execute(self):
        raise NotImplementedError()


class QuerySet(AwaitableQuery):
    def __init__(self, model):
        super().__init__()
        self.fields = model._meta.db_fields
        self.model = model
        self.query = Query.from_(model._meta.table)
        self._prefetch_map = {}
        self._prefetch_queries = {}
        self._single = False
        self._count = False
        self._db = None
        self._limit = None
        self._offset = None
        self._filter_kwargs = {}
        self._orderings = []
        self._joined_tables = []
        self._q_objects_for_resolve = []
        self._distinct = False
        self._annotations = {}
        self._having = {}
        self._available_custom_filters = {}

    def _clone(self):
        queryset = self.__class__(self.model)
        queryset._prefetch_map = self._prefetch_map
        queryset._prefetch_queries = self._prefetch_queries
        queryset._single = self._single
        queryset._count = self._count
        queryset._db = self._db
        queryset._limit = self._limit
        queryset._offset = self._offset
        queryset._filter_kwargs = dict(self._filter_kwargs)
        queryset._orderings = list(self._orderings)
        queryset._joined_tables = list(self._joined_tables)
        queryset._q_objects_for_resolve = list(self._q_objects_for_resolve)
        queryset._distinct = self._distinct
        queryset._annotations = self._annotations
        queryset._having = self._having
        queryset._available_custom_filters = self._available_custom_filters
        return queryset

    def filter(self, *args, **kwargs):
        queryset = self._clone()
        for arg in args:
            if not isinstance(arg, Q):
                raise TypeError('expected Q objects as args')
            queryset._q_objects_for_resolve.append(arg)
        for key, value in kwargs.items():
            if key in queryset.model._meta.filters:
                queryset._filter_kwargs[key] = value
            elif key in self.model._meta.fk_fields:
                field_object = self.model._meta.fields_map[key]
                queryset._filter_kwargs[field_object.source_field] = value.id
            elif key.split('__')[0] in self.model._meta.fetch_fields:
                queryset._q_objects_for_resolve.append(Q(**{key: value}))
            elif key in self._available_custom_filters:
                queryset._having[key] = value
            else:
                raise FieldError('unknown filter param {}'.format(key))
        return queryset

    def order_by(self, *orderings):
        queryset = self._clone()
        new_ordering = []
        for ordering in orderings:
            order_type = Order.asc
            if ordering[0] == '-':
                field_name = ordering[1:]
                order_type = Order.desc
            else:
                field_name = ordering

            if not (
                field_name.split('__')[0] in self.model._meta.fields
                or field_name in self._annotations
            ):
                raise FieldError(
                    'Unknown field {} for model {}'.format(
                        field_name,
                        self.model.__name__,
                    )
                )
            new_ordering.append((field_name, order_type))
        queryset._orderings = new_ordering
        return queryset

    def limit(self, limit):
        queryset = self._clone()
        queryset._limit = limit
        return queryset

    def offset(self, offset):
        queryset = self._clone()
        queryset._offset = offset
        return queryset

    def distinct(self):
        queryset = self._clone()
        queryset._distinct = True
        return queryset

    def annotate(self, **kwargs):
        queryset = self._clone()
        for key, aggregation in kwargs.items():
            if not isinstance(aggregation, Aggregate):
                raise TypeError('value is expected to be Aggregate instance')
            queryset._annotations[key] = aggregation
            from tortoise.models import get_filters_for_field
            queryset._available_custom_filters.update(get_filters_for_field(key, None, key))
        return queryset

    def values_list(self, *fields, flat=False):
        return ValuesListQuery(
            db=self._db,
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            q_objects=self._q_objects_for_resolve,
            flat=flat,
            fields_for_select_list=fields,
            distinct=self._distinct,
            limit=self._limit,
            offset=self._offset,
            orderings=self._orderings,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )

    def values(self, *args, **kwargs):
        fields_for_select = {}
        for field in args:
            if field in fields_for_select:
                raise FieldError('Duplicate key {}'.format(field))
            fields_for_select[field] = field

        for return_as, field in kwargs.items():
            if return_as in fields_for_select:
                raise FieldError('Duplicate key {}'.format(return_as))
            fields_for_select[return_as] = field

        return ValuesQuery(
            db=self._db,
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            q_objects=self._q_objects_for_resolve,
            fields_for_select=fields_for_select,
            distinct=self._distinct,
            limit=self._limit,
            offset=self._offset,
            orderings=self._orderings,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )

    def delete(self):
        return DeleteQuery(
            db=self._db,
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            q_objects=self._q_objects_for_resolve,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )

    def update(self, **kwargs):
        return UpdateQuery(
            db=self._db,
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            update_kwargs=kwargs,
            q_objects=self._q_objects_for_resolve,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )

    def count(self):
        return CountQuery(
            db=self._db,
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            q_objects=self._q_objects_for_resolve,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )

    def all(self):
        return self._clone()

    def first(self):
        queryset = self._clone()
        queryset._limit = 1
        queryset._single = True
        return queryset

    def _resolve_prefetch_object(self, queryset, prefetch):
        pass

    def prefetch_related(self, *args):
        queryset = self._clone()
        queryset._prefetch_map = {}

        for relation in args:
            if isinstance(relation, Prefetch):
                relation.resolve_for_queryset(queryset)
                continue
            relation_split = relation.split('__')
            first_level_field = relation_split[0]
            if first_level_field not in self.model._meta.fetch_fields:
                raise FieldError(
                    'relation {} for {} not found'.format(
                        first_level_field, self.model._meta.table
                    )
                )
            if first_level_field not in queryset._prefetch_map.keys():
                queryset._prefetch_map[first_level_field] = set()
            forwarded_prefetch = '__'.join(relation_split[1:])
            if forwarded_prefetch:
                queryset._prefetch_map[first_level_field].add(forwarded_prefetch)
        return queryset

    def using_db(self, _db: BaseDBAsyncClient):
        queryset = self._clone()
        queryset._db = _db
        return queryset

    def _resolve_annotate(self):
        if not self._annotations:
            return
        table = Table(self.model._meta.table)
        self.query = self.query.groupby(table.id)
        for key, aggregate in self._annotations.items():
            aggregation_info = aggregate.resolve_for_model(self.model)
            for join in aggregation_info['joins']:
                self._join_table_by_field(*join)
            self.query = self.query.select(aggregation_info['field'].as_(key))

    def _make_query(self):
        db = self._db if self._db else self.model._meta.db
        table = Table(self.model._meta.table)
        self.query = db.query_class.from_(table).select(*self.fields)
        self._resolve_annotate()
        self.resolve_filters(
            model=self.model,
            filter_kwargs=self._filter_kwargs,
            q_objects=self._q_objects_for_resolve,
            annotations=self._annotations,
            having=self._having,
            custom_filters=self._available_custom_filters,
        )
        if self._limit:
            self.query = self.query.limit(self._limit)
        if self._offset:
            self.query = self.query.offset(self._offset)
        if self._distinct:
            self.query = self.query.distinct()
        self.resolve_ordering(self.model, self._orderings, self._annotations)
        return self.query

    async def _execute(self):
        self.query = self._make_query()
        db = self._db if self._db else self.model._meta.db
        instance_list = await db.executor_class(
            model=self.model,
            db=db,
            prefetch_map=self._prefetch_map,
            prefetch_queries=self._prefetch_queries,
        ).execute_select(
            self.query, custom_fields=list(self._annotations.keys())
        )
        if not instance_list:
            if self._single:
                return None
            return []
        elif self._single:
            return instance_list[0]
        return instance_list

    async def __aiter__(self):
        result = await self
        return AsyncIteratorWrapper(result)


class UpdateQuery(AwaitableQuery):
    def __init__(
        self, model, filter_kwargs, update_kwargs, db, q_objects, annotations, having,
        custom_filters
    ):
        super().__init__()
        self._db = db if db else model._meta.db
        table = Table(model._meta.table)
        self.query = self._db.query_class.update(table)
        self.resolve_filters(
            model=model,
            filter_kwargs=filter_kwargs,
            q_objects=q_objects,
            annotations=annotations,
            having=having,
            custom_filters=custom_filters
        )

        for key, value in update_kwargs.items():
            field_object = model._meta.fields_map.get(key)
            if not field_object:
                raise FieldError('Unknown keyword argument {} for model {}'.format(key, model))
            assert not field_object.generated, 'Field {} is generated and can not be updated'
            if isinstance(field_object, fields.ForeignKeyField):
                db_field = '{}_id'.format(key)
                value = value.id
            else:
                db_field = model._meta.fields_db_projection[key]
            self.query = self.query.set(db_field, value)

    async def _execute(self):
        await self._db.execute_query(str(self.query))


class DeleteQuery(AwaitableQuery):
    def __init__(self, model, filter_kwargs, db, q_objects, annotations, having, custom_filters):
        super().__init__()
        self._db = db if db else model._meta.db
        table = Table(model._meta.table)
        self.query = self._db.query_class.from_(table)
        self.resolve_filters(
            model=model,
            filter_kwargs=filter_kwargs,
            q_objects=q_objects,
            annotations=annotations,
            having=having,
            custom_filters=custom_filters
        )
        self.query = self.query.delete()

    async def _execute(self):
        await self._db.execute_query(str(self.query))


class CountQuery(AwaitableQuery):
    def __init__(self, model, filter_kwargs, db, q_objects, annotations, having, custom_filters):
        super().__init__()
        self._db = db if db else model._meta.db
        table = Table(model._meta.table)
        self.query = self._db.query_class.from_(table)
        self.resolve_filters(
            model=model,
            filter_kwargs=filter_kwargs,
            q_objects=q_objects,
            annotations=annotations,
            having=having,
            custom_filters=custom_filters,
        )
        self.query = self.query.select(Count(table.star))

    async def _execute(self):
        result = await self._db.execute_query(str(self.query))
        return list(dict(result[0]).values())[0]


class FieldSelectQuery(AwaitableQuery):
    def _join_table_with_forwarded_fields(self, model, field, forwarded_fields):
        table = Table(model._meta.table)
        if field in model._meta.fields_db_projection and not forwarded_fields:
            db_field = model._meta.fields_db_projection[field]
            return table, db_field
        elif field in model._meta.fields_db_projection and forwarded_fields:
            raise FieldError(
                'Field "{}" for model "{}" is not relation'.format(
                    field,
                    model.__name__,
                )
            )

        if field in self.model._meta.fetch_fields and not forwarded_fields:
            raise ValueError(
                'Selecting relation "{}" is not possible, select concrete field on related model'
                .format(field)
            )

        field_object = model._meta.fields_map.get(field)
        if not field_object:
            raise FieldError('Unknown field "{}" for model "{}"'.format(
                field,
                model.__name__,
            ))

        self._join_table_by_field(table, field, field_object)
        forwarded_fields_split = forwarded_fields.split('__')
        return self._join_table_with_forwarded_fields(
            model=field_object.type,
            field=forwarded_fields_split[0],
            forwarded_fields='__'.join(forwarded_fields_split[1:]),
        )

    def add_field_to_select_query(self, field, return_as):
        table = Table(self.model._meta.table)
        if field in self.model._meta.fields_db_projection:
            db_field = self.model._meta.fields_db_projection[field]
            self.query = self.query.select(getattr(table, db_field).as_(return_as))
            return

        if field in self.model._meta.fetch_fields:
            raise ValueError(
                'Selecting relation "{}" is not possible, select concrete field on related model'
                .format(field)
            )

        field_split = field.split('__')
        if field_split[0] in self.model._meta.fetch_fields:
            related_table, related_db_field = self._join_table_with_forwarded_fields(
                model=self.model,
                field=field_split[0],
                forwarded_fields='__'.join(field_split[1:]),
            )
            self.query = self.query.select(getattr(related_table, related_db_field).as_(return_as))
            return

        raise FieldError('Unknown field "{}" for model "{}"'.format(
            field,
            self.model.__name__,
        ))


class ValuesListQuery(FieldSelectQuery):
    def __init__(
        self, model, filter_kwargs, db, q_objects, fields_for_select_list, limit, offset, distinct,
        orderings, flat, annotations, having, custom_filters
    ):
        super().__init__()
        if not (len(fields_for_select_list) == 1) == flat:
            raise TypeError('You can flat value_list only if contains one field')

        self.model = model
        table = Table(model._meta.table)
        self._db = db if db else model._meta.db
        self.query = self._db.query_class.from_(table)
        fields_for_select = {str(i): field for i, field in enumerate(fields_for_select_list)}

        for positional_number, field in fields_for_select.items():
            self.add_field_to_select_query(field, positional_number)

        self.resolve_filters(
            model=model,
            filter_kwargs=filter_kwargs,
            q_objects=q_objects,
            annotations=annotations,
            having=having,
            custom_filters=custom_filters,
        )
        if limit:
            self.query = self.query.limit(limit)
        if offset:
            self.query = self.query.offset(offset)
        if distinct:
            self.query = self.query.distinct()
        self.resolve_ordering(model, orderings, annotations)
        self.flat = flat
        self.fields = fields_for_select

    async def _execute(self):
        result = await self._db.execute_query(str(self.query))
        if self.flat:
            return [entry['0'] for entry in result]
        values_list = []
        column_numbers = sorted(list(self.fields.keys()))
        for entry in result:
            values = [entry[column] for column in column_numbers]
            values_list.append(values)
        return values_list


class ValuesQuery(FieldSelectQuery):
    def __init__(
        self, model, filter_kwargs, db, q_objects, fields_for_select, limit, offset, distinct,
        orderings, annotations, having, custom_filters
    ):
        super().__init__()
        self.model = model
        table = Table(model._meta.table)
        self._db = db if db else model._meta.db
        self.query = self._db.query_class.from_(table)
        for returns_as, field in fields_for_select.items():
            self.add_field_to_select_query(field, returns_as)

        self.resolve_filters(
            model=model,
            filter_kwargs=filter_kwargs,
            q_objects=q_objects,
            annotations=annotations,
            having=having,
            custom_filters=custom_filters,
        )
        if limit:
            self.query = self.query.limit(limit)
        if offset:
            self.query = self.query.offset(offset)
        if distinct:
            self.query = self.query.distinct()
        for ordering in orderings:
            self.query = self.query.orderby(ordering[0], order=ordering[1])
        self.resolve_ordering(model, orderings, annotations)
        self.fields_for_select = fields_for_select

    async def _execute(self):
        return await self._db.execute_query(str(self.query))
