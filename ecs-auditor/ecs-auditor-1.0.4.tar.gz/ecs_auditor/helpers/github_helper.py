'''
Github Helper class to provide an interface with Github api
'''
from github import Github as GithubExternal
import base64
import yaml
from ansible_vault import Vault
import ecs_auditor.config as config

class GithubHelper(object):
    """docstring for Github.
    """

    def __init__(self):
        """Initializer

        Args:
            N/A

        Returns:
            N/A

        """
        super(GithubHelper, self).__init__()
        self.client = GithubExternal(config.settings['common']['gh_access_token'])
        self.organization = self.client.get_organization(config.settings['common']['gh_org'])

    def get_param_version_data(self, app_name, landscape, environment):
        """Retrieves the content of the vault and playbook file

        Args:
            app_name (str): the name of the application
            landscape (str): the landscape where the application is
            environment (str): the environment of the application

        Returns:
            String

        """
        data = {}
        rtn = {'version': 'NOT FOUND', 'params': {}}

        repo = self.organization.get_repo(config.settings['common']['gh_repo'])
        file_name = app_name.replace('-', '_')

        file_options = [
            "{}/{}/{}".format(file_name, environment, landscape.upper()),
            "{}/{}/{}".format(file_name, environment, landscape)
        ]

        for option in file_options:
            try:
                files = repo.get_file_contents(option)
                for file_path in files:
                    if "vault" in file_path.path:
                        data['vault'] = repo.get_file_contents(file_path.path).content
                    else:
                        data['content'] = repo.get_file_contents(file_path.path).content
                break
            except Exception as e:
                pass

        if 'content' in data:
            content = yaml.load(base64.b64decode(data['content']))
            rtn['version'] = content[0]['tasks'][1]['param_pusher']['version']
            rtn['params'] = self.combine_vault_with_playbook(data, content)

        return rtn

    def combine_vault_with_playbook(self, data, content):
        """Combines the vault data with the playbook data

        Args:
            data (dict)
            content (dict)

        Returns:
            dict

        """
        vault = Vault(config.settings['common']['vault_enc_key'])
        secrets = vault.load(base64.b64decode(data['vault']))

        for k, v in content[0]['tasks'][1]['param_pusher']['parameters'].iteritems():
            if ('VAULT' in v) and (k in content[0]['tasks'][1]['param_pusher']['parameters']):
                if "VAULT_{}".format(k) in secrets:
                    content[0]['tasks'][1]['param_pusher']['parameters'][k] = secrets["VAULT_" + k]
                else:
                    content[0]['tasks'][1]['param_pusher']['parameters'][k] = "KEY NAME MISMATCH"

        return content[0]['tasks'][1]['param_pusher']['parameters']
