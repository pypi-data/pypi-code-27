from awslabs.challenge import Challenge
import boto3
import os
import yaml
import click
from cfn_tools.yaml_loader import CfnYamlLoader, ODict


class MyChallenge(Challenge):

    title = "ParameterStore"
    description = (
        "- Get the latest AMI from the parameter store.\n"
        "- Use image: /aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-ebs"
    )

    def start(self):
        self.instructions()

    def validate(self):
        
        client = boto3.client('ssm')
        response = client.get_parameter(
            Name='/aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-ebs'
        )
        ami_to_be_used = response['Parameter']['Value']

        if os.path.isfile('./template.yaml'):
            with open('./template.yaml', 'r') as f:
                try:
                    doc = yaml.load(f, Loader=CfnYamlLoader)
                except:
                    return self.fail("Failed to load your template.yaml")
                if doc is None:
                    return self.fail("No valid yaml!")
                else:
                    try:
                        param_type = doc['Parameters']['LatestAmiId']['Type']
                        ami = doc['Resources']['Ec2Instance']['Properties']['ImageId']
                        click.echo('template.yaml looks valid')
                    except:
                        return self.fail("Your template.yaml contains errors.")

                    if ami != ODict([('Fn::Ref:', 'LatestAmiId')]) and ami != ODict([('Ref', 'LatestAmiId')]):
                        return self.fail("Use Ref to use the parameter from parameter store")
                    else:
                        # stack
                        client = boto3.client('cloudformation')
                        try:
                            stack = client.describe_stacks(
                                StackName='awslabs'
                            )
                            click.echo('found the stack!')
                        except:
                            return self.fail("Stack awslabs not deployed.")
                        
                        # resource
                        try:
                            resource = client.describe_stack_resources(
                                StackName='awslabs',
                                LogicalResourceId='Ec2Instance'
                            )
                            instance_id = resource['StackResources'][0]['PhysicalResourceId']
                            click.echo('found the resource! ({})'.format(instance_id))
                        except:
                            return self.fail("Stack does not contain a resource Ec2Instance.")
                        
                        # instance check
                        try:
                            ec2 = boto3.client('ec2')
                            instance = ec2.describe_instances(
                                InstanceIds=[instance_id]
                            )
                        except:
                            return self.fail("Cannot find the instance.")

                        if not instance['Reservations'][0]['Instances'][0]['ImageId'] == ami_to_be_used:
                            return self.fail("Deployed instance has a wrong ImageId")
                        else:
                            return self.success("You deployed the correct ami, with the correct parameter!")
        else:
            return self.fail("Cannot find template.yaml")