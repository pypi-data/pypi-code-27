#-------------------------------------------------------------------------
# Copyright (c) DATA ARTIST
# All rights reserved.
#
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#--------------------------------------------------------------------------
'''
Created on 2018. 7. 25.

@author: kim
'''
import boto3
from io import StringIO, BytesIO
import pandas as pd
#from tornado.log import access_log
import gzip

class S3 ():
    
    def __init__(self, access_key, secret_key):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id = access_key, 
            aws_secret_access_key = secret_key
        )
        
    def list_bucket(self):
        res = self.s3.list_buckets()
        return res
    
    def df_to_s3(self, bucket, path, data_frame):
        csv_buffer = StringIO()
        data_frame.to_csv(csv_buffer, index=False)
        
        # compress string stream using gzip
        '''
        csv_buffer.seek(0)
        gz_buffer = BytesIO()
        
        with gzip.GzipFile(mode='w', fileobj=gz_buffer) as gz_file:
            gz_file.write(bytes(csv_buffer.getvalue(), 'utf-8'))
        
        ret = self.s3.Object(bucket, path).put(Body=gz_buffer.getvalue())
        '''
        # write stream to S3
        res = self.s3.Object(bucket, path).put(Body=csv_buffer.getvalue())
        
        return res
    
    def s3_to_df (self, bucket, key):
        
        bucket = self.s3.Bucket(bucket)
        obj = bucket.Object(key)
        get = obj.get()
        body = get['Body']
        #utf8 = body.decode('utf-8')
        
        #gz = gzip.GzipFile(fileobj=body['Body'])
        
        res = pd.read_csv(body, header=0, dtype=str)
        
        return res
    
if __name__=="__main__":
    s3 = S3(
                access_key = "###",
                secret_key = "####"
            )
    
    #ret = s3.list_bucket()
    ret = s3.df_to_s3("da.amazon.crawling", df)

    print(ret)
            
