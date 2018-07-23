"""This module holds the definition of Database connectivity"""

import json

from elasticsearch_dsl import DocType
from elasticsearch_dsl.connections import connections
from protean.context import context
from protean.entity import BaseEntity
from protean.usecase import ObjectNotFoundException

from protean_elasticsearch.config import CONFIG


class DB:
    """Class to initialize Database Connections"""

    def __init__(self):
        """Initialize Database Connection based on configuration"""

        try:
            self.connection = connections.create_connection(
                hosts=CONFIG.ELASTICSEARCH_HOSTS,
                http_auth=(CONFIG.ELASTICSEARCH_USER,
                           CONFIG.ELASTICSEARCH_SECRET))
        except Exception as exception:
            print("Exception: ", exception)
            raise NotImplementedError()


DATABASE = DB()


class BaseRepository(DocType):
    """This is the base class for all repository classes"""


class RepositoryWrapper:
    """Repository for UseCase/Service Layers"""

    def __init__(self, repo: DocType, cache_enabled=False):
        """Initialize with Repository to use"""

        self.repo = repo
        self.cache_enabled = cache_enabled
        self.indexname = None

    def _return_list(self, item):
        """This method either returns item if item is already a list,
        or converts item into a list
        """
        value = item
        if isinstance(item, str):
            # Convert value to a list if its not one already,
            #   so that we can use a `terms` search
            value = [item]
        return value

    def execute(self, search, exclude_tenant_id_filter=False):
        """Filter entities which are not is_archived and execute"""

        # Dont set the index here as it is been set.
        search = search.filter("term", is_archived=False)
        search = search.filter("term", is_active=True)

        if not exclude_tenant_id_filter:
            search = search.filter("term", tenant_id=context.tenant_id)

        print("Query:: (index={}) - {}".format(search._index[0], json.dumps(search.to_dict())))
        return search.execute()

    def from_entity(self, entity: BaseEntity):
        """Transform from Domain Model into Repository Entity"""

        return type(self.repo).from_entity(entity)

    def to_entity(self):
        """Transform from Repository Entity into Domain Entity"""

        return self.repo.to_entity()

    def find_by(self, atuple, exclude_tenant_id_filter=False):
        """Find by method to retrieve an object"""

        if isinstance(atuple[0], str):
            # The target attribute can either be a string or a list
            #   So we will use `terms` filter.
            value = self._return_list(atuple[1])
            must = [{"terms": {atuple[0]:value}}]
        else:
            must = []
            for item in atuple:
                value = self._return_list(item[1])
                must.append({"terms": {item[0]: value}})

        search = self.repo.search(index=self.indexname).update_from_dict({
            "query": {
                "bool": {
                    "must": must
                }
            }
        })

        response = self.execute(search, exclude_tenant_id_filter)

        if response.hits.total >= 1:
            # fixme - Raise exception if more than one record is found
            if response.hits.total > 1:
                print('find_by returned more than ONE record: {0}'.format(response.hits.hits))

            return self.repo.from_es(response.hits.hits[0]).to_entity()

        return None

    def query(self, exclude_tenant_id_filter=False, page=0, per_page=CONFIG.PER_PAGE,
              sort=None, sort_order='desc', **filters):
        """Query method for filtering entity objects"""

        if page > 0:
            start = (page - 1) * per_page
            end = page * per_page
        else:
            start = 0
            end = int(per_page)

        if filters:
            term_filters = []
            for item in filters:
                value = self._return_list(filters[item])
                term_filters.append({"terms": {item: value}})

            search = self.repo.search(index=self.indexname).update_from_dict({
                "query": {
                    "bool": {
                        "filter": term_filters
                    }
                }
            })[start:end]
        else:
            search = self.repo.search(index=self.indexname).query()[start:end]

        if sort:
            sort_key = sort
            if sort_order == 'desc':
                sort_key = '-' + sort_key
            search = search.sort(sort_key)

        response = self.execute(search, exclude_tenant_id_filter)

        results = {}
        data = []
        for hit in response.hits.hits:
            if self.cache_enabled:
                data.append(hit)
            else:
                data.append(self.repo.from_es(hit).to_entity())

        results['data'] = data
        results['total'] = response.hits.total
        results['page'] = page

        return results  # this will be cached.

    def search_query(self, page, query, per_page=CONFIG.PER_PAGE, **filters):
        """Method to pass search query"""

        start = (page - 1) * int(per_page)
        end = page * int(per_page)
        search = self.repo.search(index=self.indexname).update_from_dict(query)[start:end]

        if filters:
            search = search.filter("term", **filters)

        response = self.execute(search)
        results = {}
        data = []

        for hit in response.hits.hits:
            if self.cache_enabled:
                data.append(hit)
            else:
                matched_entity = self.repo.from_es(hit).to_entity()
                # fixme: Is there a better way to inject the custom query field into entity
                if "matched_queries" in hit:
                    matched_entity.__dict__['matched_queries'] = hit["matched_queries"]
                data.append(matched_entity)

        resp = response.to_dict()
        if 'aggregations' in resp:
            buckets = list(resp['aggregations']['count']['buckets'])
            results['aggs'] = buckets
        results['data'] = data
        results['total'] = response.hits.total
        results['page'] = page
        return results

    def aggregate(self, body):
        """Method to pass aggregate query to ES"""

        search = self.repo.search(index=self.indexname).update_from_dict(body)
        response = self.execute(search)
        aggregations = response.to_dict()
        buckets = list(aggregations['aggregations']['count']['buckets'])
        return buckets

    def get(self, identifier, exclude_tenant_id_filter=False):
        """READ method of CRUD"""
        search = self.repo.search(index=self.indexname).query("match", _id=identifier)
        response = self.execute(search, exclude_tenant_id_filter)
        if not response:
            return response

        hit = response.hits.hits[0]
        return self.repo.from_es(hit).to_entity()

    def create(self, entity: BaseEntity):
        """CREATE method of CRUD"""

        entity.is_archived = False

        # Honor the flag is_active if already set. Otherwise default to True
        if (not hasattr(entity, 'is_active') or
                (hasattr(entity, 'is_active') and entity.is_active is None)):
            entity.is_active = True

        # If the entity object does not have an attribute called tenant_id,
        #   or if it has, but the value is None,
        #   assign tenant_id
        if (not hasattr(entity, 'tenant_id') or
                (hasattr(entity, 'tenant_id') and not entity.tenant_id)):
            entity.tenant_id = context.tenant_id

        repo_object = type(self.repo).from_entity(entity)
        repo_object.save(refresh=True, index=self.indexname)
        return repo_object.to_entity()

    def update(self, identifier, data):
        """UPDATE method of CRUD"""

        repo_object = self.repo.get(identifier, index=self.indexname)
        try:
            data.pop('id')  # Remove ID if present in data
            data.pop('tenant_id')
        except KeyError:
            # Ignore if id is not present
            pass

        repo_object.update(refresh=True, **data)
        return repo_object.to_entity()

    def index(self, index, doc_type, data):  # pragma: no cover
        """ Index method """

        connections.get_connection().index(index=index, doc_type=doc_type,
                                           id=data["id"], body=data)

    def delete(self, identifier):
        """DELETE method of CRUD"""
        repo_object = self.repo.get(identifier, index=self.indexname)
        if repo_object.to_dict()['is_archived'] is True:
            raise ObjectNotFoundException("Object already Archived!")

        self.update(
            identifier, {'is_archived': True})
        return "Archived"

    def delete_by(self, atuple):
        """Delete by method to delete records by query"""

        if isinstance(atuple[0], str):
            must = [{"match": {atuple[0]:atuple[1]}}]
        else:
            must = [{"match": {x[0]:x[1]}} for x in atuple]

        search = self.repo.search(index=self.indexname).update_from_dict({
            "query": {
                "bool": {
                    "must": must
                }
            }
        })

        response = search.delete()
        return response['deleted']

    def delete_by_key(self, identifier, key, key_id):
        """Delete id inside object"""

        repo_object = self.repo.get(identifier, index=self.indexname)
        body = {
            "script": {
                "source": "ctx._source." + key + ".remove('" + key_id + "')"
            }
        }
        connections.get_connection().update(repo_object.meta['index'], repo_object.meta['doc_type'],
                                            repo_object.meta['id'], body)

    def get_by_source(self, identifier, source):  # pragma: no cover
        """ Get by source """
        return self.repo.get(identifier, _source=source, index=self.indexname).__dict__['_d_']

    def scroll(self, size=1000, scroll="5m"):  # pragma: no cover
        """ Get scroll generator """

        for hit in self.repo.search(index=self.indexname).params(scroll=scroll, size=size).scan():
            yield self.repo.from_dict(hit.__dict__)
