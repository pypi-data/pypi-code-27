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
import logging

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
        
    def run_instances(self):
    
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.run_instances.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.run_instances.error", 
            log_file    = "./logs/error.log"
        )
        
        resource = self.get_resource()
        
        try:
            exe_logger.debug("run instances are start")
            res = resource.create_instances(
                ImageId=self.image_id, 
                MinCount=1, 
                MaxCount=self.max_cnt,
                KeyName=self.key_name,
                InstanceType=self.instance_type
            )
        except ClientError as e:
            err_logger.error("Error: %s", e, exc_info=True)
            if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                raise
        else:
            instanceIds = []
            cnt = 0
            for i in res:
                instanceIds.append(i.instance_id)
                res[cnt].wait_until_running()
                cnt += 1
            exe_logger.debug("run instances are completed")
            exe_logger.debug("in preparation of starting instances...")
            return instanceIds
    
    def start_all_instances(self):
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.start_all_instances.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.start_all_instances.error", 
            log_file    = "./logs/error.log"
        )
        
        instanceIds = self.get_stopped_instance_infos('InstanceId')
        
        if len(instanceIds) == 0:
            return int(0)
        else:
            client = self.get_client()
            
            try:
                exe_logger.debug("start_all_instances are start[{}]".format(len(instanceIds)))
                res = client.start_instances (InstanceIds = instanceIds)
            except ClientError as e:
                err_logger.error("Error: %s", e, exc_info=True)
                if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                    raise
                 
            else:
                exe_logger.debug("in preparation of starting instances...")
                #waiter = client.get_waiter('instance_running')
                #waiter.wait()
                exe_logger.debug("start_all_instances are completed[{}]".format(len(instanceIds)))
                return res
    
    def stop_instance(self, instance_id):
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.stop_instance.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s> %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.stop_instance.error", 
            log_file    = "./logs/error.log"
        )
        try:
            #print("stopping...")
            exe_logger.debug("stopping instance : [{}]".format(len(instance_id)))
            client = self.get_client()
            res = client.stop_instances (InstanceIds = instance_id) 
            
            #print(res["StoppingInstances"][0]["CurrentState"]['Code'])
            #waiter = client.get_waiter('instance_stopped')
            #waiter.wait()
            
            if res["StoppingInstances"][0]["CurrentState"]['Code'] == 64:
                return 0
            else:
                exe_logger.debug("[{}] stopping error : retrying".format(len(instance_id)))
                return 1
            
        except ClientError as e:
            err_logger.error("Error: %s", e, exc_info=True)
            return 1
        
    def stop_all_instances(self):
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.stop_all_instances.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s> %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.stop_all_instances.error", 
            log_file    = "./logs/error.log"
        )
        
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
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.terminate_instances.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s> %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.terminate_instances.error", 
            log_file    = "./logs/error.log"
        )
        
        try:
            instanceIds = self.get_runing_instance_infos('InstanceId')
            
            if len(instanceIds) == 0:
                exe_logger.debug("target instance is 0")
            
            else:
                exe_logger.debug("{} instances are terminating".format(len(instanceIds)))
                
                client = self.get_client()
                res = client.terminate_instances (InstanceIds = instanceIds) 
                
                #waiter = client.get_waiter('terminating instances')
                #waiter.wait()
                
                return res        
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
        else:
            exe_logger.debug("{} instances are completed".format(len(instanceIds)))
                    
    def describe_instance(self):
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.describe_instance.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s> %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.describe_instance.error", 
            log_file    = "./logs/error.log"
        )
        
        '''
         0 : pending
        16 : running
        32 : shutting-down
        48 : terminated
        64 : stopping
        80 : stopped
        '''
        try:
            exe_logger.debug("describe instances are start")
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
        except ClientError as e:
            err_logger.error("Error: %s", e, exc_info=True)
            if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                raise
        else:
            infos = []
            for instances in res:
                for info in instances['Instances']:
                    infos.append([info['InstanceId'],info['PublicIpAddress']])
            
            exe_logger.debug("describe instances is completed[{}]".format(len(infos)))    
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
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.get_stopped_instance_infos.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.get_stopped_instance_infos.error", 
            log_file    = "./logs/error.log"
        )
        try:
            exe_logger.debug("check stopped instances...")
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
        except Client as e:
            err_logger.error("Error: %s", e, exc_info=True)
            if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                raise
        
        else:
            infos = []
            for instances in res:
                for info in instances['Instances']:
                    infos.append(info[params])
            exe_logger.debug("stopped instances are {}".format(len(infos)))    
            return infos
    
    def excute_cmd(self, p_key, host_name, user_name, cmd):
        
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.excute_cmd.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.excute_cmd.error", 
            log_file    = "./logs/error.log"
        )
        
        try:
            exe_logger.debug("execute [{}] is start...".format(cmd))
            key = paramiko.RSAKey.from_private_key_file(p_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name, username=user_name, pkey=key)
            
            (stdin, stdout, stderr) = client.exec_command(cmd, timeout=120)
            
        except socket.timeout as e:
            client.close()
            err_logger.error("Error: Time out %s", e, exc_info=True)
        else:
            exe_logger.debug("[{}] is completed".format(cmd))
            client.close()
    
    def get_remote_job_status(self, p_key, host_name, user_name, localfilepath, remotefilepath):
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.get_remote_job_status.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.get_remote_job_status.error", 
            log_file    = "./logs/error.log"
        )
        
        try:
            exe_logger.debug("get remote instance status")
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
            err_logger.error("Error: %s", e, exc_info=True)
        else:
            exe_logger.debug("remote instance status : {}(OK)".format(status))
            return int(status)
    
    def transfer_file(self, p_key, host_name, user_name, localfilepath, remotefilepath):
        # execution logger
        exe_logger = self.get_logging_cnf(
            logger_name = "ec2.transfer_file.execution", 
            log_file    = "./logs/execution.log", 
            format      = "%(asctime)s - %(name)s > %(message)s"
        )

        # error logger
        err_logger = self.get_logging_cnf(
            logger_name = "ec2.transfer_file.error", 
            log_file    = "./logs/error.log"
        )
        
        try:
            exe_logger.debug("send executing file to {}".format(host_name))
            key = paramiko.RSAKey.from_private_key_file(p_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name, username=user_name, pkey=key, timeout=120)
            
            ftp_client=client.open_sftp()
            ftp_client.put(localfilepath, remotefilepath)
            ftp_client.close()
        except Exception as e:
            err_logger.error("Error: %s", e, exc_info=True)
        else:
            exe_logger.debug("executing file is translated to {}".format(host_name))
        
    def get_logging_cnf(self, logger_name, log_file, format=None):
        
        logger = logging.getLogger(logger_name)
        
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(format)
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        
        exe_streamHandler = logging.StreamHandler()
        if format != None:
            exe_streamHandler.setFormatter(formatter)
        logger.addHandler(exe_streamHandler)
        
        return logger
        
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
    
