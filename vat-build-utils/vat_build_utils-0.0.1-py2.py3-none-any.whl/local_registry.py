import base64

import docker
from docker.errors import ImageNotFound

class LocalRegistry(object):
    def get_image_repository(self, name):
        return name

    def get_full_image_tag(self, name, tag):
        return "{0}:{1}".format(name, tag)

    def get_auth_config(self):
        return None

    def has_image(self, name, tag):
        docker_client = docker.from_env(version='auto')

        repository = self.get_image_repository(name)

        try:
            docker_client.images.get("{0}:{1}".format(repository, tag))
            return True
        except ImageNotFound:
            return False

    def push_image(self, name, tag):
        pass
