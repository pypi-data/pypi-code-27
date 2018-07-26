'''
Created on 2018. 7. 25.

@author: kim
'''
import boto3
from io import StringIO, BytesIO
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
        ret = self.s3.list_buckets()
        return ret
    
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
        ret = self.s3.Object(bucket, path).put(Body=csv_buffer.getvalue())
        
        return ret
    
    
if __name__=="__main__":
    s3 = S3(
                access_key = "AKIAIPTSPE7MOZ3FXFFA",
                secret_key = "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"
            )
    
    #ret = s3.list_bucket()
    ret = s3.df_to_s3("da.amazon.crawling", df)

    print(ret)
            