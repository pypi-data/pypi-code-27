import boto3
import pytest
from moto import mock_ssm
from botocore.exceptions import ProfileNotFound

from awsparams import AWSParams, ParamResult


@pytest.fixture
@mock_ssm
def fake_param():
    ssm = boto3.client('ssm')
    param = {
        'Name': 'fakeparam',
        'Type': 'String',
        'Value': 'fakevalue'
    }
    ssm.put_parameter(**param)
    yield param
    ssm.delete_parameter(Name=param['Name'])


@pytest.fixture
@mock_ssm
def awsparams():
    return AWSParams()


@mock_ssm
def test_connect_ssm(awsparams):
    assert awsparams._connect_ssm()
    try:
        assert awsparams._connect_ssm('blahblah')
    except ProfileNotFound:
        pass


def test_awsparam():
    assert AWSParams()
    try:
        assert AWSParams('default')
    except ProfileNotFound:
        pass


@mock_ssm
def test_put_parameter(awsparams):
    ssm = boto3.client('ssm')
    param = {
        'Name': 'fakeparam',
        'Type': 'String',
        'Value': 'fakevalue'
    }
    awsparams.put_parameter(param)
    result = ssm.get_parameters(Names=['fakeparam'])['Parameters']
    assert result[0]['Name'] == param['Name']
    assert result[0]['Value'] == param['Value']
    assert result[0]['Type'] == param['Type']


@mock_ssm
def test_put_parameter_profile(awsparams):
    param = {
        'Name': 'fakeparam',
        'Type': 'String',
        'Value': 'fakevalue'
    }
    try:
        awsparams.put_parameter(param, profile='default')
        result = awsparams.get_parameter('fakeparam', values=True)
        assert result == ParamResult(**param)
    except ProfileNotFound:
        pytest.skip(msg="No Profiles to test")


@mock_ssm
def test_remove_parameter(fake_param, awsparams):
    ssm = boto3.client('ssm')
    param = next(fake_param)
    awsparams.remove_parameter(param['Name'])
    result = ssm.get_parameters(Names=['fakeparam'])['Parameters']
    assert len(result) == 0


@mock_ssm
def test_remove_nonexisting_parameter(awsparams):
    ssm = boto3.client('ssm')
    awsparams.remove_parameter('fakeparam')
    result = ssm.get_parameters(Names=['fakeparam'])['Parameters']
    assert len(result) == 0


@mock_ssm
def test_get_parameter_value(fake_param, awsparams):
    param = next(fake_param)
    result = awsparams.get_parameter_value(param['Name'])
    assert result == param['Value']


@mock_ssm
def test_get_parameter(fake_param, awsparams):
    param = next(fake_param)
    result = awsparams.get_parameter(param['Name'])
    assert result == ParamResult(**param)
    result = awsparams.get_parameter('notarealparam')
    assert result is None


@mock_ssm
def test_build_param_result(fake_param, awsparams):
    param = next(fake_param)
    result = awsparams.build_param_result(param)
    assert result == ParamResult(**param)
    assert result._asdict() == param


@mock_ssm
def test_get_all_parameters(fake_param, awsparams):
    next(fake_param)
    ssm = boto3.client('ssm')
    param2 = {
        'Name': 'fakeparam2',
        'Type': 'String',
        'Value': 'fakevalue2'
    }
    ssm.put_parameter(**param2)
    result = awsparams.get_all_parameters(values=True)
    assert len(result) == 2


@mock_ssm
def test_get_all_parameters_path(awsparams):
    ssm = boto3.client('ssm')
    params = [{
        'Name': '/foo/bar',
        'Type': 'String',
        'Value': 'bar'
    },
        {
        'Name': '/foo/baz',
        'Type': 'String',
        'Value': 'baz'
    },
        {
        'Name': '/bar/baz',
        'Type': 'String',
        'Value': 'baz'
    }]
    for param in params:
        ssm.put_parameter(**param)
    result = awsparams.get_all_parameters(
        prefix='/foo/', by_path=True, values=True)
    assert len(result) == 2


@mock_ssm
def test_new_param(awsparams):
    awsparams.new_param(name='foo', value='bar', param_type='String', description='a test parameter')
    param = awsparams.get_parameter(name='foo')
    assert param.Name == 'foo'
    assert param.Value == 'bar'


@mock_ssm
def test_set_param(fake_param, awsparams):
    next(fake_param)
    assert awsparams.set_param('fakeparam', 'foobar')
    assert 'foobar' == awsparams.get_parameter_value(name='fakeparam')
    # Don't change if same value
    assert not awsparams.set_param('fakeparam', 'foobar')
