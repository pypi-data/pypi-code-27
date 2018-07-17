# pylint: disable=C0325,C0103,C0111
import logging
import time
from murano_client.commands.mqtt import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

LOG = logging.getLogger('GDC.MQTT.sub')

class ExoCommand(ExositeConnection):
    """Subscribe to Murano device using the MQTT protocol.

  usage:
    subscribe [options]

  options:
    -h --help                   Show this screen.

    """
    Name = 'subscribe'
    def execute(self):
        from murano_client.ini import Device
        from murano_client.mqtt import MuranoMQTT

        subtimeout = float(self.global_args.get('--timeout') or 0)

        if self.global_args.get('--file'):
            mqtt_client = Device(self.global_args.get('--file'))
        else:
            mqtt_client = MuranoMQTT(**build_api_opts_from_docopt_args(self.global_args))

        def on_message(client, userdata, msg):
            _, resource, timestamp = msg.topic.split('/')[0:3]
            print("{}.{}={}".format(resource, timestamp, msg.payload.decode()))
        mqtt_client.on_message = on_message

        mqtt_client.start()

        try:
            start = time.time()
            while True:
                mqtt_client.loop()
                if time.time() - start >= subtimeout and subtimeout:
                    break
        except KeyboardInterrupt:
            pass
