from clusterone.just_client import Notebook


class CreateNotebookCommand(object):
    JOB_MODE = 'single'
    WORKER_REPLICA_COUNT = 1
    JOB_FRAMEWORK = {'slug': 'jupyter'}

    def __init__(self, params, command_base, client, notebook_class=Notebook):
        self.context = params['context']
        self.custom_arguments = params['custom_arguments']
        self.kwargs = params['kwargs']
        self.command_base = command_base
        self.client = client
        self.notebook_class = notebook_class

    def execute(self):
        configuration = self._prepare_notebook_configuration()
        notebook = self.notebook_class(self.client, configuration)

        return notebook

    def _prepare_notebook_configuration(self):
        config = self.command_base(self.context, self.kwargs, module_arguments=self.custom_arguments)
        notebook_configuration = config['parameters']
        notebook_meta = config['meta']

        notebook_configuration['mode'] = self.JOB_MODE
        notebook_configuration['workers'] = {'slug': self.kwargs['instance_type'],
                                             'replicas': self.WORKER_REPLICA_COUNT}
        notebook_configuration['framework'] = self.JOB_FRAMEWORK
        notebook_configuration.update(notebook_meta)

        return notebook_configuration
