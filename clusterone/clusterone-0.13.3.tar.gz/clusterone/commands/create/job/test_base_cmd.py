from collections import OrderedDict

import pytest
from click import BadArgumentUsage, BadOptionUsage

from clusterone.clusterone_cli import Context
from clusterone.commands.create.job import base_cmd
from clusterone.commands.create.job.base_cmd import validate_module_arguments
from clusterone.commands.create.job.base_cmd import _prepare_list_of_datasets
from clusterone.persistance.session import Session


def test_python_version_aliases(mocker):
    path_to_project_return_value = {'id': "project-id-123456",
                                    "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]),
                                                OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d2')])]}
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value=path_to_project_return_value)
    mocker.patch('clusterone.commands.create.job.base_cmd.client')
    mocker.patch('clusterone.commands.create.job.base_cmd.time_limit_to_minutes', return_value=123456)
    kwargs_py2 = {'framework': 'tensorflow-130',
                  'project_path': 'mnist-demo',
                  'python_version': '2',
                  'requirements': None,
                  'commit': 'latest',
                  'name': 'old-morning-562',
                  'module': 'mymodule.py',
                  'package_manager': 'pip',
                  'package_path': '',
                  'description': '',
                  'time_limit': 2880,
                  'datasets': '', }
    kwargs_py3 = {'framework': 'tensorflow-130',
                  'project_path': 'mnist-demo',
                  'python_version': '3',
                  'requirements': None,
                  'commit': 'latest',
                  'name': 'old-morning-562',
                  'module': 'mymodule.py',
                  'package_manager': 'pip',
                  'package_path': '',
                  'description': '',
                  'time_limit': 2880,
                  'datasets': '', }

    session = Session()
    session.load()
    context = Context(None, session, None)

    result_py2 = base_cmd.base(context, kwargs_py2, module_arguments=())
    result_py3 = base_cmd.base(context, kwargs_py3, module_arguments=())

    assert result_py2['parameters']['python_version'] == '2.7'
    assert result_py3['parameters']['python_version'] == '3.6'


def test_package_manager_aliases(mocker):
    path_to_project_return_value = {'id': "project-id-123456",
                                    "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]),
                                                OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d2')])]}
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value=path_to_project_return_value)
    mocker.patch('clusterone.commands.create.job.base_cmd.client')
    mocker.patch('clusterone.commands.create.job.base_cmd.time_limit_to_minutes', return_value=123456)
    kwargs = {'framework': 'tensorflow-130',
              'project_path': 'mnist-demo',
              'python_version': '3',
              'requirements': None,
              'commit': 'latest',
              'name': 'old-morning-562',
              'module': 'mymodule.py',
              'package_manager': 'anaconda',
              'package_path': '',
              'description': '',
              'time_limit': 2880,
              'datasets': '', }

    session = Session()
    session.load()
    context = Context(None, session, None)

    result = base_cmd.base(context, kwargs, module_arguments=())

    assert result['parameters']['package_manager'] == 'conda'


def test_default_requirement_conda(mocker):
    path_to_project_return_value = {'id': "project-id-123456",
                                    "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]),
                                                OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]}
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value=path_to_project_return_value)
    mocker.patch('clusterone.commands.create.job.base_cmd.client')
    mocker.patch('clusterone.commands.create.job.base_cmd.time_limit_to_minutes', return_value=123456)
    kwargs = {'framework': 'tensorflow-1.3.0',
              'project_path': 'mnist-demo',
              'python_version': '3',
              'requirements': None,
              'commit': 'latest',
              'name': 'old-morning-562',
              'module': 'mymodule.py',
              'package_manager': 'anaconda',
              'package_path': '',
              'description': '',
              'time_limit': 2880,
              'datasets': '', }

    session = Session()
    session.load()
    context = Context(None, session, None)

    result = base_cmd.base(context, kwargs, module_arguments=())

    assert result['parameters']['requirements'] == 'requirements.yml'


class TestValidateModuleArguments:
    def test_should_return_custom_arguments_when_proper_call_was_made(self):
        raw_value = ('--first', 'first', '--second', 'second')

        result = validate_module_arguments(None, None, raw_value)

        expected = {'first': 'first',
                    'second': 'second'}

        assert result == expected

    @pytest.mark.parametrize(
        'raw_value', [
            ('--first', 'first_value', '--second', '--second_value'),
            ('--first', '--first_value', '--second', 'second_value'),
        ]
    )
    def test_bad_value(self, raw_value):
        with pytest.raises(BadOptionUsage):
            validate_module_arguments(None, None, raw_value)

    @pytest.mark.parametrize(
        'raw_value', [
            ('first', 'first_value', '--second', 'second_value'),
            ('--first', 'first_value', 'second', 'second_value'),
        ]
    )
    def test_bad_value(self, raw_value):
        with pytest.raises(BadArgumentUsage):
            validate_module_arguments(None, None, raw_value)

    @pytest.mark.parametrize(
        'raw_value', [
            ('--first', 'first_value', '--second'),
            ('--first', '--second', 'second_value'),
        ]
    )
    def test_missing_values_for_options(self, raw_value):
        with pytest.raises(BadOptionUsage):
            validate_module_arguments(None, None, raw_value)


def test_should_return_an_empty_list_when_datasets_in_kwargs_is_empty():
    kwargs = {'datasets': ''}

    data_sets = _prepare_list_of_datasets('context', kwargs)

    assert data_sets == []


def test_should_return_a_list_of_dicts_when_datasets_in_kwargs_is_not_empty(mocker):
    path_to_dataset_patched = mocker.patch('clusterone.commands.create.job.base_cmd.path_to_dataset',
                                           return_value={'id': 'fake_id'})

    kwargs = {'datasets': 'username/project_name, keton/beton:fake-commit-hash'}

    datasets_list = _prepare_list_of_datasets('fake_context', kwargs)
    fst_dataset = datasets_list[0]
    snd_dataset = datasets_list[1]

    assert fst_dataset == {'dataset': 'fake_id'}
    path_to_dataset_patched.assert_called_with('keton/beton', context='fake_context')
    assert snd_dataset == {'dataset': 'fake_id', 'git_commit_hash': 'fake-commit-hash'}
