import logging
import os

from vat_utils.config import create_config_client_v2

from build_utils.rules import base_rule

logger = logging.getLogger(__name__)

class GetPassthroughConfig(base_rule.BaseRule):
    def run(self):
        old_working_directory = os.getcwd()
        try:
            os.chdir(self.dir_path)

            config_source = self.build_context.get_rule_config_value('passthrough_config_source')
            config_client = create_config_client_v2(config_source)
            return config_client.get_root_json_value()
        finally:
            os.chdir(old_working_directory)
