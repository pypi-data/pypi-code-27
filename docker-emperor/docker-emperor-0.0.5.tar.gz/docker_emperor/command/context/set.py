import os
import six
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    def select_context():
        logger.ask('Please select the {}{}{}{} context to work on'.format(logger.BOLD, root.project.name, logger.END, logger.YELLOW))
        for i, c in enumerate(root.project.contexts):
            logger.ask('{}{}){}{} {}'.format(logger.BOLD, i+1, logger.END, logger.YELLOW, c.name))
        ci = six.moves.input(': ')
        try:
            if ci == '0':
                raise Exception
            return root.project.contexts[int(ci)-1]
        except Exception as e:
            logger.error('{} is not a valid choice'.format(ci))
            return select_context()

    root.project.config['context'] = select_context()