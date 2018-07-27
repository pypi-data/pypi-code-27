"""This module expose methods for use lxc library."""
import logging
from pylxd import exceptions, Client
import urllib3
import click
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class lxc:

    connection = None

    def __init__(self):
        pass

    @staticmethod
    def get_connection(host=os.environ['LXC_CLI_HOST'], port=os.environ['LXC_CLI_PORT'],
                       cert=os.environ['LXC_CLI_CERT'], key=os.environ['LXC_CLI_KEY']):
        """Create connection on LXC."""
        if lxc.connection is None:
            try:
                lxc.connection = Client(
                    endpoint='https://{}:{}'.format(host, port),
                    cert=(cert, key),
                    verify=False)
                lxc.connection.authenticate(os.environ['LXC_CLI_PASSWD'])
                logging.info("CONNECTION: Connection success.")
            except exceptions.ClientConnectionFailed:
                logging.error("CONNECTION: Connection failed.")
                raise
        return lxc.connection

    @staticmethod
    @click.command()
    @click.option('--old_name', '-o', required=1, help='old name of container')
    @click.option('--new_name', '-n', required=1, help='new name of container')
    def rename(old_name, new_name):
        """Rename a container on LXC."""
        try:
            container = lxc.get_connection().containers.get(old_name)
            container.stop()
            container.rename(new_name)
            container.start()
            logging.info('Container %s was renamed successfully', new_name)
            print('Container %s was renamed successfully', new_name)
        except (exceptions.LXDAPIException, exceptions.ClientConnectionFailed):
            print("Error on renaming container. " +
                  "Verify if the container name is corrected.")
            logging.error("RENAME: Error on renaming container. " +
                          "Verify if the container name is corrected.")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1,
                  help='container to be stopped')
    def remove(container):
        """Remove a container on LXC."""
        try:
            lxc.get_connection().containers.get(container).stop()
            lxc.get_connection().containers.get(container).delete()
            logging.info('Container %s was deleted successfully', container)
            print('Container %s was deleted successfully', container)
        except (exceptions.LXDAPIException, exceptions.ClientConnectionFailed):
            print("Error on removing container. " +
                  "Verify if the container is stopped.")
            logging.error("REMOVE: Error on removing container. " +
                          "Verify if the container is stopped.")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1,
                  help='container to be stopped')
    def stop(container):
        """Stop a container on LXC."""
        try:
            lxc.get_connection().containers.get(container).stop()
            logging.info('Container %s was stopped successfully', container)
            print('Container %s was stopped successfully', container)
        except (exceptions.LXDAPIException, exceptions.ClientConnectionFailed):
            logging.error("Wrong command. Please, use --help command.")
            print("Wrong command. Please, use --help command.")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1,
                  help='container to be started')
    def start(container):
        """Start a container on LXC."""
        try:
            lxc.get_connection().containers.get(container).start()
            logging.info('Container %s was started successfully', container)
            print('Container %s was started successfully', container)
        except (exceptions.LXDAPIException, exceptions.ClientConnectionFailed):
            logging.error("START: Wrong command. Please, use --help command.")
            print("Wrong command. Please, use --help command.")

    @staticmethod
    @click.command()
    @click.option('--component', '-c', required=1,
                  help='component to be listed')
    @click.option('--json_format', '-j', help='format to be showed')
    def list(component, json_format):
        """List all containers on LXC."""
        try:
            conn = lxc.get_connection()
            if component == 'containers':
                if json_format:
                    containers = map(lambda container: {
                                "name": container.name,
                                "status": container.status,
                                "created_date": container.created_at
                            }, conn.containers.all())
                    print(list(containers))
                else:
                    print("Name    Status    Created")
                    for container in conn.containers.all():
                        print(container.name + "    " + container.status +
                              "    " + container.created_at)
                logging.info("LIST: List all containers")
            elif component == 'images':
                if json_format:
                    images = map(lambda image: {
                            "name": image.architecture,
                            "properties": str(image.properties),
                            "created_date": image.created_at
                        }, conn.containers.all())
                    print(images)
                else:
                    for image in conn.images.all():
                        print("Architecture    Created    Properties")
                        print(image.architecture + "    " + image.created_at +
                              "    " + str(image.properties))
                logging.info("LIST: List all images")
            else:
                logging.error("LIST: Wrong parameters. Please, use --help")
                print("Wrong parameters. Please, use --help")
                raise Exception
        except exceptions.ClientConnectionFailed:
            logging.error("LIST: Error during connection")
            print("Error during connection")

    @staticmethod
    @click.command()
    @click.option('--name', '-n', required=1, help='name')
    @click.option('--image', '-i', required=1,
                  help='linux distribution')
    @click.option('--server', '-s', required=1,
                  help='linux server')
    def create(name, image, server):
        """Create a container on LXC."""
        try:
            if name is not '' and image is not '' and server is not '':
                config = {
                    'name': name,
                    'source': {
                        'type': 'image',
                        'alias': image,
                        'protocol': 'simplestreams',
                        'server': server
                        }
                    }
                container = lxc.get_connection().containers.create(config, wait=True)
                container.start(wait=True)
                logging.info('Container %s was created successfully', name)
                print('Container %s was created successfully', name)
            else:
                logging.error("CREATE: Wrong parameters. Please, use --help")
                print("Wrong parameters. Please, use --help")
                raise Exception
        except (exceptions.LXDAPIException, exceptions.ClientConnectionFailed):
            logging.error("CREATE: Error on creating container. Try again!")
            print("Error on creating container. Try again!")
