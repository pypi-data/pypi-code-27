'''
Ssm Helper class to provide an interface to retrieve parameter data from AWS SSM
'''
import boto3
import base64, zlib
import simplejson

class SsmHelper(object):
    """docstring for SsmHelper.
    """

    def __init__(self, region):
        """Initializer

        Args:
            region (str)

        Returns:
            N/A

        """
        super(SsmHelper, self).__init__()
        self.region = region
        self.client = boto3.Session(region_name=self.region).client('ssm')

    def get_param(self, name):
        """Retrieve a parameter from SSM

        Args:
            region (str)

        Returns:
            Dict

        """
        try:
            rtn = self.client.get_parameter(Name=name, WithDecryption=True)

            if len(rtn['Parameter']) > 0:
                json_resp = zlib.decompress(base64.b64decode(
                    rtn['Parameter']['Value']), 16 + zlib.MAX_WBITS
                                           ).decode('utf-8')
                return simplejson.loads(json_resp)
        except Exception as e:
            print "Parameter {} not found.. skipping.".format(name)

        return {}

    def get_author(self, prefix, application, version):
        """Get the Author of a SSM parameter push

        Args:
            prefix (str): the prefix of the parameter
            application (str): the application name for the parameter
            version (str): the version of the parameter

        Returns:
            str

        """
        filters=[
            {
                'Key': 'Name',
                'Values': [
                    "{}.{}.{}".format(prefix, application.replace('-', '_'), version),
                ],
            }
        ]

        rtn = self.client.describe_parameters(Filters=filters)

        if len(rtn['Parameters']) == 0:
            while rtn.get('NextToken') and (rtn['NextToken'] is not None or rtn['NextToken'] != '') and (len(rtn.get('Parameters')) <= 0):
                rtn = self.client.describe_parameters(
                    Filters=filters,
                    NextToken=rtn['NextToken']
                )

        if len(rtn['Parameters']) > 0:
            return rtn['Parameters'][0]['LastModifiedUser']

        return ""
