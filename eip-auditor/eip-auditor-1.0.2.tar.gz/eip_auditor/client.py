#!/usr/bin/env python
'''
Class that allows us to take all unused ip addresses for a region, and search
through all security groups for its reference.

Options:
    --region (optional, example: us-east-1, example: --all [searches all regions])
    --ip_addresses (string): one or multiple ip addresses, comma separated, no spaces
'''
import os
import argparse
import boto3
from eip_auditor.lib import base
from emojipedia import Emojipedia

class Client(object):
    """docstring for Client.
    @attributes:
    client: An instance of the ECR boto3 client.
    """

    def __init__(self, region=None, cidr=None):
        """Initializer

        Args:
            region (str): the aws region to check for unused IP Addreses
            cidr (str|list): a list of ip addresses to search for in security groups

        Returns:
            String

        """
        super(Client, self).__init__()
        self.regions = []
        self.default_region = 'us-east-1'
        self.__set_region__(region)
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID', None)
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', None)
        self.session = None
        self.client = None
        self.cidr = cidr

    def perform(self):
        """Main method to be called to run this application.

        Args:
            N/A

        Returns:
            N/A

        """
        print "Searching for usage in {}:\n".format(self.regions)

        for i in self.regions:
            self.session = boto3.Session(region_name=i)
            self.client = self.session.client('ec2')
            cidr_list = self.__set_cidr_list__(self.cidr, i)
            if len(cidr_list) < 1:
                print Emojipedia.search('smiling-face-with-smiling-eyes').character + "  No unused IP addresses found " + Emojipedia.search('smiling-face-with-smiling-eyes').character
            else:
                for cidr in cidr_list:
                    print "\t{}/32".format(cidr)
                print "\n"
                self.describe_security_groups(cidr_list)
            print "\n\n"

    def describe_unused_ip_addresses(self):
        """Find unused IP addresses from a dict and map the names to a list

        Args:
            N/A

        Returns:
            rtn (list): List of unused IP Addresses

        """
        rtn = []
        for k in self.client.describe_addresses()['Addresses']:
            if ('AssociationId' in k) or ('InstanceId' in k) or ('PrivateIpAddress' in k) or 'NetworkInterfaceId' in k:
                continue
            rtn.append(k['PublicIp'])
        return rtn

    def describe_security_groups(self, cidr_list):
        """Find unused IP addresses from a dict and map the names to a list

        Args:
            N/A

        Returns:
            rtn (list): List of unused IP Addresses

        """
        filters = []
        cidr_inbound_permission = {
            'Name': 'ip-permission.cidr',
            'Values': []
        }

        for k in cidr_list:
            cidr_inbound_permission['Values'].append(
                [
                    "{}/32".format(k)
                ]
            )

        cidr_inbound_permission['Values'] = base.flatten(cidr_inbound_permission['Values'])

        filters.append(cidr_inbound_permission)
        rtn = self.client.describe_security_groups(
            Filters=filters
        )

        found_mapping = {}
        if len(rtn['SecurityGroups']) > 0:
            print Emojipedia.search('loudly-crying-face').character + "  Found Unused IP Address(es) in the following SGs: " + Emojipedia.search('loudly-crying-face').character
            for k in rtn['SecurityGroups']:
                found_mapping[k['GroupId']] = []
                for j in k['IpPermissions']:
                    for l in j['IpRanges']:
                        if l['CidrIp'] in cidr_inbound_permission['Values']:
                            found_mapping[k['GroupId']].append(l['CidrIp'])
            for k in found_mapping:
                print k + ": "
                for j in found_mapping[k]:
                    print "\t" + j
                print "\n"
        else:
            print Emojipedia.search('smiling-face-with-smiling-eyes').character + "  Unused IP Addresses do not exist in any security group " + Emojipedia.search('smiling-face-with-smiling-eyes').character
        return found_mapping

    def __set_cidr_list__(self, cidr, region):
        """Determine which IP Addresses to look at, either determined by the user
           or by a region list

        Args:
            cidr (str/list): cidr list or string determined by the user
            region (str): the aws region to look in

        Returns:
            cidr_list (list): list of unused IP Addresses for a specific region

        """
        cidr_list = []
        if cidr is None:
            print "Found the following unused EIPs in {}".format(region)
            cidr_list = self.describe_unused_ip_addresses()
        elif isinstance(cidr, basestring):
            print "Setting CIDR list to argument value specified"
            split = self.cidr.split(",")
            cidr_list = split
        return cidr_list

    def __set_region__(self, region):
        """Determine which regions to look for unused IP Addresses in

        Args:
            region (str): the region passed by args

        Returns:
            N/A

        """
        if region is None:
            raise "Region not set."
        elif region == "all":
            self.regions = []
            for i in boto3.client('ec2', region_name=self.default_region).describe_regions()['Regions']:
                self.regions.append(i['RegionName'])
        else:
            self.regions = [region]
