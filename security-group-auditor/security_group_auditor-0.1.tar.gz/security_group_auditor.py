import boto3
import pandas as pd

from exceptions import RegionNotSpecified, PathNotSpecified

# parser = argparse.ArgumentParser(description="Argument Parser for SG Auditor")
# parser.add_argument("-region", help="List of comma seperated AWS supported regions")
# parser.add_argument("-id", help="List of comma seperated security group ids")
# parser.add_argument("-vpc", help="Finds security groups in a particulat VPC")
# parser.add_argument("-user_id", help="AWS Account ID")
# parser.add_argument("-protocol", help="TCP | UDP | ICMP")
# parser.add_argument("-cidr", help="CIDR of the group")
#
# args = parser.parse_args()

def _filter_builder(vpc_ids=None, protocol=None, cidr=None, user_id=None, sg_ids=None):
    """

    :param vpc_ids: list of VPC ID's that you want to search in
    :param protocol: String specifying TCP | UDP | ICMP
    :param cidr: list of CIDR's that you want to search
    :param user_id: list of AWS account ID's
    :param sg_ids: list of security group ID's

    :return: list of dictionaries specifying the filter's applied
    """
    response_filter = []
    if vpc_ids is not None:
        response_filter.append({
            "Name"  : "vpc-id",
            "Values": vpc_ids
        })

    if protocol is not None:
        response_filter.append({
            "Name"  : "ip-permission.protocol",
            "Values": [protocol]
        })

    if cidr is not None:
        response_filter.append({
            "Name"  : "ip-permission.cidr",
            "Values": cidr
        })

    if user_id is not None:
        response_filter.append({
            "Name"  : "owner-id",
            "Values": user_id
        })

    if sg_ids is not None:
        response_filter.append({
            "Name": "group-id",
            "Values": sg_ids
        })

    return response_filter


def security_group_auditor(regions=None, vpc_ids=None, protocol=None, cidr=None, user_id=None, sg_ids=None,
                           audit_file_path=None):
    """
    :param regions: ALL | [list of regions]
    :param vpc_ids: list of vpc_ids
    :param protocol: String specifying TCP | UDP | ICMP
    :param cidr: list of CIDR's that you want to search
    :param user_id: list of AWS account ID's
    :param sg_ids: list of security group ID's
    :param audit_file_path: Path to .csv file where you want to store data. Ex: /home/user/data.csv

    :return: None
    """
    REGIONS = ['us-east-2',
               'us-east-1',
               'us-west-1',
               'us-west-2',
               'ap-northeast-1',
               'ap-northeast-2',
               'ap-northeast-3',
               'ap-south-1',
               'ap-southeast-1',
               'ap-southeast-2',
               'ca-central-1',
               'cn-north-1',
               'cn-northwest-1',
               'eu-central-1',
               'eu-west-1',
               'eu-west-2',
               'eu-west-3',
               'sa-east-1'
               ]
    data_frame = pd.DataFrame()
    if regions is None:
        raise RegionNotSpecified("No region specified")

    elif regions == "ALL" or type(regions) == list:

        if regions != "ALL":
            REGIONS = regions

        for region in REGIONS:
            sg_client = boto3.client("ec2", region_name = region)
            try:
                if vpc_ids is None and protocol is None and cidr is None and user_id is None and sg_ids is None:
                    security_groups = sg_client.describe_security_groups()

                else:
                    filter_list = _filter_builder(vpc_ids, protocol, cidr, user_id, sg_ids)
                    security_groups = sg_client.describe_security_groups(
                        Filters=filter_list
                    )

                for security_group in security_groups["SecurityGroups"]:
                    vpc_id              = security_group["VpcId"]
                    security_group_name = security_group["GroupName"]
                    security_group_id   = security_group["GroupId"]

                    for rules in security_group["IpPermissions"]:
                        try:
                            if rules.get("ToPort") is not None:
                                to_port = rules["ToPort"]
                            else:
                                to_port = -1

                            for ip in rules["IpRanges"]:
                                _cidr        = ip["CidrIp"]
                                if ip.get("Description") is not None:
                                    description = ip["Description"]
                                else:
                                    description = "Default"

                                data_frame = data_frame.append({"Description" : description,
                                                                "VPC_ID"      : vpc_id,
                                                                "Name"        : security_group_name,
                                                                "Group ID"    : security_group_id,
                                                                "Port"        : to_port,
                                                                "CIDR"        : _cidr,
                                                                "Region"      : region}, ignore_index=True)

                        except:
                            continue
            except Exception as e:
                print(e)
                continue

    if audit_file_path is None:
        raise PathNotSpecified("Path to save the csv file not specified")
    else:
        data_frame.to_csv(audit_file_path)
