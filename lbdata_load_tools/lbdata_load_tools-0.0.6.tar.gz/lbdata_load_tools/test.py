import unittest
import os
from uuid import uuid4
import csv

import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

from helpers import staging_table, create_dir, delete_files_in_dir
from presets import replace, upsert


load_dotenv()

S3_PROCESSING_BUCKET = 'lb-data-etl'
REDSHIFT_CLUSTER_SLICES = 2
REDSHIFT_SCHEMA_TEST = 'testalex'
REDSHIFT_DBNAME = os.environ["REDSHIFT_DBNAME"]
REDSHIFT_PORT = os.environ["REDSHIFT_PORT"]
REDSHIFT_USER = os.environ["REDSHIFT_USER"]
REDSHIFT_PASSWORD = os.environ["REDSHIFT_PASSWORD"]
REDSHIFT_HOST = os.environ["REDSHIFT_HOST"]

TEST_TABLE = 'testtable'


class TestMain(unittest.TestCase):
    def setUp(self):
        self.con = psycopg2.connect("dbname={} port={} user={} password={} host={}".format(REDSHIFT_DBNAME, REDSHIFT_PORT, REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_HOST))
        with self.con.cursor() as cur:
            cur.execute('create table if not exists %s ( foo int, bar varchar(255) );', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            self.con.commit()


    def tearDown(self):
        with self.con.cursor() as cur:
            cur.execute('drop table %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            self.con.commit()
        self.con.close()


    def test_staging_context_manager(self):
        """
        Test behaviour of custom context manager for staging tables
        """
        with self.con.cursor() as cur:
            query = 'select foo from {}'.format(AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)))
            table_stage_name = '{}_stage'.format(TEST_TABLE)
            with staging_table(cur, query, table_stage_name):
                cur.execute('select * from information_schema.columns where table_name = %s', (table_stage_name, ))
                res = cur.fetchall()
                self.assertEqual(len(res), 1)
                self.assertEqual(res[0][3], 'foo')

            # Outside the context manager, the temp table should be deleted
            cur.execute('select * from information_schema.tables where table_name = %s', (table_stage_name, ))
            res = cur.fetchall()
            self.assertEqual(len(res), 0)


    def test_preset_replace(self):
        """
        Test to replace content of the testtable with sample csv file
        """
        with self.con.cursor() as cur:
            # Add some garbage data into TEST_TABLE
            cur.execute('insert into %s (foo, bar) values (1, \'yo\');', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            cur.execute('insert into %s (foo, bar) values (2, \'ya\');', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            cur.execute('select count(*) from %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            self.con.commit()
            res = cur.fetchone()
        self.assertEqual(res[0], 2)

        # Create sample csv
        csv_path = '/tmp/{}'.format(uuid4())
        create_dir(csv_path)
        with open('{}/{}.csv'.format(csv_path, TEST_TABLE), 'w+', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([3, 'yi'])
            csv_writer.writerow([4, 'yu'])

        # Call replace preset
        replace(
            entity_name=TEST_TABLE,
            csv_path='{}/{}.csv'.format(csv_path, TEST_TABLE),
            cluster_size=2, 
            s3_bucket=S3_PROCESSING_BUCKET, 
            rs_schema=REDSHIFT_SCHEMA_TEST, 
            rs_dbname=REDSHIFT_DBNAME, 
            rs_user=REDSHIFT_USER, 
            rs_password=REDSHIFT_PASSWORD, 
            rs_host=REDSHIFT_HOST, 
            rs_port=REDSHIFT_PORT
        )

        with self.con.cursor() as cur:
            # Assert that new data is in the table
            cur.execute('select count(*) from %s where foo = 3', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            res = cur.fetchone()
            self.assertEqual(res[0], 1)

            # Assert that old data is removed
            cur.execute('select count(*) from %s where foo = 1', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            res = cur.fetchone()
            self.assertEqual(res[0], 0)

            # Clear table
            cur.execute('delete from %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))

        # Delete test ressources & clear table
        delete_files_in_dir(csv_path)


    def test_preset_upsert(self):
        """
        Test to upsert content of the testtable with sample csv file
        """
        with self.con.cursor() as cur:
            cur.execute('select count(*) from %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            res = cur.fetchone()
            self.assertEqual(res[0], 0)  # Assert database is empty at the beginning of the test

            # Add some garbage data into TEST_TABLE
            cur.execute('insert into %s (foo, bar) values (1, \'a\');', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            cur.execute('insert into %s (foo, bar) values (2, \'b\');', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            cur.execute('select count(*) from %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            self.con.commit()
            res = cur.fetchone()
        self.assertEqual(res[0], 2)

        # Create sample csv
        csv_path = '/tmp/{}'.format(uuid4())
        create_dir(csv_path)
        with open('{}/{}.csv'.format(csv_path, TEST_TABLE), 'w+', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([3, 'c'])
            csv_writer.writerow([4, 'd'])

        # Call upsert preset
        upsert(
            entity_name=TEST_TABLE,
            csv_path='{}/{}.csv'.format(csv_path, TEST_TABLE),
            primary_key='foo',
            cluster_size=2, 
            s3_bucket=S3_PROCESSING_BUCKET, 
            rs_schema=REDSHIFT_SCHEMA_TEST, 
            rs_dbname=REDSHIFT_DBNAME, 
            rs_user=REDSHIFT_USER, 
            rs_password=REDSHIFT_PASSWORD, 
            rs_host=REDSHIFT_HOST, 
            rs_port=REDSHIFT_PORT
        )

        with self.con.cursor() as cur:
            # Assert that new data is in the table
            cur.execute('select count(*) from %s where foo = 1', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            res = cur.fetchone()
            self.assertEqual(res[0], 1)

            # Assert that old data is removed
            cur.execute('select count(*) from %s where foo = 3', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))
            res = cur.fetchone()
            self.assertEqual(res[0], 1)

            # Clear table
            cur.execute('delete from %s;', (AsIs('{}.{}'.format(REDSHIFT_SCHEMA_TEST, TEST_TABLE)), ))

        # Delete test ressources & clear table
        delete_files_in_dir(csv_path)


if __name__ == '__main__':
    unittest.main()
