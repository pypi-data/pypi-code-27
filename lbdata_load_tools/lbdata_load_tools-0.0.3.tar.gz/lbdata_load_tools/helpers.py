import os
import math
import gzip
import csv
from contextlib import contextmanager
from uuid import uuid4

import boto3
from psycopg2.extensions import AsIs

from .config import (
    AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)


def create_dir(dir):
    """
    Create all directories for the specified path
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def upload_to_s3(src_dir, out_bkt, prefix=''):
    """
    Upload all files from the src directory into the specified out bucket
    """
    s3 = boto3.resource('s3', region_name=AWS_REGION_NAME)
    for file_name in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file_name)
        s3.meta.client.upload_file(file_path, out_bkt, prefix + file_name)


def delete_files_in_dir(dir):
    """
    Delete all the files in the specified directory
    """
    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)
        os.remove(file_path)


def empty_s3_bucket(bucket, prefix=''):
    """
    Delete all the files in the specific s3 bucket starting with the specified prefix
    """
    os.system("aws s3 rm s3://%s/%s --recursive --quiet" % (bucket, prefix))


def create_staging_table(cur, table_src_name, table_stage_name):
    """
    Create staging table exactly similar to the specified table_name
    """
    cur.execute("""
    create temp table %(table_stage_name)s
    (like %(table_src_name)s);
    """, {'table_stage_name': AsIs(table_stage_name), 'table_src_name': AsIs(table_src_name)})


def copy_s3_to_redshift(cur, dest_table, src_bkt, obj_prefix):
    """
    Data must be in csv format with ',' delimiter
    Data must be gzip compressed
    Data can be split for parallel uploading
    """
    cur.execute("""
    copy %(dest_table)s
    from 's3://%(src_bkt)s/%(obj_prefix)s.gz'
    credentials 'aws_access_key_id=%(aws_access_key_id)s;aws_secret_access_key=%(aws_secret_access_key)s'
    trimblanks
    truncatecolumns
    csv
    delimiter ','
    gzip;
    """, {'dest_table': AsIs(dest_table), 'src_bkt': AsIs(src_bkt), 'obj_prefix': AsIs(obj_prefix), 'aws_access_key_id': AsIs(AWS_ACCESS_KEY_ID), 'aws_secret_access_key': AsIs(AWS_SECRET_ACCESS_KEY)})


def delete_conflict_rows(cur, src_table, dest_table, primary_key):
    """
    Delete rows from dest_table that are present in src_table
    """
    cur.execute("""
    delete from %(dest_table)s
    using %(src_table)s
    where %(dest_table)s.%(primary_key)s = %(src_table)s.%(primary_key)s;
    """, {'dest_table': AsIs(dest_table), 'src_table': AsIs(src_table), 'primary_key': AsIs(primary_key)})


def insert_rows_from_table(cur, src_table, dest_table):
    """
    Insert all rows from src_table into dest_table
    """
    cur.execute("""
    insert into %(dest_table)s
    select * from %(src_table)s;
    """, {'dest_table': AsIs(dest_table), 'src_table': AsIs(src_table)})


def insert_rows_from_query(cur, dest_table, query):
    """
    Insert result of select query into dest_table
    """
    cur.execute("""
    insert into %(dest_table)s
    %(query)s;
    """, {'dest_table': AsIs(dest_table), 'query': AsIs(query)})


def drop_table(cur, table_name):
    cur.execute('drop table %s;', (AsIs(table_name), ))


def create_shredded_files(file_path, out_dir, nb_parts, prefix):
    """
    Prepare files for optimal Redshift upload
    Split csv input file into {nb_parts} compressed csv files
    """
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        # Determine how many lines to write in each shredded file
        file_length = sum(1 for line in f)
        interval_size = math.ceil(file_length / nb_parts)
        f.seek(0)  # Return to beginning of generator

        # Initiate csv reader
        csvreader = csv.reader(f, delimiter=',')

        # Write rows in shredded files
        for n in range(nb_parts):
            shrd_path = '%s/%s.gz.%s' % (out_dir, prefix, n + 1)
            with gzip.open(shrd_path, 'wt+', encoding='utf-8') as shrd_file:
                csv_writer = csv.writer(shrd_file, delimiter=',')
                for _ in range(interval_size):
                    try:
                        csv_writer.writerow(next(csvreader))
                    except StopIteration:
                        break


def prepare_file_for_load(entity_name, csv_path, cluster_size, s3_bucket):
    """
    Prepare and upload data from the specified CSV file into the S3_PROCESSING_BUCKET/entity_name/ bucket
    Run load_func
    Automatically delete files and clear bucket
    """
    def _inner(load_func):
        def _wrapper(*args, **kwargs):
            try:
                shredded_dir = '/tmp/{}'.format(uuid4())
                create_dir(shredded_dir)
                create_shredded_files(csv_path, shredded_dir, cluster_size, entity_name)

                s3_prefix = '%s/' % entity_name
                upload_to_s3(shredded_dir, s3_bucket, s3_prefix)

                load_func(*args, **kwargs)

            finally:
                delete_files_in_dir(shredded_dir)
                empty_s3_bucket('%s/%s' % (s3_bucket, entity_name))

        return _wrapper
    return _inner


def delete_all_from_table(cur, table_name):
    cur.execute('delete from %s;', (AsIs(table_name), ))


@contextmanager
def staging_table(cur, table_src_name, table_stage_name):
    """
    Provides a context manager for using staging tables and be sure that it will correctly be dropped
    """
    create_staging_table(cur, table_src_name, table_stage_name)
    try:
        yield
    finally:
        drop_table(cur, table_stage_name)
