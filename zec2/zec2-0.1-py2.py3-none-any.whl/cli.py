import click
from terminaltables import AsciiTable

from zec2.aws_ec2 import AwsEc2, AwsVpc


@click.group()
def cli():
    pass


@cli.command()
def ls():
    ec2 = AwsEc2()
    vpcs = AwsVpc()

    i = 0

    for vpc in vpcs.list():
        instances = ec2.list(_filter=[('vpc-id', vpc.id)])

        table_data = [
            ['', 'Name', 'Private IP', 'Public IP', 'State', 'Key Pair', 'Type', 'Launch time'],
        ]

        click.echo()
        click.secho(vpc.id, fg='red')

        for instance in instances:
            row = list()

            row.append(str(i+1))
            row.append(click.style(instance.name(), fg='blue'))
            row.append(instance.aws.private_ip_address)
            row.append(instance.aws.public_ip_address)
            state, state_fg = instance.state()
            row.append(click.style(state, fg=state_fg))
            row.append(instance.aws.key_name)
            row.append(instance.aws.instance_type)
            row.append(instance.aws.launch_time)

            table_data.append(row)

            i += 1

        table = AsciiTable(table_data)

        click.echo(table.table)
        click.echo()


@cli.command()
@click.argument('number')
@click.option('-u', '--user', help='SSH user')
@click.option('-i', '--key_path', help='SSH user')
def ssh(number, user, key_path):
    ec2 = AwsEc2()
    vpcs = AwsVpc()

    instances = list()
    for vpc in vpcs.list():
        instances += ec2.list(_filter=[('vpc-id', vpc.id)])

    instance = instances[int(number)-1]
    click.echo(instance.ssh_command(user, key_path))
