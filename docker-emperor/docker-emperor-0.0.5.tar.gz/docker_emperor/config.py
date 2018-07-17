import six
import os
import json
from docker_emperor.command import Command
from docker_emperor.utils import memoized_property


__all__ = ['Config']


class Config():

    def __init__(self, root, path=".docker-emperor"):

        self.root = root
        self.path = os.path.expanduser(os.path.join('~', path))
        try:
            self.data = json.loads(open(self.path, 'rb'))
        except:
            self.data = {}            
        # try:
        #     root.data
        # except DockerEmperorException:
        #     pass

    def save(self):
        file = open(self.path, 'wb')
        file.write( json.dumps(self.data) )
        file.close()

    def projects(self):
        return self.data.get('projects', {})
        if not isinstance(project, dict):
            project = {}

    def project(self):
        project = self.projects.get(self.root.project_name, {})
        if not isinstance(project, dict):
            project = {}
        return project

    def context(self, name):
        if self.project:
            project = self.projects.get(name, None)
        else:
            return None

    def set_context(self, name):
        project = self.projects.get(name, None)
        return project

    def machine(self, name):
        project = self.projects.get(name, None)
        return project

    def set_machine(self, name):
        project = self.projects.get(name, None)
        return project

