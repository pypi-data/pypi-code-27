import click
import pytest

from clusterone import ClusteroneClient
from clusterone.business_logic.notebook_command import CreateNotebookCommand
from clusterone.just_client import Notebook


class TestCreateNotebookCommand(object):
    @pytest.fixture
    def command_base(self, mocker):
        command_base = mocker.Mock()
        command_base.return_value = {'parameters': {'workers': None},
                                     'meta': {'name': 'my-notebook',
                                              'description': 'My description'}}

        return command_base

    @pytest.fixture
    def client(self, mocker):
        return mocker.Mock(spec=ClusteroneClient)

    @pytest.fixture
    def notebook_class(self, mocker):
        return mocker.Mock(spec=Notebook)

    @pytest.fixture
    def context(self, mocker):
        return mocker.Mock(spec=click.Context)

    def test_should_return_configured_notebook_when_called(self, command_base, client, notebook_class, context):
        custom_arguments = {'some_custom_argument': 'some_value'}
        kwargs = {'instance_type': 't2.small'}

        params = {'context': context,
                  'custom_arguments': custom_arguments,
                  'kwargs': kwargs}

        expected_notebook_params = {'name': 'my-notebook',
                                    'description': 'My description',
                                    'mode': CreateNotebookCommand.JOB_MODE,
                                    'workers': {'slug': 't2.small',
                                                'replicas': CreateNotebookCommand.WORKER_REPLICA_COUNT},
                                    'framework': CreateNotebookCommand.JOB_FRAMEWORK}

        command = CreateNotebookCommand(params, command_base, client, notebook_class)
        command.execute()

        notebook_class.assert_called_with(client, expected_notebook_params)
        assert notebook_class.call_count == 1

        command_base.assert_called_with(context, kwargs, module_arguments=custom_arguments)
        assert command_base.call_count == 1
