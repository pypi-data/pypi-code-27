import boto3


class AwsClient(object):

    def __init__(self, aws_profile='default'):
        s = boto3.Session(profile_name=aws_profile)
        self._client = s.resource('ec2')


class AwsEc2(AwsClient):

    def list(self, _filter=[]):
        instances = self._client.instances.filter(Filters=[
            {
                'Name': name,
                'Values': value if type(value) == list else [value]
            }
            for name, value in _filter
        ])

        def by_name(instance):
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    return tag['Value']

        instances = sorted(instances, key=by_name)
        return [AwsEc2Instance(instance) for instance in instances]


class AwsVpc(AwsClient):

    def list(self):
        return self._client.vpcs.all()


class AwsEc2Instance(object):

    def __init__(self, instance):
        self._instance = instance

    def name(self):
        for tag in self._instance.tags:
            if tag['Key'] == 'Name':
                return tag['Value']

    def state(self):
        state_fg = 'red'
        state = self._instance.state['Name']
        if state == 'running':
            state_fg = 'green'

        return state, state_fg

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
