'''
ECS Helper class to provide interactions with the ECS API
'''
import boto3

class EcsHelper(object):
    """docstring for EcsHelper.
    """

    def __init__(self, region):
        """Initializer

        Args:
            N/A

        Returns:
            N/A

        """
        super(EcsHelper, self).__init__()
        self.region = region
        self.client = boto3.Session(region_name=self.region).client('ecs')

    def list_services(self, cluster, arn_list, token):
        '''Return list of services for an environment/region pair

        Args:
            N/A

        Returns:
            list
        '''
        response = self.client.list_services(
            cluster=cluster,
            nextToken=token
        )

        for service in response['serviceArns']:
            arn_list.append(service)

        if 'nextToken' in response:
            self.list_services(cluster, arn_list, token=response['nextToken'])

        return arn_list
