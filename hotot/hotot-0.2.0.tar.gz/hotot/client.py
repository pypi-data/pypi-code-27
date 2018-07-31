import sys
import time
import uuid
import json
import pika
import datetime

import logging

logging.getLogger('pika').setLevel(logging.INFO)

class BaseClient(object):
    def __init__(self, host, exchange = '', header = {}, timeout=60, connection_attempts=100):
        self.timeout    = timeout
        self.exchange   = exchange
        self.header     = header
        self.response   = None

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                connection_attempts=connection_attempts,
                retry_delay=5,
        ))

        print(str(datetime.datetime.now()) + ' Connected!')               

        self.channel = self.connection.channel()

    def _publish(self, routing_key, props, mandatory=False, **kwargs):
        return self.channel.basic_publish(
                exchange=self.exchange, 
                routing_key=routing_key, 
                properties=pika.BasicProperties(**{
                    **props,
                    **{
                        'content_type': 'application/json',
                        'delivery_mode': 1
                    }
                }),
                mandatory=mandatory,
                body=json.dumps({**self.header, **kwargs}))

    def exit(self):
        self.channel.stop_consuming()
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()


class ConsumerClient(BaseClient):
    def __init__(self, host, exchange='', queue='', routing_key=None, exclusive=False, durable=False, **kwargs):
        super().__init__(host, exchange, **kwargs)
        self.queue = queue
        self.channel.exchange_declare(exchange)
        result = self.channel.queue_declare(queue=self.queue, exclusive=exclusive, durable=durable)
        self.channel.queue_bind(exchange=self.exchange, queue=result.method.queue, routing_key=routing_key)
        
    def consume(self, callback):
        self.channel.basic_consume(callback, queue=self.queue)
        self.channel.start_consuming()

class RpcClient(BaseClient):
    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def _wait(self, frequency=0):
        t_end = time.time() + self.timeout
        while self.response is None:
            time.sleep(frequency)
            if time.time() > t_end:
                break
            self.connection.process_data_events()
        return self.response

    def call(self, routing_key, **kwargs):
        self.response = None
        if not hasattr(self, 'callback_queue'):
            result = self.channel.queue_declare(exclusive=True)
            self.callback_queue = result.method.queue
            self.channel.basic_consume(self._on_response, no_ack=True,
                            queue=self.callback_queue)

        self.corr_id = str(uuid.uuid4())
        self._publish(routing_key, 
            { 'reply_to': self.callback_queue, 'correlation_id' : self.corr_id }, 
            **kwargs)
        return self._wait()

    def send(self, routing_key, **kwargs):
        return self._publish(routing_key, {}, **kwargs)




