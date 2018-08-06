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
from logging import FileHandler
'''
Created on 2018. 7. 25.

@author: kim
'''

import boto3
import botocore
import paramiko
import logging
import logging.handlers
import time

class EC2 ():
    exe_logger = logging.getLogger(__name__)
    err_logger = logging.getLogger("error")
    start_time = time.time()
    '''
    EC2
    '''
    def __init__ (self, access_key, secret_key, region, image_id, instance_type, key_name, max_cnt):
        
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.image_id = image_id
        self.instance_type = instance_type
        self.key_name = key_name
        self.max_cnt = max_cnt
        
    def test (self) :
        return 'hello EC2"'
    
    def get_resource(self):
        resource = boto3.resource(
            'ec2', 
            region_name=self.region, 
            aws_access_key_id=self.access_key, 
            aws_secret_access_key=self.secret_key
        )
        return resource
    
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
    
    def start_all_instances(self):
        
        EC2.exe_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s > %(message)s")
        
        #if log_file > 10M then file rotation
        file_max_bytes = 10 * 1024 * 1024  
        fileHandler = logging.handlers.RotatingFileHandler(
            "./logs/{}/execution.log".format(self.region), 
            maxBytes = file_max_bytes, 
            backupCount = 10
        )
        fileHandler.setFormatter(formatter)
        EC2.exe_logger.addHandler(fileHandler)
        exe_streamHandler = logging.StreamHandler()
        exe_streamHandler.setFormatter(formatter)
        EC2.exe_logger.addHandler(exe_streamHandler)
        EC2.exe_logger.propagate = False
        
        # error logger
        EC2.err_logger.setLevel(logging.DEBUG)
        #if log_file > 10M then file rotation
        file_max_bytes = 10 * 1024 * 1024  
        fileHandler = logging.handlers.RotatingFileHandler(
            "./logs/{}/error.log".format(self.region), 
            maxBytes = file_max_bytes, 
            backupCount = 10
        )
        EC2.err_logger.addHandler(fileHandler)
        err_streamHandler = logging.StreamHandler()
        EC2.err_logger.addHandler(err_streamHandler)
        EC2.err_logger.propagate = False
        
        
        instanceIds = self.get_stopped_instance_infos('InstanceId')
        
        if len(instanceIds) == 0:
            return int(0)
        else:
            client = self.get_client()
            
            try:
                EC2.exe_logger.debug("start_all_instances are start[{}]".format(len(instanceIds)))
                res = client.start_instances (InstanceIds = instanceIds)
            except Exception as e:
                EC2.err_logger.error("Error: %s", e, exc_info=True)
                 
            else:
                EC2.exe_logger.debug("in preparation of crawling...")
                #waiter = client.get_waiter('instance_running')
                #waiter.wait()
                EC2.exe_logger.debug("start_all_instances are completed[{}]".format(len(instanceIds)))
                return res
        
    def run_instances(self):
        
        resource = self.get_resource()
        
        try:
            EC2.exe_logger.debug("run instances are start")
            res = resource.create_instances(
                ImageId=self.image_id, 
                MinCount=1, 
                MaxCount=self.max_cnt,
                KeyName=self.key_name,
                InstanceType=self.instance_type
            )
        except Exception as e:
            EC2.err_logger.error("Error: %s", e, exc_info=True)
        else:
            instanceIds = []
            cnt = 0
            for i in res:
                instanceIds.append(i.instance_id)
                res[cnt].wait_until_running()
                cnt += 1
            EC2.exe_logger.debug("run instances are completed")
            EC2.exe_logger.debug("in preparation of starting instances...")
            return instanceIds
    
    
    
    def stop_instance(self, instance_id):
        
        try:
            #print("stopping...")
            EC2.exe_logger.debug("stopping instance : [{}]".format(len(instance_id)))
            client = self.get_client()
            res = client.stop_instances (InstanceIds = instance_id) 
            
            #print(res["StoppingInstances"][0]["CurrentState"]['Code'])
            #waiter = client.get_waiter('instance_stopped')
            #waiter.wait()
            
            if res["StoppingInstances"][0]["CurrentState"]['Code'] == 64:
                return 0
            else:
                EC2.exe_logger.debug("[{}] stopping error : retrying".format(len(instance_id)))
                return 1
            
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
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
        try:
            instanceIds = self.get_runing_instance_infos('InstanceId')
            
            if len(instanceIds) == 0:
                EC2.exe_logger.debug("target instance is 0")
            
            else:
                EC2.exe_logger.debug("{} instances are terminating".format(len(instanceIds)))
                
                client = self.get_client()
                res = client.terminate_instances (InstanceIds = instanceIds) 
                
                #waiter = client.get_waiter('terminating instances')
                #waiter.wait()
                
                return res        
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
        else:
            EC2.exe_logger.debug("{} instances are completed".format(len(instanceIds)))
                    
    def describe_instance(self, instance_id=None):
                
        '''
         0 : pending
        16 : running
        32 : shutting-down
        48 : terminated
        64 : stopping
        80 : stopped
        '''
        try:
            EC2.exe_logger.debug("describe instances are start")
            client = self.get_client()
            if instance_id == None:
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
            else:
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
                    ],
                    InstanceIds = instance_id,
                )["Reservations"]
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
            #if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            #    raise
        else:
            infos = []
            for instances in res:
                for info in instances['Instances']:
                    infos.append([info['InstanceId'],info['PublicIpAddress']])
            
            EC2.exe_logger.debug("describe instances is completed[{}]".format(len(infos)))
            return infos
           
    def get_runing_instance_infos(self, params):
        
        try:
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
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
            
    def get_stopped_instance_infos(self, params):

        try:
            EC2.exe_logger.debug("check stopped instances...")
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
            
        except Exception as e:
            EC2.err_logger.error("Error: %s", e, exc_info=True)
        
        else:
            infos = []
            for instances in res:
                for info in instances['Instances']:
                    infos.append(info[params])
            EC2.exe_logger.debug("stopped instances are {}".format(len(infos)))
            return infos
    
    def excute_cmd(self, p_key, host_name, user_name, cmd):

        try:
            EC2.exe_logger.debug("execute [{}] is start...".format(cmd))
            key = paramiko.RSAKey.from_private_key_file(p_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name, username=user_name, pkey=key)
            
            (stdin, stdout, stderr) = client.exec_command(cmd, timeout=120)
            
        except Exception as e:
            client.close()
            EC2.err_logger.error("Error: Time out %s", e, exc_info=True)
        else:
            EC2.exe_logger.debug("[{}] is completed".format(cmd))
            client.close()
            
    
    def get_remote_instande_status(self, p_key, host_name, user_name, localfilepath, remotefilepath):

        try:
            EC2.exe_logger.debug("get remote instance status")
            key = paramiko.RSAKey.from_private_key_file(p_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name, username=user_name, pkey=key, timeout=120)
            
            ftp_client=client.open_sftp()
            ftp_client.get(remotefilepath, localfilepath)
            ftp_client.close()
            
            job_status = open(localfilepath, 'r')
            status = job_status.readline()
            
        except Exception as e:
            EC2.err_logger.error("Error: %s", e, exc_info=True)
            
        else:
            EC2.exe_logger.debug("remote instance status : {}".format(status))
            return int(status)
    
    def transfer_file(self, p_key, host_name, user_name, localfilepath, remotefilepath):
        
        try:
            EC2.exe_logger.debug("send executing file to {}".format(host_name))
            key = paramiko.RSAKey.from_private_key_file(p_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name, username=user_name, pkey=key, timeout=120)
            
            ftp_client=client.open_sftp()
            ftp_client.put(localfilepath, remotefilepath)
            ftp_client.close()
        except Exception as e:
            EC2.err_logger.error("Error: %s", e, exc_info=True)
        else:
            EC2.exe_logger.debug("executing file is translated to {}".format(host_name))
        
    def get_logging_cnf(self, log_file, format=None):
        
        #logger = logging.getLogger(logger_name)
        
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(format)
        
        #if log_file > 10M then file rotation
        file_max_bytes = 10 * 1024 * 1024  
        fileHandler = logging.handlers.RotatingFileHandler(log_file, maxBytes = file_max_bytes, backupCount = 10)
        #fileHandler = logging.FileHandler(log_file)
        
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        
        exe_streamHandler = logging.StreamHandler()
        if format != None:
            exe_streamHandler.setFormatter(formatter)
        logger.addHandler(exe_streamHandler)
        
        logger.propagate = False
        return logger
    
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
    
