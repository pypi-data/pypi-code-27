import psycopg2

from helpers import (
    copy_s3_to_redshift, delete_all_from_table, staging_table, delete_conflict_rows, upload_files_to_s3, insert_rows_from_query
)


def upsert(entity_name, csv_path, primary_key, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port):
    """
    Perform an upsert on a Redshift table
    Requires the table to have a unique primary key
    """
    with psycopg2.connect("dbname={} port={} user={} password={} host={}".format(rs_dbname, rs_port, rs_user, rs_password, rs_host)) as con:
        with con.cursor() as cur:
            with upload_files_to_s3(csv_path, cluster_size, entity_name, s3_bucket):
                table_name = '{}.{}'.format(rs_schema, entity_name)
                table_stage_name = '{}_stage'.format(entity_name)
                with staging_table(cur, query='select * from {}'.format(table_name), table_stage_name=table_stage_name):
                    copy_s3_to_redshift(cur, dest_table=table_stage_name, src_bkt='{}/{}'.format(s3_bucket, entity_name), obj_prefix=entity_name)
                    delete_conflict_rows(cur, src_table=table_stage_name, dest_table=table_name, primary_key=primary_key)
                    insert_rows_from_query(cur, dest_table=table_name, query='select * from {}'.format(table_stage_name))
    con.close()


def replace(entity_name, csv_path, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port):
    """
    Replace the data in a redshift table with the content of the specified csv file
    """
    with psycopg2.connect("dbname={} port={} user={} password={} host={}".format(rs_dbname, rs_port, rs_user, rs_password, rs_host)) as con:
        with con.cursor() as cur:
            with upload_files_to_s3(csv_path, cluster_size, entity_name, s3_bucket):
                table_name='{}.{}'.format(rs_schema, entity_name)
                delete_all_from_table(cur, table_name)
                copy_s3_to_redshift(cur, dest_table=table_name, src_bkt='{}/{}'.format(s3_bucket, entity_name), obj_prefix=entity_name)
    con.close()
