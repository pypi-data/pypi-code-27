import boto3
import requests


client = boto3.client("route53")
METADATA_URL = "http://169.254.169.254/latest/meta-data/"
METADATA_IP_URL = METADATA_URL + "public-ipv4/"


def change_record(domain, subdomain, target_ip, action, ttl=900):
    """ Change the record for subdomain """
    zone_id = get_hosted_zone_id(domain)
    name = subdomain + "." + domain
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "%s subdomain %s from zone %s" % (action, subdomain, zone_id),
            "Changes": [
                {
                    "Action": action,
                    "ResourceRecordSet": {
                        "Name": name,
                        "Type": "A",
                        "ResourceRecords": [{"Value": target_ip}],
                        "TTL": ttl,
                    },
                }
            ],
        },
    )


def get_hosted_zone_id(domain):
    name = ".".join(reversed(domain.split(".")))
    result = client.list_hosted_zones_by_name(DNSName=name, MaxItems="1")
    return result["HostedZones"][0]["Id"]


def create_record(domain, subdomain):
    """ Create a new A record to this machine for subdomain
    :param string domain: name for domain, e.g. blastedstudios.com.
    :param string subdomain: subdomain name
    """
    change_record(domain, subdomain, get_ip(), "CREATE")


def delete_record(domain, subdomain):
    """ Delete the record for subdomain
    :param string domain: name for domain, e.g. blastedstudios.com.
    :param string subdomain: subdomain name
    """
    change_record(domain, subdomain, get_ip(), "DELETE")


def get_ip():
    """ Return this instance's ip"""
    return requests.get(METADATA_IP_URL).text
