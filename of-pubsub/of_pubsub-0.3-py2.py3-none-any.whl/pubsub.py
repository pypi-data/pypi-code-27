# this library encapsulates a pubsub system.  The example here uses AWS SNS, but the idea is that the interface is generic enough to
# just change this one file when interfacing to a new system (we'll wait for that to add multiple drivers)

import boto3
import os
import logging
import threading
import random
import string
import json
import time

class Subscription:
    def __init__(self, pubsub, channel, kwargs):
        self.pubsub = pubsub
        self.logger = pubsub.logger
        self.channel = channel
        self.queue_name = 'PS_SUB_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        self.queue = self.pubsub.sqs_client.create_queue(QueueName = self.queue_name)

        self.logger.info('created queue named: %s' % self.queue_name)
        # hack ahead, see: https://forums.aws.amazon.com/thread.jspa?threadID=223798

        self.queue.add_permission(Label='Public_send_permission',
                                  AWSAccountIds = [self.queue.attributes['QueueArn'].split(':')[4]],
                                  Actions = ['SendMessage'])
        policy = json.loads(self.queue.attributes['Policy'])
        new_policy = policy
        new_policy['Statement'][0]['Principal'] = '*'
        self.queue.set_attributes(Attributes={'Policy': json.dumps(new_policy)})

        subscription = self.pubsub.sns_client.subscribe(
            TopicArn = self.pubsub.topic_arn,
            Protocol = 'sqs',
            Endpoint = self.queue.attributes['QueueArn'],
            Attributes = {"FilterPolicy" : json.dumps({"Channel": [channel]})})
        self.subscription_arn = subscription['SubscriptionArn']
        self.callback = kwargs.get('callback', None)
        self.items = kwargs.get('items', None)
        self.polling_thread = threading.Thread(target=self.polling_thread_function)
        self.polling_thread.start()
        return

    def polling_thread_function(self):
        self._stop = False
        self.logger.info('starting polling thread function for channel %s' % self.channel)
        while not self._stop:
            self.logger.info('checking for queue events on channel: %s' % self.channel)
            for message in  self.queue.receive_messages(WaitTimeSeconds=1):
                self.logger.info('got message on channel %s queue of %s' % (self.channel, message.body))
                msg = json.loads(message.body)['Message']
                if self.items is not None:
                    self.items.append(msg)
                if self.callback:
                    try:
                        self.callback(msg)
                    except:
                        self.logger.exception('error processing message %s' % message)
                message.delete()
        self.logger.info('exiting polling thread function for channel %s' % self.channel)
        return
    
    def unsubscribe(self):
        self.logger.info('in unsubscribe to channel %s' % self.channel)
        self._stop = True
        self.pubsub.sns_client.unsubscribe(SubscriptionArn = self.subscription_arn)
        self.subscription_arn = None
        self.logger.info('deleting queue name %s' % self.queue_name)
        self.queue.delete()
        self.queue = None
        self.polling_thread = None
        self.callback = None

    def __repr__(self):
        return "<Subscription: channel=%s at 0x%02x>" % (self.channel, id(self))

class PubSub:
    def __init__(self, driver, **kw_args):
        assert "AWS" == driver, "Unsupported driver: %s, supported drivers must be one of ['AWS']" % driver
        self.topic_arn = kw_args['topic_arn']
        self.region_name = self.topic_arn.split(':')[3]
        self.sns_client = boto3.client('sns', region_name = self.region_name)
        self.sqs_client = boto3.resource('sqs', region_name = self.region_name)
        self.logger = kw_args.get('logger', logging.getLogger(__name__))
        return
    
    def subscribe(self, channel, **kwargs):
        """ subscribe take a channel and either callback or an item array.  The callback is called with messages that come back """
        return Subscription(self, channel, kwargs)

    def publish(self, channel, data):
        self.logger.info('publishing %s to %s' % (data, channel))
        self.sns_client.publish(TopicArn = self.topic_arn, Message = json.dumps(data),
                                MessageAttributes = {"Channel": {"DataType": "String",
                                                                 "StringValue" : channel}})
        return

        
