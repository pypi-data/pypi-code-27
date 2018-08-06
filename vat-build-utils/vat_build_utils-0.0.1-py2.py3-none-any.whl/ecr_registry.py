import base64

import boto3
from botocore.exceptions import ClientError
import docker

from build_utils import docker_utils

class EcrRegistry(object):
    def __init__(self, config):
        self.host = config['host']
        self.repositories = config.get('repositories', {})
        self.registry_id = self.host.split('.')[0]

    def get_image_repository(self, name):
        # return "{0}/{1}".format(self.host, name)
        return self.repositories[name]

    def get_full_image_tag(self, name, tag):
        return "{0}/{1}:{2}".format(self.host, name, tag)

    def has_image(self, name, tag):
        ecr_client = boto3.client('ecr')
        repository = self.get_image_repository(name)

        try:
            ecr_client.describe_images(
                registryId=self.registry_id,
                repositoryName=repository,
                imageIds=[{'imageTag': tag}]
            )
            return True

        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ImageNotFoundException':
                return False
            else:
                raise ex

    def push_image(self, name, tag):
        docker_client = docker.APIClient(version='auto')
        docker_utils.push_docker_image(
            docker_client,
            repository=self.get_image_repository(name),
            tag=tag,
            auth_config=self._get_auth_config(),
            stream=True
        )

    def _get_auth_config(self):
        ecr_client = boto3.client('ecr')

        token_response = ecr_client.get_authorization_token(registryIds=[self.registry_id])
        username, password = base64.b64decode(
            token_response['authorizationData'][0]['authorizationToken']).encode().split(':')

        return {
            'username': username,
            'password': password
        }
