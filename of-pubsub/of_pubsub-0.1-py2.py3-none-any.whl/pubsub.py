# this library encapsulates a pubsub system.  The example here uses AWS SNS, but the idea is that the interface is generic enough to
# just change this one file when interfacing to a new system (we'll wait for that to add multiple drivers)

import boto3
import os
import logging
import threading
import random
import string
import json

class PubSub:
    
    def __init__(self, driver, **kw_args):
        assert "AWS" == driver, "Unsupported driver: %s, supported drivers must be one of ['AWS']" % driver
        self.topic_arn = kw_args['topic_arn']
        self.region_name = self.topic_arn.split(':')[3]
        self.sns_client = boto3.client('sns', region_name = self.region_name)
        self.sqs_client = boto3.resource('sqs', region_name = self.region_name)
        self.logger = kw_args.get('logger', logging.getLogger(__name__))
        return
    
    def subscribe(self, channel, callback):
        """ subscribe take a channel and a callback.  The callback is called with messages that come back """
        self._stop = False
        self.queue_name = 'PS_SUB_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        self.polling_thread = threading.Thread(target=self.polling_thread_function)
        self.callback = callback
        self.queue = self.sqs_client.create_queue(QueueName = self.queue_name)

        # hack ahead, see: https://forums.aws.amazon.com/thread.jspa?threadID=223798

        self.queue.add_permission(Label='Public_send_permission',
                                  AWSAccountIds = [self.queue.attributes['QueueArn'].split(':')[4]],
                                  Actions = ['SendMessage'])
        policy = json.loads(self.queue.attributes['Policy'])
        new_policy = policy
        new_policy['Statement'][0]['Principal'] = '*'
        self.queue.set_attributes(Attributes={'Policy': json.dumps(new_policy)})

        subscription = self.sns_client.subscribe(
            TopicArn = self.topic_arn,
            Protocol = 'sqs',
            Endpoint = self.queue.attributes['QueueArn'],
            Attributes = {"FilterPolicy" : json.dumps({"Channel": [channel]})})
        self.subscription_arn = subscription['SubscriptionArn']
        self.polling_thread.start()
        self.logger.info('set up subscriber')
        return

    def publish(self, channel, data):
        self.sns_client.publish(TopicArn = self.topic_arn, Message = json.dumps(data),
                                MessageAttributes = {"Channel": {"DataType": "String",
                                                                 "StringValue" : channel}})
        return
        
    def polling_thread_function(self):
        while not self._stop:
            self.logger.info('checking for queue events')
            for message in self.queue.receive_messages(WaitTimeSeconds=1):
                self.logger.info('got message on queue of %s' % message.body)
                try:
                    msg = json.loads(message.body)['Message']
                    self.logger.debug('got message of: %s' % msg)
                    self.callback(msg)
                    message.delete()
                except:
                    self.logger.exception('cannot print message %s' % message.body)

    def unsubscribe(self):
        self._stop = True
        self.sns_client.unsubscribe(SubscriptionArn = self.subscription_arn)
        self.subscription_arn = None
        self.queue.delete()
        self.queue = None
        self.polling_thread = None
        self.callback = None
        
