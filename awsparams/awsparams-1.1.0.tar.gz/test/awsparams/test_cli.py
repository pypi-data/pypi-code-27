import pytest
import boto3
from click.testing import CliRunner
from moto import mock_ssm

from awsparams import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_sanity_check(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "y")
    assert cli.sanity_check('SomeParam', False)
    monkeypatch.setattr('builtins.input', lambda x: "n")
    assert not cli.sanity_check('SomeParam', False)
    assert cli.sanity_check('SomeParam', True)


@mock_ssm
def test_new(cli_runner):
    result = cli_runner.invoke(
        cli.new,
        [
            '--name',
            'testing.testing.testing',
            '--value',
            '1234',
            '--param_type',
            'SecureString',
            '--key',
            'alias/test/fookey'
        ]
    )
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert result.output.strip() == ''


@mock_ssm
def test_new_simple(cli_runner):
    result = cli_runner.invoke(
        cli.new, ['--name', 'testing.testing.testing', '--value', '1234'])
    assert result.exit_code == 0
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])


@mock_ssm
def test_ls(cli_runner):
    cli_runner.invoke(cli.new, ['--name', 'testing.testing.testing',
                                '--value', '1234', '--param_type', 'SecureString'])
    result = cli_runner.invoke(cli.ls, ['testing.testing.'])
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert result.output.strip() == "testing.testing.testing"


@mock_ssm
def test_ls_values(cli_runner):
    cli_runner.invoke(cli.new, ['--name', 'testing.testing.testing',
                                '--value', '1234', '--param_type', 'SecureString'])
    result = cli_runner.invoke(
        cli.ls, ['testing.testing.', '-v'])
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert result.output.strip() == "testing.testing.testing: 1234"


@mock_ssm
def test_ls__without_decrypt(cli_runner):
    cli_runner.invoke(cli.new, ['--name', 'testing.testing.testing',
                                '--value', '1234', '--param_type', 'SecureString'])
    result = cli_runner.invoke(
        cli.ls, ['testing.testing.', '-v', '--no-decryption'])
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert result.output.strip() == "testing.testing.testing: kms:default:1234"


@mock_ssm
def test_cp_basic(cli_runner):
    cli_runner.invoke(cli.new, ['--name', 'testing.testing.testing',
                                '--value', '1234', '--param_type', 'SecureString'])
    result = cli_runner.invoke(
        cli.cp, ['testing.testing.testing', 'testing.testing.newthing'])
    cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert result.output.strip() == 'Copied testing.testing.testing to testing.testing.newthing'
    cli_runner.invoke(cli.rm, ['testing.testing.newthing', '-f'])
    result = cli_runner.invoke(cli.cp, ['foobar', 'barfoo'])
    assert result.exit_code == 0
    assert result.output.strip() == 'Parameter: foobar not found'


@mock_ssm
def test_cp_prefix(cli_runner):
    ssm = boto3.client('ssm')
    params = [
        {
            'Name': '/testing/testing/foo',
            'Value': 'bar',
            'Type': 'String'
        },
        {
            'Name': '/testing/testing/bar',
            'Value': 'qux',
            'Type': 'String'
        },
        {
            'Name': 'foo',
            'Value': 'bar',
            'Type': 'String'
        }
    ]
    for param in params:
        ssm.put_parameter(**param)

    result = cli_runner.invoke(
        cli.cp, ['/testing/testing/', '/example/example/', '--prefix']
    )
    assert result.exit_code == 0
    all_params = ssm.get_parameters_by_path(Path='/', Recursive=True)
    assert len(all_params['Parameters']) == 5
    examples = ssm.get_parameters_by_path(Path='/example', Recursive=True)
    assert len(examples['Parameters']) == 2
    assert [param['Value'] for param in examples['Parameters']] == [param['Value'] for param in params if '/testing/testing/' in param['Name']]


@mock_ssm
def test_cp_paths_single_item(cli_runner):
    ssm = boto3.client('ssm')
    params = [
        {
            'Name': '/testing/testing/foo',
            'Value': 'bar',
            'Type': 'String'
        },
        {
            'Name': '/testing/testing/bar',
            'Value': 'qux',
            'Type': 'String'
        },
        {
            'Name': 'foo',
            'Value': 'bar',
            'Type': 'String'
        }
    ]
    for param in params:
        ssm.put_parameter(**param)

    result = cli_runner.invoke(
        cli.cp, ['/testing/testing/foo', '/newpath/foo']
    )
    assert result.exit_code == 0
    all_params = ssm.get_parameters_by_path(Path='/', Recursive=True)
    assert len(all_params['Parameters']) == 4
    examples = ssm.get_parameters_by_path(Path='/newpath', Recursive=True)
    assert len(examples['Parameters']) == 1
    assert [param['Value'] for param in examples['Parameters']] == [
        param['Value'] for param in params if '/testing/testing/foo' in param['Name']]


@mock_ssm
def test_cp_fail(cli_runner):
    result = cli_runner.invoke(cli.cp, ['testing.testing.testing'])
    assert result.exit_code == 0
    assert result.output.strip(
    ) == 'dst (Destination) is required when not copying to another profile'


@mock_ssm
def test_rm(cli_runner):
    ssm = boto3.client('ssm')
    cli_runner.invoke(
        cli.new, ['--name', 'testing.testing.testing', '--value', '1234'])
    result = cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    params = ssm.get_parameters_by_path(Path='/', Recursive=True)
    assert len(params['Parameters']) == 0


@mock_ssm
def test_rm_no_params(cli_runner):
    result = cli_runner.invoke(cli.rm, ['testing.testing.testing', '-f'])
    assert result.exit_code == 0
    assert 'Parameter testing.testing.testing not found' == result.output.strip()
    result = cli_runner.invoke(cli.rm, ['testing.testing.', '-f', '--prefix'])
    assert result.exit_code == 0
    assert 'No parameters with the testing.testing. prefix found' == result.output.strip()


@mock_ssm
def test_set(cli_runner):
    cli_runner.invoke(
        cli.new, ['--name', 'testing.testing.testing', '--value', '1234'])
    result = cli_runner.invoke(cli.set, ['testing.testing.testing', '4321'])
    second_result = cli_runner.invoke(
        cli.ls, ['testing.testing.testing', '--values'])
    assert result.exit_code == 0
    assert result.output.strip() == "updated param 'testing.testing.testing' with value"
    assert second_result.output.strip() == "testing.testing.testing: 4321"


@mock_ssm
def test_set_same_value(cli_runner):
    cli_runner.invoke(
        cli.new, ['--name', 'testing.testing.testing', '--value', '1234'])
    result = cli_runner.invoke(cli.set, ['testing.testing.testing', '1234'])
    second_result = cli_runner.invoke(
        cli.ls, ['testing.testing.testing', '--values'])
    assert result.exit_code == 0
    assert result.output.strip() == "not updated, param 'testing.testing.testing' already contains that value"
    assert second_result.output.strip() == "testing.testing.testing: 1234"


@mock_ssm
def test_mv_simple(cli_runner):
    cli_runner.invoke(
        cli.new, ['--name', 'testing.testing.testing', '--value', '1234'])
    result = cli_runner.invoke(
        cli.mv, ['testing.testing.testing', 'testing1.testing1.testing1'])
    second_result = cli_runner.invoke(
        cli.ls, ['testing.testing.testing', '--values'])
    third_result = cli_runner.invoke(
        cli.ls, ['testing1.testing1.testing1', '--values'])
    print(result.output)
    assert result.exit_code == 0
    assert second_result.output.strip() == ""
    assert third_result.output.strip() == "testing1.testing1.testing1: 1234"


@mock_ssm
def test_mv_prefix(cli_runner):
    ssm = boto3.client('ssm')
    params = [
        {
            'Name': '/testing/testing/foo',
            'Value': 'bar',
            'Type': 'String'
        },
        {
            'Name': '/testing/testing/bar',
            'Value': 'qux',
            'Type': 'String'
        },
        {
            'Name': 'foo',
            'Value': 'bar',
            'Type': 'String'
        }
    ]
    for param in params:
        ssm.put_parameter(**param)

    result = cli_runner.invoke(
        cli.mv, ['/testing/testing/', '/example/example/', '--prefix']
    )
    assert result.exit_code == 0
    all_params = ssm.get_parameters_by_path(Path='/', Recursive=True)
    assert len(all_params['Parameters']) == 3
    examples = ssm.get_parameters_by_path(Path='/example', Recursive=True)
    assert len(examples['Parameters']) == 2
    assert [param['Value'] for param in examples['Parameters']] == [
        param['Value'] for param in params if '/testing/testing/' in param['Name']]


@mock_ssm
def test_cp_with_key(cli_runner):
    ssm = boto3.client('ssm')
    param = {
        'Name': '/foo/bar',
        'Value': 'bar',
        'Type': 'SecureString'
    }
    ssm.put_parameter(**param)
    result = cli_runner.invoke(
        cli.cp, ['/foo/bar', '/bar/foo', '--key', 'somekmskey']
    )
    assert result.exit_code == 0
    assert result.output.strip() == 'Copied /foo/bar to /bar/foo'
    response = ssm.get_parameter(Name='/bar/foo')
    assert response['Parameter']['Value'] == f'kms:somekmskey:{param["Value"]}'


@mock_ssm
def test_new_with_key(cli_runner):
    ssm = boto3.client('ssm')
    result = cli_runner.invoke(
        cli.new, ['--name', '/foo/bar', '--value', 'bar', '--param_type', 'SecureString', '--key', 'somekmskey']
    )

    assert result.exit_code == 0
    param = ssm.get_parameter(Name='/foo/bar')
    assert param['Parameter'].get('Value') == 'kms:somekmskey:bar'
