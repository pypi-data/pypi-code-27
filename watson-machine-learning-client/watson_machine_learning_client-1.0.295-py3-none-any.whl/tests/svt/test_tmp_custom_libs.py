import unittest
import datetime
from preparation_and_cleaning import *
from models_preparation import *
from watson_machine_learning_client.log_util import get_logger


class TestCustomLibraries(unittest.TestCase):
    custom_library_uid = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestCustomLibraries.logger.info("Service Instance: setting up credentials")
        self.wml_credentials = get_wml_credentials()
        self.client = get_client()
        self.custom_library_path = os.path.join(os.getcwd(), 'artifacts', 'scikit_xgboost_model.tar.gz') # TODO

    def test_1_service_instance_details(self):
        TestCustomLibraries.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        TestCustomLibraries.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()

        TestCustomLibraries.logger.debug(details)
        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_2_create_custom_library(self):
        TestCustomLibraries.custom_library_uid = self.client.runtime_specs._create_custom_library({
            "name": "libraries_custom",
            "description": "custom libraries for scoring",
            "filepath": self.custom_library_path,
            "version": "1.0",
            "platform": {"name": "python", "version": ["3.5"]}
        })

        self.assertTrue(TestCustomLibraries.custom_library_uid is not None)

    def test_3_delete_custom_library(self):
        self.client.runtime_specs.delete_custom_library(TestCustomLibraries.custom_library_uid)


if __name__ == '__main__':
    unittest.main()
