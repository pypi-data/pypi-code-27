import psycopg2

from .helpers import (
    copy_s3_to_redshift, prepare_file_for_load, delete_all_from_table, staging_table, delete_conflict_rows, insert_rows_from_table
)


def upsert(entity_name, csv_path, primary_key, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port=5439):
    """
    Perform an upsert on a Redshift table
    Requires the table to have a unique primary key
    """
    @prepare_file_for_load(entity_name, csv_path, cluster_size, s3_bucket)
    def _():
        with psycopg2.connect("dbname={} port={} user={} password={} host={}".format(rs_dbname, rs_port, rs_user, rs_password, rs_host)) as con:
            with con.cursor() as cur:
                table_name = '{}.{}'.format(rs_schema, entity_name)
                table_stage_name = '{}_stage'.format(entity_name)
                with staging_table(cur, table_name, table_stage_name):
                    src_bkt = '{}/{}'.format(s3_bucket, entity_name)
                    copy_s3_to_redshift(cur, table_stage_name, src_bkt, entity_name)
                    delete_conflict_rows(cur, table_stage_name, table_name, primary_key)
                    insert_rows_from_table(cur, table_stage_name, table_name)

        con.close()
    _()


def replace(entity_name, csv_path, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port=5439):
    """
    Replace the data in a redshift table by the content of the specified csv file
    """
    @prepare_file_for_load(entity_name, csv_path, cluster_size, s3_bucket)
    def _():
        with psycopg2.connect("dbname={} port={} user={} password={} host={}".format(rs_dbname, rs_port, rs_user, rs_password, rs_host)) as con:
            with con.cursor() as cur:
                table_name = '%s.%s' % (rs_schema, entity_name)
                delete_all_from_table(cur, table_name)
                src_bkt = '%s/%s' % (s3_bucket, entity_name)
                copy_s3_to_redshift(cur, table_name, src_bkt, entity_name)

        con.close()
    _()
