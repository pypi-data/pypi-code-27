import unittest
import datetime
from preparation_and_cleaning import *
from models_preparation import *
from watson_machine_learning_client.log_util import get_logger


class TestRuntimeSpec(unittest.TestCase):
    runtime_uid = None
    runtime_url = None
    model_uid = None
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
                {
                    "name": "my_lib",
                    "description": "t",
                    "filepath": self.custom_library_path,
                    "version": "1.0",
                    "platform": {"name": "python", "versions": ["3.5"]}
                },
                {
                    "name": "my_lib",
                    "filepath": self.custom_library_path,
                    "version": "1.1",
                    "platform": {"name": "python", "versions": ["3.5"]}
                }
            ],
            self.client.runtime_specs.ConfigurationMetaNames.CUSTOM_LIBRARIES_UIDS: [custom_library_uid]
        }
        runtime_details = self.client.runtime_specs.create(meta)
        TestRuntimeSpec.runtime_uid = self.client.runtime_specs.get_uid(runtime_details)
        TestRuntimeSpec.runtime_url = self.client.runtime_specs.get_url(runtime_details)

        self.assertTrue(TestRuntimeSpec.runtime_uid is not None)

    def test_3_publish_model(self):
        TestRuntimeSpec.logger.info("Creating scikit-learn model ...")

        model_data = create_scikit_learn_model_data()
        predicted = model_data['prediction']

        TestRuntimeSpec.logger.debug(predicted)
        self.assertIsNotNone(predicted)

        self.logger.info("Publishing scikit-learn model ...")

        self.client.repository.ModelMetaNames.show()

        model_props = {self.client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                       self.client.repository.ModelMetaNames.RUNTIME_URL: TestRuntimeSpec.runtime_url,
                       self.client.repository.ModelMetaNames.NAME: "LOCALLY created Digits prediction model",
                       self.client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: {},
                       self.client.repository.ModelMetaNames.EVALUATION_METHOD: "multiclass",
                       self.client.repository.ModelMetaNames.EVALUATION_METRICS: [
                           {
                               "name": "accuracy",
                               "value": 0.64,
                               "threshold": 0.8
                           }
                       ]
                       }
        published_model_details = self.client.repository.store_model(model=model_data['model'], meta_props=model_props, training_data=model_data['training_data'], training_target=model_data['training_target'])
        TestRuntimeSpec.model_uid = self.client.repository.get_model_uid(published_model_details)
        TestRuntimeSpec.model_url = self.client.repository.get_model_url(published_model_details)
        self.logger.info("Published model ID:" + str(TestRuntimeSpec.model_uid))
        self.logger.info("Published model URL:" + str(TestRuntimeSpec.model_url))
        self.assertIsNotNone(TestRuntimeSpec.model_uid)
        self.assertIsNotNone(TestRuntimeSpec.model_url)

    def test_4_get_details(self):
        details = self.client.repository.get_details(TestRuntimeSpec.model_uid)
        runtime_url = self.client.runtime_specs.get_url(details)

        self.assertTrue(runtime_url == TestRuntimeSpec.runtime_url)

    def test_5_delete_model(self):
        self.client.repository.delete(TestRuntimeSpec.model_uid)

    def test_6_delete_runtime(self):
        self.client.runtime_specs.delete(TestRuntimeSpec.runtime_uid, autoremove=True)


if __name__ == '__main__':
    unittest.main()
