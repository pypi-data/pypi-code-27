from awslabs.challenge import Challenge
import boto3
import yaml
import os
import click
from cfn_tools.yaml_loader import CfnYamlLoader, ODict

class MyChallenge(Challenge):

    title = "Launch an instance"
    description = (
        "Tasks:\n"
        " - Start a new template.yaml.\n"
        " - Create an instance with type t2.small and ImageId: ami-d834aba1.\n"
        " - The logic ID should be exactly: Ec2Instance.\n"
        " - The stack name should be: awslabs, deploy in eu-west-1"
    )

    def start(self):
        self.instructions()

    def validate(self):
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
                        it = doc['Resources']['Ec2Instance']['Properties']['InstanceType']
                        ami = doc['Resources']['Ec2Instance']['Properties']['ImageId']
                        click.echo('found the resource in template')
                    except:
                        return self.fail("Cannot find the Ec2Instance Resource in the template.")  
                    
                    if it != 't2.small':
                        return self.fail("InstanceType is not t2.small")
                    elif ami != 'ami-d834aba1':
                        return self.fail("ImageId is not ami-d834aba1")
                    else:
                        client = boto3.client('cloudformation')
                        try:
                            stack = client.describe_stacks(
                                StackName='awslabs'
                            )
                            click.echo('found the stack!')
                        except:
                            return self.fail("Stack awslabs not deployed.")
                        
                        try:
                            resource = client.describe_stack_resources(
                                StackName='awslabs',
                                LogicalResourceId='Ec2Instance'
                            )
                            instance_id = resource['StackResources'][0]['PhysicalResourceId']
                            click.echo('found the resource!')
                        except:
                            return self.fail("Stack does not contain a resource Ec2Instance.")

                        # instance check
                        try:
                            ec2 = boto3.client('ec2')
                            instance = ec2.describe_instances(
                                InstanceIds=[instance_id]
                            )
                            click.echo('found the instance!')
                        except:
                            return self.fail("Cannot find the instance.")

                        if not instance['Reservations'][0]['Instances'][0]['ImageId'] == 'ami-d834aba1':
                            return self.fail("Deployed instance has a wrong ImageId")
                        else:
                            return self.success("You deployed the instance with cloudformation!")
        else:
            return self.fail("Cannot find template.yaml")

        
