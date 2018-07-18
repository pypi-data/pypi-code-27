import os
import boto3
import sys

class LambdaUtils:
    """
    Class for set of lambda utilities.  This library requires python>=3.6
    The utilities are:
    get_secrets:  Gets the requested secrets from AWS Parameter Store

    See documentation in function for usage and output examples.

    NOTE: You must set the ENV environmental variable to the environment your code runs in
    """
    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except:
            print('An environmental variable called ENV must be set to the proper environment before proceeding')
            sys.exit(1)
   
    def build_list(self, keys):
        envkeys = [f'/env/{self.env}/{key}' for key in keys]
        return envkeys

    def get_secrets(self, keys):
        """
        Usage example:
        
        from patientpop_python_utils import lambda_utils as lu
        a = lu.LambdaUtils()
        secrets, err = a.get_secrets(['Test1', 'Test2', 'dbuser', 'dbpass'])
        if err:
            print(f'The following keys were not found in the store: {err})
            sys.exit(1)
	mysql_connector.connect(user=secrets['dbuser'], password=secrets['dbpass'], ...)

        keys = a list of strings ['foo1', 'foo2', 'etc']
        for multi-level keys (i.e /cron/brain/cron1/name), specify it as
        ['cron/brain/cron1/name'] (notice the missing / at the beginning)

        Returns a tuple with the first value being a dictionary
        containing the returned key/value pairs from Parameter Store.
        It returns a blank dictionary if no valid keys returned.
        The second being a list with any invalid keys specified.

        Example with all invalid keys
        ({}, ['/env/qa/Test1', '/env/qa/Test2'])
        Example with matched keys and no invalid keys
        ({'dbpass': 'tickertape'}, [])
        Example with both matched and invalid keys
        ({'dbpass': 'tickertape'}, ['/env/qa/Test1', '/env/qa/Test2'])
        """
        secrets = {}
        invalid_keys = []
        client = boto3.client('ssm', region_name='us-east-1')
        response = client.get_parameters(
            Names=self.build_list(keys),
            WithDecryption=True
        )

        for entry in response['Parameters']:
            name = entry['Name'].split(f'/env/{self.env}/')[1]
            secrets[name] = entry['Value']

        invalid_keys = [key for key in response['InvalidParameters']]
        return (secrets, invalid_keys)
