from sqlalchemy import inspect, testing, MetaData, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.testing import eq_
from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.testing.suite import *  # noqa

from sqlalchemy.testing.suite import ComponentReflectionTest as _ComponentReflectionTest


class ComponentReflectionTest(_ComponentReflectionTest):
    @testing.requires.foreign_key_constraint_option_reflection
    @testing.provide_metadata
    def test_get_foreign_key_options(self):
        meta = self.metadata

        Table(
            'x', meta,
            Column('id', Integer, primary_key=True),
            test_needs_fk=True
        )

        Table('table', meta,
              Column('id', Integer, primary_key=True),
              Column('x_id', Integer, ForeignKey('x.id', name='xid')),
              Column('test', String(10)),
              test_needs_fk=True)

        Table('user', meta,
              Column('id', Integer, primary_key=True),
              Column('name', String(50), nullable=False),
              Column('tid', Integer),
              ForeignKeyConstraint(
                  ['tid'], ['table.id'],
                  name='myfk',
                  ondelete="CASCADE"),
              test_needs_fk=True)

        meta.create_all()

        insp = inspect(meta.bind)

        # test 'options' is always present for a backend
        # that can reflect these, since alembic looks for this
        opts = insp.get_foreign_keys('table')[0]['options']

        eq_(
            dict(
                (k, opts[k])
                for k in opts if opts[k]
            ),
            {}
        )

        opts = insp.get_foreign_keys('user')[0]['options']
        eq_(
            dict(
                (k, opts[k])
                for k in opts if opts[k]
            ),
            {'ondelete': 'CASCADE'}
        )
