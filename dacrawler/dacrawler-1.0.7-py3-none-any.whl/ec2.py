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
import botocore
import paramiko

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
        
        outfile = open("{}.pem".format(self.key_name),'w')
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

        instanceIds = []
        cnt = 0
        for i in res:
            instanceIds.append(i.instance_id)
            res[cnt].wait_until_running()
            cnt += 1
        
        return instanceIds
    
    def start_all_instances(self):
        
        instanceIds = self.get_stopped_instance_infos('InstanceId')

        if len(instanceIds) == 0:
            #print("starting instances is null")
            return int(0)
        else:
            #print("running...")
            client = self.get_client()
            res = client.start_instances (InstanceIds = instanceIds) 
            
            waiter = client.get_waiter('instance_running')
            waiter.wait()
            
            return res
    
    def stop_instance(self, instance_id):
        
        #print("stopping...")
        client = self.get_client()
        res = client.stop_instances (InstanceIds = instance_id) 
        
        #print(res["StoppingInstances"][0]["CurrentState"]['Code'])
        #waiter = client.get_waiter('instance_stopped')
        #waiter.wait()
        
        if res["StoppingInstances"][0]["CurrentState"]['Code'] == 64:
            return 0
        else:
            return 1
    
    def stop_all_instances(self):
        
        instanceIds = self.get_runing_instance_infos('InstanceId')
        
        if len(instanceIds) == 0:
            return "running instances is 0"
        
        else:
            #print("stopping...")
            client = self.get_client()
            res = client.stop_instances (InstanceIds = instanceIds) 
            
            waiter = client.get_waiter('instance_stopped')
            waiter.wait()
            
            return res
        
    def terminate_instances(self):
        
        instanceIds = self.get_runing_instance_infos('InstanceId')
        
        if len(instanceIds) == 0:
            return "Target instances is 0"
        
        else:
            print("terminating...")
            client = self.get_client()
            res = client.terminate_instances (InstanceIds = instanceIds) 
            
            waiter = client.get_waiter('instance_terminated')
            waiter.wait()
            
            return res        
    
    def describe_instance(self):
        '''
         0 : pending
        16 : running
        32 : shutting-down
        48 : terminated
        64 : stopping
        80 : stopped
        '''
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
        )["Reservations"]
        
        infos = []
        for instances in res:
            for info in instances['Instances']:
                infos.append([info['InstanceId'],info['PublicIpAddress']])
            
        return infos
           
    def get_runing_instance_infos(self, params):

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
        )["Reservations"]
        
        infos = []
        for instances in res:
            for info in instances['Instances']:
                infos.append(info[params])
            
        return infos
        
    def get_stopped_instance_infos(self, params):
        client = self.get_client()
        res = client.describe_instances(
            Filters=[
                {
                    'Name': 'key-name',
                    'Values': [self.key_name]
                },
                {
                    'Name': 'instance-state-code',
                    'Values': ['80']
                }
            ]
        )["Reservations"]
        
        infos = []
        for instances in res:
            for info in instances['Instances']:
                infos.append(info[params])
            
        return infos
    
    def excute_cmd(self, p_key, host_name, user_name, cmd):
        key = paramiko.RSAKey.from_private_key_file(p_key)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host_name, username=user_name, pkey=key)
        
        stdin, stdout, stderr = client.exec_command(cmd)
        #print (stdout.read())
        
        client.close()
        #return stdout.read()
    
    def get_remote_job_status(self, p_key, host_name, user_name, localfilepath, remotefilepath):
        key = paramiko.RSAKey.from_private_key_file(p_key)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host_name, username=user_name, pkey=key)
        
        ftp_client=client.open_sftp()
        ftp_client.get(remotefilepath, localfilepath)
        ftp_client.close()
        
        job_status = open(localfilepath, 'r')
        status = job_status.readline()
        return int(status)
    
    def transfer_file(self, p_key, host_name, user_name, localfilepath, remotefilepath):
        key = paramiko.RSAKey.from_private_key_file(p_key)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host_name, username=user_name, pkey=key)
        
        ftp_client=client.open_sftp()
        ftp_client.put(localfilepath, remotefilepath)
        
        ftp_client.close()


        
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
    
