from django.db.models import Lookup

from .util import check_if_pg_connection


class LookupMixin(Lookup):

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s %s %s' % (lhs, self.operator, rhs), params


class DataContains(LookupMixin):
    lookup_name = 'contains'
    operator = '@>' if check_if_pg_connection() else 'LIKE'


class ContainedBy(LookupMixin):
    lookup_name = 'contained_by'
    operator = '<@' if check_if_pg_connection() else 'LIKE'


class Overlap(LookupMixin):
    lookup_name = 'overlap'
    operator = '&&' if check_if_pg_connection() else 'LIKE'
