import os


AWS_REGION_NAME = os.environ['AWS_REGION_NAME'] if 'AWS_REGION_NAME' in os.environ else 'ap-southeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
