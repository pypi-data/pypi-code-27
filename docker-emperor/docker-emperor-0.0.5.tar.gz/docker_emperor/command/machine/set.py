import os
import six
import docker_emperor.logger as logger


__all__ = ['run']


def run(root, *args, **kwargs):


    def select_machine():
        # logger.ask('0) no machine (localhost)')
        logger.ask('Please select the {}{}{}{} machine to work on'.format(logger.BOLD, root.project.name, logger.END, logger.YELLOW))
        for i, m in enumerate(root.project.machines):
            logger.ask('{}{}){}{} {}'.format(logger.BOLD,i+1, logger.END, logger.YELLOW, m.name))
        mi = six.moves.input(': ')
        try:
            if mi == '0':
                raise Exception
            return root.project.machines[int(mi)-1]
        except Exception as e:
            logger.error('{} is not a valid choice'.format(mi))
            return select_machine()

    root.project.config['machine'] = select_machine()
