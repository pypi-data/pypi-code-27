import psycopg2

from .helpers import (
    copy_s3_to_redshift, delete_all_from_table, staging_table, delete_conflict_rows, upload_files_to_s3, insert_rows_from_query
)


def upsert(cur, entity_name, csv_path, primary_key, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port):
    """
    Perform an upsert on a Redshift table
    Requires the table to have a unique primary key
    """
    with upload_files_to_s3(csv_path, cluster_size, entity_name, s3_bucket):
        table_src = '{}.{}'.format(rs_schema, entity_name)
        table_stg = '{}_stage'.format(entity_name)
        with staging_table(cur, table_src, table_stg):
            copy_s3_to_redshift(cur, dest_table=table_stg, src_bkt='{}/{}'.format(s3_bucket, entity_name), obj_prefix=entity_name)
            delete_conflict_rows(cur, src_table=table_stg, dest_table=table_src, primary_key=primary_key)
            insert_rows_from_query(cur, dest_table=table_src, query='select * from {}'.format(table_stg))


def replace(cur, entity_name, csv_path, cluster_size, s3_bucket, rs_schema, rs_dbname, rs_user, rs_password, rs_host, rs_port):
    """
    Replace the data in a redshift table with the content of the specified csv file
    """
    with upload_files_to_s3(csv_path, cluster_size, entity_name, s3_bucket):
        table_name='{}.{}'.format(rs_schema, entity_name)
        delete_all_from_table(cur, table_name)
        copy_s3_to_redshift(cur, dest_table=table_name, src_bkt='{}/{}'.format(s3_bucket, entity_name), obj_prefix=entity_name)
