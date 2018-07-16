import boto3
import logging
import json

from eventcore import Consumer

log = logging.getLogger(__name__)


class SQSConsumer(Consumer):
    """
    Consume from a SQS queue.
    """

    def __init__(self, region_name, access_key_id, secret_access_key, url):
        sqs = boto3.resource('sqs',
                             region_name=region_name,
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key)
        self.queue = sqs.Queue(url)

    def consume(self):
        while True:
            for message in self.queue.receive_messages(MaxNumberOfMessages=10):
                try:
                    message_body = json.loads(message.body)
                    self.process_event(name=message_body.get('event'),
                                       subject=message_body.get('subject'),
                                       data=message_body.get('data'))
                    self.queue.delete_messages(Entries=[{
                        'Id': message.message_id,
                        'ReceiptHandle': message.receipt_handle
                    }])
                except:
                    log.error('@SQSConsumer.consume Exception:',
                              exc_info=True)
                    continue
