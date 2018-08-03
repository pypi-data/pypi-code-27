import sys
import unittest

import config
import model

sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, 'middleware-clone/lib')
sys.path.insert(1, 'middleware-clone')
import dev_appserver

dev_appserver.fix_sys_path()
from google.appengine.ext import testbed


class BaseTestCase(unittest.TestCase):
    user = model.ActiveDirectoryUser.find(email="yulia-knubisoft@octopuslabs.com")[0]

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        config.initialize()
        self.maxDiff = None
        self.testbed.setup_env(
            app_id='octopus-portal-apps',
            my_config_setting='config.py',
            overwrite=True)
        # [END setup]

    def tearDown(self):
        self.testbed.deactivate()
