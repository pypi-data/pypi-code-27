import boto3

class EC2 ():
    '''
    EC2
    '''
    def __init__ (self, region, key_name, access_key, secret_key, image_id, instance_type, max_cnt):
        self.region = region
        self.key_name = key_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.image_id = image_id
        self.instance_type = instance_type
        self.max_cnt = max_cnt
        
    def test (self) :
        return 'hello EC2"'
    
    def get_resource(self):
        client = boto3.resource(
            'ec2', 
            region_name=self.region, 
            aws_access_key_id=self.access_key, 
            aws_secret_access_key=self.secret_key
        )
        return client
    
    def get_client(self):
        client = boto3.client(
            'ec2', 
            region_name=self.region, 
            aws_access_key_id=self.access_key, 
            aws_secret_access_key=self.secret_key
        )
        return client
        
    def create_keypair(self):
        #print(self)
        
        resource = self.get_resource()
        
        outfile = open(self.key_name,'w')
        key_pair = resource.create_key_pair(KeyName=self.key_name)
        KeyPairOut = str(key_pair.key_material)
        outfile.write(KeyPairOut)
        
    def run_instances(self):
    
        #print(self)
        resource = self.get_resource()
        res = resource.create_instances(
            ImageId=self.image_id, 
            MinCount=1, 
            MaxCount=self.max_cnt,
            KeyName=self.key_name,
            InstanceType=self.instance_type
        )
        #res[0].wait_until_running()
        #res[0].instance_id
        instanceIds = []
        cnt = 0
        for i in res:
            instanceIds.append(i.instance_id)
            res[cnt].wait_until_running()
            cnt += 1
        
        '''
        for i in instanceIds:
            i.wait_until_running()     
        '''   
        return instanceIds
        
    def describe_instance(self):
        client = self.get_client()
        res = client.describe_instances(
            Filters=[
                {
                    'Name': 'key-name',
                    'Values': [self.key_name]
                },
                {
                    'Name': 'instance-state-code',
                    'Values': ['16']
                }
            ]
        )["Reservations"][0]["Instances"]
        
        
        instanceIds = []
        for i in res:
            instanceIds.append(i['InstanceId'])
            
        #instanceIds = client.describe_instances()
        return instanceIds
        #return instanceIds["Reservations"].Instances['InstanceId']
        
    def terminate_instances(self):
        client = self.get_client()
        instanceIds = self.describe_instance()
        ret = client.terminate_instances (InstanceIds = instanceIds) 
        return ret
        
    def describe_instances_status(self):
        
        #instance_ids = self.describe_instance()
        client = self.get_client()
        ret = client.describe_instance_status(
            Filters=[
                {
                    'Name': 'key-name',
                    'Values': [self.key_name]
                },
            ],
            
        )["InstanceStatuses"]
        
        '''
        instance_cnt = 0
        for InstanceState in ret:
            for code in InstanceState:
                if code==16:
                    instance_cnt += 1
                
        
        
        {
            'InstanceStatuses': [
                {
                    'AvailabilityZone': 'ap-northeast-2c', 
                    'InstanceId': 'i-01fa2e4ff395e1556', 
                    'InstanceState': {'Code': 16, 'Name': 'running'}, 
                    'InstanceStatus': {
                        'Details': [{'Name': 'reachability', 'Status': 'passed'}], 'Status': 'ok'
                    }, 
                    'SystemStatus': {
                        'Details': [{'Name': 'reachability', 'Status': 'passed'}], 'Status': 'ok'
                    }
                },   
                {
                    'AvailabilityZone': 'ap-northeast-2c', 
                    'InstanceId': 'i-0ae3e34a2e34751cf', 
                    'InstanceState': {'Code': 16, 'Name': 'running'}, 
                    'InstanceStatus': {
                        'Details': [{'Name': 'reachability', 'Status': 'passed'}], 'Status': 'ok'
                    }, 
                    'SystemStatus': {
                        'Details': [{'Name': 'reachability', 'Status': 'passed'}], 'Status': 'ok'
                    }
                }
            ], 
            'ResponseMetadata': {'RequestId': '22a9ed30-69ea-4d8f-b241-71eeabc841cf', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'date': 'Tue, 24 Jul 2018 08:59:32 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}
        }

        
        waiter = client.get_waiter('instance_running')
        ret = waiter.wait(
            InstanceIds=instance_ids,
            WaiterConfig={
                'Delay': 10,
        '        MaxAttempts': 10
            }
        )
        '''
        return ret
    
if  __name__=="__main__":
    ec2 = EC2(
        region        = "ap-northeast-2",
        key_name      = "udpap2.pem",
        access_key    = "AKIAIPTSPE7MOZ3FXFFA",
        secret_key    = "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",
        image_id      = "ami-afd86dc1", 
        instance_type = "t2.micro",
        max_cnt       = 2
    )
    ret = ec2.test()
    print(ret)
    