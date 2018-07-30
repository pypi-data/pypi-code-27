import json

import boto3
import botocore
from datetime import datetime
import pystache

cf = boto3.client('cloudformation')

def main(stack_name, template, mustache_variables):
    'Update or create stack'

    template_data = _parse_template(template, mustache_variables)
    params = {
        'StackName': stack_name,
        'TemplateBody': template_data
    }

    try:
        if _stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            stack_result = cf.update_stack(
                **params,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'])
            waiter = cf.get_waiter('stack_update_complete')
            waiter.wait(StackName=stack_name)
        else:
            print('Creating {}'.format(stack_name))
            stack_result = cf.create_stack(
                **params,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'])
            try:
                waiter = cf.get_waiter('stack_create_complete')
                print("...waiting for stack to be ready...")
                waiter.wait(StackName=stack_name)
            except Exception as ex:
                print(ex)
                print("""
                There was an error creating your stack. Please go to CloudFormation in your 
                AWS console, click on the stack you created, resolve any errors, delete the stack
                and try again.

                You are seeing this error because your stack failed to create, when stacks fail
                to create they are put into a terminal ROLLBACK_COMPLETE state and the stack cannot
                be recovered because they have no previous state to roll back to.
                """)
                exit(1)

    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(json.dumps(
            cf.describe_stacks(StackName=stack_result['StackId']),
            indent=2,
            default=json_serial
        ))


def _parse_template(template, variables=None):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()

    if variables is not None:
        template_data = pystache.render(template_data, variables)
    print(template_data)
    cf.validate_template(TemplateBody=template_data)
    return template_data


def _parse_parameters(parameters):
    with open(parameters) as parameter_fileobj:
        parameter_data = json.load(parameter_fileobj)
    return parameter_data


def _stack_exists(stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
