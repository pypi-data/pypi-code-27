import unittest
from watson_machine_learning_client.log_util import get_logger
from preparation_and_cleaning import *
from models_preparation import *
import psycopg2

postgres_connection = {
    "type": "postgresql",
    "database": "compose",
    "user": "admin",
    "password": "JIILAWZGGFYLJZOH",
    "host": "sl-us-south-1-portal.21.dblayer.com",
    "port": "42618",
    "tablename": "spark_mllib_payload_logging_test_table"
}



class TestAIFunction(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    scoring_url = None
    labels = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestAIFunction.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()

        self.function_name = 'ai function'
        self.deployment_name = 'deployment name'

    def test_00_check_client_version(self):
        TestAIFunction.logger.info("Check client version...")

        self.logger.info("Getting version ...")
        version = self.client.version
        TestAIFunction.logger.debug(version)
        self.assertTrue(len(version) > 0)

    def test_01_service_instance_details(self):
        TestAIFunction.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        self.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()
        TestAIFunction.logger.debug(details)

        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_02_publish_ai_function(self):
        function_props = {
            self.client.repository.FunctionMetaNames.NAME: TestAIFunction.function_name,
            self.client.repository.FunctionMetaNames.DESCRIPTION: 'desc',
            self.client.repository.FunctionMetaNames.TAGS: [
                {"value": "ProjectA", "description": "Functions created for ProjectA"}
            ]
        }

        def score(payload):
            return {
                'fields': ["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION", "prediction", "probability"],
                'values': [["M", 23, "Single", "Student", 1, 0.2], ["M", 55, "Single", "Executive", 2, 0.2]]
            }

        ai_function_details = self.client.repository.store_function(score, function_props)

        TestAIFunction.function_uid = self.client.repository.get_function_uid(ai_function_details)
        function_url = self.client.repository.get_function_url(ai_function_details)
        TestAIFunction.logger.info("AI function ID:" + str(TestAIFunction.function_uid))
        TestAIFunction.logger.info("AI function URL:" + str(function_url))
        self.assertIsNotNone(TestAIFunction.function_uid)
        self.assertIsNotNone(function_url)

    def test_03_download_ai_function_content(self):
        try:
            os.remove('test_ai_function.tar.gz')
        except:
            pass

        self.client.repository.download(TestAIFunction.function_uid, filename='test_ai_function.tar.gz')

        try:
            os.remove('test_ai_function.tar.gz')
        except:
            pass

    def test_04_get_details(self):
        details = self.client.repository.get_function_details()
        self.assertTrue(self.function_name in str(details))

        details = self.client.repository.get_function_details(self.function_uid)
        self.assertTrue(self.function_name in str(details))

        details = self.client.repository.get_details()
        self.assertTrue("functions" in details)

        details = self.client.repository.get_details(self.function_uid)
        self.assertTrue(self.function_name in str(details))

    def test_05_list(self):
        self.client.repository.list()

        self.client.repository.list_functions()

    def test_06_create_deployment(self):
        TestAIFunction.logger.info("Create deployment")
        deployment = self.client.deployments.create(artifact_uid=self.function_uid, name=self.deployment_name, asynchronous=False)
        TestAIFunction.logger.debug("Online deployment: " + str(deployment))
        TestAIFunction.scoring_url = self.client.deployments.get_scoring_url(deployment)
        TestAIFunction.logger.debug("Scoring url: {}".format(TestAIFunction.scoring_url))
        TestAIFunction.deployment_uid = self.client.deployments.get_uid(deployment)
        TestAIFunction.logger.debug("Deployment uid: {}".format(TestAIFunction.deployment_uid))
        self.assertTrue("online" in str(deployment))

    def test_07_enable_payload_logging(self):
        TestAIFunction.logger.info("Setup payload logging")
        payload_logging_configuration = {
            self.client.deployments.PayloadLoggingMetaNames.PAYLOAD_DATA_REFERENCE: {
                "type": postgres_connection['type'],
                "location": {
                    "tablename": postgres_connection['tablename']
                },
                "connection": {
                    "uri": "postgres://{}:{}@{}:{}/{}".format(
                        postgres_connection['user'],
                        postgres_connection['password'],
                        postgres_connection['host'],
                        postgres_connection['port'],
                        postgres_connection['database']
                    )
                }
            }
        }

        self.client.deployments.setup_payload_logging(TestAIFunction.deployment_uid, payload_logging_configuration)

    def test_08_get_payload_logging_details(self):
        payload_logging_details = self.client.deployments.get_payload_logging_details(TestAIFunction.deployment_uid)
        self.assertTrue(payload_logging_details is not None)

    def test_09_get_deployment_details(self):
        TestAIFunction.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details()
        self.assertTrue(self.deployment_name in str(deployment_details))

    def test_10_clean_db(self):
        conn = psycopg2.connect(
            database=postgres_connection['database'],
            user=postgres_connection['user'],
            password=postgres_connection['password'],
            host=postgres_connection['host'],
            port=postgres_connection['port']
        )
        cur = conn.cursor()
        cur.execute("DELETE from " + postgres_connection['tablename'] + ";")
        conn.commit()
        print("Total number of rows deleted :", cur.rowcount)
        cur.execute("SELECT * from " + postgres_connection['tablename'])
        rows = cur.fetchall()

        conn.close()

        self.assertTrue(len(rows) == 0)

    def test_11_score(self):
        TestAIFunction.logger.info("Score the model")
        scoring_data = {"fields": ["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"], "values": [["M", 23, "Single", "Student"], ["M", 55, "Single", "Executive"]]}
        predictions = self.client.deployments.score(TestAIFunction.scoring_url, scoring_data)
        TestAIFunction.logger.debug("Predictions: {}".format(predictions))
        self.assertTrue("prediction" in str(predictions))

    def test_12_check_db_content(self):
        conn = psycopg2.connect(
            database=postgres_connection['database'],
            user=postgres_connection['user'],
            password=postgres_connection['password'],
            host=postgres_connection['host'],
            port=postgres_connection['port']
        )
        cur = conn.cursor()
        cur.execute("SELECT * from " + postgres_connection['tablename'])
        rows = cur.fetchall()
        for row in rows:
            print("ID = ", row, "\n")

        conn.close()

        self.assertTrue(len(rows) == 2)

    def test_13_delete_payload_logging(self):
        self.client.deployments.delete_payload_logging(TestAIFunction.deployment_uid)

    def test_14_delete_deployment(self):
        TestAIFunction.logger.info("Delete deployment")
        self.client.deployments.delete(TestAIFunction.deployment_uid)

    def test_15_delete_runtime(self):
        TestAIFunction.logger.info("Delete runtime")
        self.client.runtimes.delete(
            self.client.runtimes.get_uid(
                self.client.repository.get_details(TestAIFunction.function_uid)
            )
        )

    def test_16_delete_function(self):
        TestAIFunction.logger.info("Delete function")
        self.client.repository.delete(TestAIFunction.function_uid)


if __name__ == '__main__':
    unittest.main()
