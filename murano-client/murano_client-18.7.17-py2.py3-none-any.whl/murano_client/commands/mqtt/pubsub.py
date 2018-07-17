# pylint: disable=C0325,C0103,C0111,W1202
from __future__ import print_function
import threading
import logging
import time
from sys import stdin
from murano_client.commands.mqtt import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

LOG = logging.getLogger('GDC.MQTT.pubsub')

class ExoCommand(ExositeConnection):
    """Pipe streaming data to a Murano resource while simultaneously
    subscribing to the devices resources.

  usage:
    pubsub <topic> [options]

  options:
    -h --help                   Show this screen.
    <topic>                     Mqtt topic to publish to Murano resource.

    """
    Name = 'pubsub'
    def execute(self):
        from murano_client.ini import Device
        from murano_client.mqtt import MuranoMQTT

        subtimeout = float(self.global_args.get('--timeout') or 0)

        if self.global_args.get('--file'):
            mqtt_client = Device(self.global_args.get('--file'))
        else:
            mqtt_client = MuranoMQTT(**build_api_opts_from_docopt_args(self.global_args))

        mqtt_client.start()

        Qos = 1
        if self.global_args.get('--qos'):
            Qos = int(self.global_args.get('--qos'))

        topic = self.args.get('<topic>')
        LOG.debug("Publishing to topic: {}".format(topic))
        def pub():
            def read_stdin():
                readline = stdin.readline()
                while readline:
                    yield readline
                    readline = stdin.readline()
            rough_count = 0
            for line in read_stdin():
                payload = line.strip()
                LOG.debug("PAYLOAD: {}".format(payload))
                mqtt_client.publish(
                    topic,
                    payload,
                    qos=Qos
                )
                rough_count += 1
                LOG.debug("connected: {} - {}"
                          .format(mqtt_client.connected(), mqtt_client.duration_connected()))
        pubthread = threading.Thread(target=pub, name='PublishThread')
        pubthread.setDaemon(True)

        def on_message(client, userdata, msg):
            """ Override default on_message function. """
            _, resource, timestamp = msg.topic.split('/')[0:3]
            print("{}.{}={}".format(resource, timestamp, msg.payload))
        mqtt_client.on_message = on_message
        try:
            pubthread.start()
            start = time.time()
            while True:
                mqtt_client.loop()
                if time.time() - start >= subtimeout and subtimeout:
                    break
        except KeyboardInterrupt:
            pass

