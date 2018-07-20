#!/usr/bin/env python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from copy import deepcopy

import boto3
from moto import mock_ec2

from ekscli.bootstrap import Kubelet
from ekscli.stack import ControlPlane, NodeGroup


def test_kubelet_svc(tmpdir):
    svc = tmpdir.join('kubelet.service')
    opts = deepcopy(Kubelet.KUBELET_OPTS)
    opts['authentication-token-webhook'] = ''
    kube_exec = '/usr/bin/kubelet'
    Kubelet._create_kube_service(svc.strpath, kube_exec, opts)
    parser = ConfigParser()
    parser.read(svc.strpath)
    assert parser.get('Service', 'ExecStart') is not None
    assert kube_exec in parser.get('Service', 'ExecStart')
    assert 'register-node=true' in parser.get('Service', 'ExecStart')


@mock_ec2
def test_get_cluster_name():
    region = 'us-east-1'
    boto3.setup_default_session(region_name=region)
    ec2 = boto3.session.Session().resource('ec2')
    instances = ec2.create_instances(ImageId=NodeGroup.DEFAULT_AMI.get(region), InstanceType='t2.nano', KeyName='test',
                                     MinCount=1, MaxCount=1,
                                     TagSpecifications=[{
                                         'ResourceType': 'instance',
                                         'Tags': [
                                             {'Key': 'kubernetes.io/cluster/test', 'Value': 'owned'}
                                         ]
                                     }])

    cname = Kubelet._get_cluster_name(region, instances[0].id)
    assert cname == 'test'


