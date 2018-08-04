import boto3
import requests


client = boto3.client("route53")
METADATA_URL = "http://169.254.169.254/latest/meta-data/"
METADATA_IP_URL = METADATA_URL + "public-ipv4/"


def change_record(zone_id, name, target_ip, action):
    """ Change the record for subdomain "name"
    :param string zone_id: id for domain, e.g. blastedstudios.com.
    :param string name: subdomain name
    """
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "%s subdomain %s from zone %s" % (action, name, zone_id),
            "Changes": [
                {
                    "Action": action,
                    "ResourceRecordSet": {
                        "Name": name,
                        "Type": "A",
                        "ResourceRecords": [{"Value": target_ip}],
                    },
                }
            ],
        },
    )


def create_record(zone_id, name):
    """ Create a new A record to this machine for subdomain "name"
    :param string zone_id: id for domain, e.g. blastedstudios.com.
    :param string name: subdomain name
    """
    change_record(zone_id, name, get_ip(), "CREATE")


def delete_record(zone_id, name):
    """ Delete the record for subdomain "name"
    :param string zone_id: id for domain, e.g. blastedstudios.com.
    :param string name: subdomain name
    """
    change_record(zone_id, name, get_ip(), "DELETE")


def get_ip():
    """ Return this instance's ip"""
    return requests.get(METADATA_IP_URL).text
