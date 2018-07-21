#!/usr/bin/env python
import os
import sys
from hashlib import md5
from boto import connect_s3

CONNECTIONS = {}

def connection():
    if 's3' not in CONNECTIONS:
        CONNECTIONS['s3'] = connect_s3()
    return CONNECTIONS['s3']

def list_filename_paths(dir):
    files = os.listdir(dir)
    for f in files:
        yield f, os.path.join(dir, f)

def cmd_upload(dir=None, prefix=None, bucket=None, zlib=False):
    if not all([dir, prefix, bucket]):
        raise RuntimeError('directory, prefix and bucket are mandatory')
    conn = connection()
    s3bucket = conn.get_bucket(bucket)
    num_uploaded = 0
    for filename, path in list_filename_paths(dir):
        keystr = os.path.join(prefix, filename)
        with open(path) as f:
            data = f.read()
        if zlib:
            keystr += '.z'
            data = data.encode('zlib')
        md5hash = md5(data).hexdigest()
        key = s3bucket.get_key(keystr)
        if key and md5hash == key.etag[1:-1]:
            print('Already uploaded {}, continuing'.format(keystr))
            continue
        if not key:
            key = s3bucket.new_key(keystr)
        key.set_contents_from_string(data)
        num_uploaded += 1
        print('Uploaded {} => {}::{}'.format(filename, bucket, keystr))
    print('Finished uploading {} files.'.format(num_uploaded))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')
    sub = subparsers.add_parser('upload', help='upload files to S3')
    sub.add_argument('--dir', '-d', help='directory to upload')
    sub.add_argument('--bucket', '-b', help='bucket to upload to')
    sub.add_argument('--prefix', '-p', help='prefix to upload to')
    sub.add_argument('--zlib', '-z', action='store_true',
        help='compress with zlib and add .z extension')
    sub = subparsers.add_parser('download', help='download from S3')
    args = parser.parse_args()

    if args.cmd == 'upload':
        cmd_upload(dir=args.dir, prefix=args.prefix, bucket=args.bucket,
            zlib=args.zlib)
    elif args.cmd == 'download':
        raise NotImplementedError('WIP')

if __name__ == '__main__':
    main()
