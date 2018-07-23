from time import time
import pytest


@pytest.mark.usefixtures('versioning_manager', 'table_creator')
class TestBenchmark:
    def test_multiple_inserts(self, user_class, session):
        first = time()
        for _ in xrange(1000):
            user = user_class(name='John')
            session.add(user)
            session.commit()
        print(time() - first)

    def test_heavy_statement(self, session, activity_cls):
        first = time()
        session.execute('INSERT INTO "user" SELECT generate_series(1, 10000)')
        session.commit()
        print(session.query(activity_cls).count())
        session.execute("""UPDATE "user" SET name = 'aaa'""")
        print(time() - first)
