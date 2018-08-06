import json
import logging

import boto3


logger = logging.getLogger("sqs")


class SQSMessageProducer:

    def __init__(self, region, access_key, secret_key, queue_name):
        self.client = boto3.client(
            "sqs",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.queue_url = self.client.get_queue_url(QueueName=queue_name)["QueueUrl"]

    def __call__(self):

        while True:
            messages = self.client.receive_message(
                QueueUrl=self.queue_url,
                WaitTimeSeconds=20,
                MaxNumberOfMessages=10
            )

            logger.info("Number of messages received. %s" % len(messages.get("Messages", [])))

            messages = {x["MessageId"]: x for x in messages.get("Messages", [])}.values()
            for message in messages:
                body = json.loads(message["Body"])
                try:
                    yield body
                finally:
                    self.client.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
