from django.db import connection


def check_if_pg_connection():
    if (connection.settings_dict['ENGINE'] ==
            'django.db.backends.postgresql_psycopg2'):
        return True
    return False
