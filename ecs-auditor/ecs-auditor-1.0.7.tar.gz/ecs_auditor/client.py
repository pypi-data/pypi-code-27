'''
ECS Auditor class to get the current image and param version for all ECS Services
'''
import json
from collections import OrderedDict
from jsondiff import diff
import ecs_auditor.config as config
from ecs_auditor.helpers.github_helper import GithubHelper
from ecs_auditor.helpers.ecs_helper import EcsHelper
from ecs_auditor.helpers.ssm_helper import SsmHelper
from ecs_auditor.helpers.excel_helper import ExcelHelper
from ecs_auditor.lib import base

class Client(object):
    """docstring for Main.
    """

    def __init__(self, config_file_path, region, output, env, services, ignore_author, show_differences_only):
        """Initializer

        Args:
            region (str):   AWS Region
            output (str):   Preferred output style
            env (str):      ECS Cluster environment

        Returns:
            N/A

        """
        super(Client, self).__init__()
        self.config_file_path = config_file_path
        self.region = region
        self.output = output
        self.env = env
        self.ignore_author = ignore_author
        self.services = services
        self.diff_mode = show_differences_only

    def perform(self):
        for cluster in config.settings['clusters']:
            if (self.region != 'all' and self.region != cluster['region']) or (self.env != 'all' and self.env != cluster['env']):
                continue

            print "*--------------------------------*"
            print "Getting data for {} {}".format(cluster['region'], cluster['env'])
            print "*--------------------------------*"

            ecs = EcsHelper(cluster['region'])
            ssm = SsmHelper(cluster['region'])
            cluster['services'] = []
            services = []
            task_definitions = []
            service_list_arns = ecs.list_services(cluster['name'], [], '')

            for service_chunk in [service_list_arns[i:i + 10] for i in xrange(0, len(service_list_arns), 10)]:
                for service in ecs.client.describe_services(cluster=cluster['name'], services=service_chunk)['services']:
                    name = "_".join((service['serviceName'].split('-')[3:-4]))
                    if self.services is not '' and name in self.services.split(','):
                        services.append(service)
                    elif self.services is '':
                        services.append(service)

            for service in services:
                task_definitions.append(ecs.client.describe_task_definition(
                    taskDefinition=service['taskDefinition']
                ))

            for task_definition in task_definitions:
                dict_ordered = None
                for containerDefinition in task_definition['taskDefinition']['containerDefinitions']:
                    for param in containerDefinition['environment']:
                        if param['name'] == "VERSION" or param['name'] == "PARAM_VERSION":
                            dict_ordered = None
                            image_tag = containerDefinition['image'].split(':')[-1]
                            regionEnv = "{}.{}".format(base.get_landscape(cluster['region']), base.get_environment(cluster['env']))
                            print containerDefinition['name']

                            author = ssm.get_author(regionEnv, containerDefinition['name'], param['value'])

                            try:
                                author = ("".join(author).split('/')[-1:])[0]
                            except Exception as e:
                                author = None
                            github = GithubHelper().get_param_version_data(containerDefinition['name'], base.get_landscape(cluster['region']), base.get_environment(cluster['env']))
                            version = regionEnv + "." + containerDefinition['name'].replace('-', '_') + "." + param['value']
                            ssm_version = ssm.get_param(version)

                            diff_output = diff(ssm_version, github['params'])

                            if self.diff_mode is True and author != self.ignore_author and (len(diff_output) > 0 or param['value'] != github['version'] or author != 'codeship_param_pusher'):
                                dict_ordered = OrderedDict([('name', containerDefinition['name']), ('region', regionEnv), ('image_tag', image_tag), ('running_param_version', param['value']), ('github_param_version', github['version']), ('author', author), ('diff', diff_output)])
                                break
                            elif self.diff_mode is False and author != self.ignore_author:
                                dict_ordered = OrderedDict([('name', containerDefinition['name']), ('region', regionEnv), ('image_tag', image_tag), ('running_param_version', param['value']), ('github_param_version', github['version']), ('author', author), ('diff', diff_output)])
                                break

                if dict_ordered is not None: cluster['services'].append(dict_ordered)

            print "\n\n"

        self.output_data()

    def output_data(self):
        if self.output == 'excel':
            ExcelHelper().create(config.settings['clusters'])
            return None

        for cluster in config.settings['clusters']:
            if 'services' not in cluster: continue

            print "*--------------------------------*"
            print "Output for {} {}".format(cluster['region'], cluster['env'])
            print "*--------------------------------*"

            if self.output == "json":
                print json.dumps(cluster['services'], indent=4)
            elif self.output == "pretty":
                for service in cluster['services']:
                    print service['name']
                    print "---> PARAM_VERSION: {}, IMAGE_TAG: {}, AUTHOR: {}".format(service['running_param_version'], service['image_tag'], service['author'])
                    print "---> GITHUB_VERSION: {}".format(service['github_param_version'])
                    print "---> DIFF"
                    print service['diff']
                    print "\n"
            elif self.output == "compare":
                compare = {}
                for service in cluster['services']:
                    if self.ignore_author not in service['author']:
                        regionEnv = "{}-{}".format(base.get_landscape(cluster['region']), cluster['env'])
                        if service['name'] not in compare:
                            compare["{}".format(service['name'])] = {}
                        compare[service['name']][regionEnv] = {'image_tag': service['image_tag'], 'running_param_version': service['param_version'], 'author': service['author']}
                print json.dumps(compare, indent=4, sort_keys=True)
