from subprocess import call
import click
import logging


class lxc:

    @staticmethod
    @click.command()
    @click.option('--old_name', '-o', required=1, help='old name of container')
    @click.option('--new_name', '-n', required=1, help='new name of container')
    def rename(old_name, new_name):
        result = call(["lxc", "stop", old_name])
        if result == 1:
            call(["echo", "Error on stopping container"])
            logging.error("Error on stopping container")
        else:
            result = call(["lxc", "move", old_name, new_name])
            if result == 1:
                call(["echo", "Error on renaming container"])
                logging.error("Error on renaming container")
            else:
                call(["lxc", "start", new_name])
                call(["echo", "Container " + new_name + " was renamed successfully"])
                logging.info("Container " + new_name + " was renamed successfully")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1, help='container to be stopped')
    def remove(container):
        result = call(["lxc", "stop", container])
        if result == 1:
            call(["echo", "Error on stopping container"])
            logging.error("Error on stopping container")
        else:
            result = call(["lxc", "delete", container])
            if result == 1:
                call(["echo", "Error on deleting container"])
                logging.error("Error on deleting container")
            else:
                call(["echo", "Container " + container + " was deleted successfully"])
                logging.info("Container " + container + " was deleted successfully")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1, help='container to be stopped')
    def stop(container):
        result = call(["lxc", "stop", container])
        if result == 1:
            call(["echo", "Wrong command. Please, use --help command."])
            logging.error("Wrong command. Please, use --help command.")
        else:
            call(["echo", "Container " + container + " was stopped successfully"])
            logging.info("Container " + container + " was stopped successfully")

    @staticmethod
    @click.command()
    @click.option('--container', '-c', default='CONTAINER', required=1, help='container to be started')
    def start(container):
        result = call(["lxc", "start", container])
        if result == 1:
            call(["echo", "Wrong command. Please, use --help command."])
            logging.error("Wrong command. Please, use --help command.")
        else:
            call(["echo", "Container " + container + " was started successfully"])
            logging.info("Container " + container + " was started successfully")

    @staticmethod
    @click.command()
    @click.option('--component', '-c', default='COMPONENT', required=1, help='component to be listed')
    def list(component):
        if component == 'containers':
            call(["lxc", "list"])
            logging.info("List all containers")
        elif component == 'images':
            call(["lxc", "list", "images"])
            logging.info("List all images")
        else:
            call(["echo", "Wrong parameters. Please, use --help"])
            logging.error("Wrong parameters. Please, use --help")

    @staticmethod
    @click.command()
    @click.option('--image', '-i', default='TEMPLATE', required=1, help='linux distribution')
    @click.option('--name', '-n', default='NAME', required=1, help='name')
    def create(image, name):
        result = call(["lxc", "launch", image, name])
        if result == 1:
            logging.info("Error on creating container. Try again!")
        else:
            call(["echo", "Container " + name + " was created successfully"])
            logging.info("Container " + name + " was created successfully")
