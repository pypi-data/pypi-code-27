import six
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    def select_context_name():
        logger.ask(u'Please select the <b>{}</b> context to work on'.format(root.project.name))
        for i, c in enumerate(root.project['contexts']):
            logger.choice(u'<b>%s</b>) %s' % (i+1, c.name))
        ci = six.moves.input(': ')
        try:
            if ci == '0':
                raise Exception
            return root.project['contexts'][int(ci)-1].name
        except Exception as e:
            logger.error(u'<b>%s/b> is not a valid choice' % ci)
            return select_context_name()

    root.project.config['context'] = select_context_name()
    logger.success(u'Context <b>%s</b> selected.' % root.project.context.name)