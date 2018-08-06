import boto3
from click import UsageError
from botocore import exceptions


class AwsClient(object):

    def __init__(self):
        self._aws_profile = 'default'

    def aws_profile(self, _aws_profile):
        self._aws_profile = _aws_profile

    @property
    def client(self):
        try:
            s = boto3.Session(profile_name=self._aws_profile)
            return s.resource('ec2')
        except exceptions.ProfileNotFound as e:
            raise UsageError(str(e))
        except exceptions.ConfigParseError as e:
            raise UsageError(str(e))
        except exceptions.ConfigNotFound as e:
            raise UsageError(str(e))
        except exceptions.UnknownCredentialError as e:
            raise UsageError(str(e))


class AwsEc2(AwsClient):

    def list(self, _filter=None):

        if _filter is None:
            _filter = []

        instances = self.client.instances.filter(Filters=[
            {
                'Name': name,
                'Values': value if type(value) == list else [value]
            }
            for name, value in _filter
        ])

        def by_name(instance):
            for tag in instance.tags or []:
                if tag['Key'] == 'Name':
                    return tag['Value']
            else:
                return ''

        instances = sorted(instances, key=by_name)
        return [AwsEc2Instance(instance) for instance in instances]


class AwsVpc(AwsClient):

    def list(self):
        return self.client.vpcs.all()


class AwsEc2Instance(object):

    states = {
        'running': 'green',
        'stopping': 'yellow',
        'stopped': 'red',
        'pending': 'yellow',
        'shutting-down': 'red'
    }

    def __init__(self, instance):
        self._instance = instance

    def name(self):
        for tag in self._instance.tags or []:
            if tag['Key'] == 'Name':
                return tag['Value']
        else:
            return ''

    def state(self):
        state = self._instance.state['Name']
        state_fg = self.states.get(state, 'red')
        return state, state_fg

    def zone(self):
        return str(self._instance.placement['AvailabilityZone'])

    @property
    def aws(self):
        return self._instance

    def ssh_command(self, user, key_path):
        if not user:
            user = 'ec2-user'
        if not key_path:
            key_path = '~/.ssh/%s.pem' % self._instance.key_name
        params = (key_path, user, self._instance.public_ip_address)
        return 'ssh -i %s %s@%s' % params

    def stop(self):
        self._instance.stop()

    def start(self):
        self._instance.start()

    def restart(self):
        self._instance.reboot()

    def terminate(self):
        self._instance.terminate()

    def disable_api_termination(self):
        self._instance.modify_attribute(DisableApiTermination={'Value': False})
