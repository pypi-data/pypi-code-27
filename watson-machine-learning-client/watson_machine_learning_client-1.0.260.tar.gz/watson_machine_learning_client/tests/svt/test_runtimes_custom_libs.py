import unittest
import datetime
from preparation_and_cleaning import *
from models_preparation import *
from watson_machine_learning_client.log_util import get_logger
from watson_machine_learning_client.runtime_specs import CustomLibraryDefinition


class TestRuntimeSpec(unittest.TestCase):
    runtime_uid = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestRuntimeSpec.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()
        self.custom_library_path = os.path.join(os.getcwd(), 'artifacts', 'scikit_xgboost_model.tar.gz') # TODO

    def test_1_service_instance_details(self):
        TestRuntimeSpec.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        TestRuntimeSpec.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()

        TestRuntimeSpec.logger.debug(details)
        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_2_create_runtime(self):
        custom_library_uid = self.client.runtime_specs._create_custom_library({
            "name": "libraries_custom",
            "description": "custom libraries for scoring",
            "filepath": self.custom_library_path,
            "version": "1.0",
            "platform": {"name": "python", "versions": ["3.5"]}
        }, None)

        meta = {
            self.client.runtime_specs.ConfigurationMetaNames.NAME: "runtime_spec_python_3.5",
            self.client.runtime_specs.ConfigurationMetaNames.DESCRIPTION: "test",
            self.client.runtime_specs.ConfigurationMetaNames.PLATFORM: {
                "name": "python",
                "version": "3.5"
            },
            self.client.runtime_specs.ConfigurationMetaNames.CUSTOM_LIBRARIES_DEFINITIONS: [
                CustomLibraryDefinition(
                    "my_lib",
                    "1.0",
                    self.custom_library_path,
                    description="t",
                    platform={"name": "python", "versions": ["3.5"]}
                ),
                CustomLibraryDefinition(
                    "my_lib",
                    "1.1",
                    self.custom_library_path
                )
            ],
            self.client.runtime_specs.ConfigurationMetaNames.CUSTOM_LIBRARIES_UIDS: [custom_library_uid]
        }
        runtime_details = self.client.runtime_specs.create(meta)
        TestRuntimeSpec.runtime_uid = self.client.runtime_specs.get_uid(runtime_details)
        runtime_url = self.client.runtime_specs.get_url(runtime_details)

        self.assertTrue(TestRuntimeSpec.runtime_uid is not None)

    def test_3_get_details(self):
        print(self.client.runtime_specs.get_details(TestRuntimeSpec.runtime_uid))

        print(self.client.runtime_specs.get_details())

    def test_4_list(self):
        self.client.runtime_specs.list()

    def test_5_list_custom_libs(self):
        self.client.runtime_specs.list_custom_libraries(TestRuntimeSpec.runtime_uid)
        self.client.runtime_specs.list_custom_libraries()

    def test_6_list_runtimes_for_libraries(self):
        self.client.runtime_specs._list_runtime_specs_for_libraries()

    def test_7_delete_runtime(self):
        self.client.runtime_specs.delete(TestRuntimeSpec.runtime_uid, autoremove=True)


if __name__ == '__main__':
    unittest.main()
