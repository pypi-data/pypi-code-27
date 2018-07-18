import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mqttclient import MQTTClient
from argaeus.controller.behavior.behavior import Behavior
from pelops.read_config import read_config, validate_config
import threading
import time


class Test_Behavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_Behavior")
        cls.logger.info("start")
        cls.mqtt_client = MQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        self.behavior_config = {
            "name": "button1",
            "topic-sub": "/test/button1",
            "command-active": "PRESSED",
            "behavior": "to-default-mode"
        }

    def tearDown(self):
        self.mqtt_client.unsubscribe_all()

    def test_0init(self):
        b = Behavior(self.behavior_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(b)

    def test_1method_direct_a(self):
        global counter
        counter = 0

        def method():
            global counter
            counter = counter + 1

        b = Behavior(self.behavior_config, self.mqtt_client, self.logger)
        b.response_methods.append(method)

        self.assertEqual(counter, 0)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter, 1)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter, 2)
        b._topic_handler("".encode("UTF-8"))
        self.assertEqual(counter, 2)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter, 3)
        b._topic_handler("PRESSED_".encode("UTF-8"))
        self.assertEqual(counter, 3)

    def test_2method_direct_b(self):
        global counter_a
        global counter_b
        counter_a = 0
        counter_b = 100

        def method_a():
            global counter_a
            counter_a = counter_a + 1

        def method_b():
            global counter_b
            counter_b = counter_b - 1

        b = Behavior(self.behavior_config, self.mqtt_client, self.logger)
        b.response_methods.append(method_a)
        b.response_methods.append(method_b)

        self.assertEqual(counter_a, 0)
        self.assertEqual(counter_b, 100-counter_a)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter_a, 1)
        self.assertEqual(counter_b, 100-counter_a)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter_a, 2)
        self.assertEqual(counter_b, 100-counter_a)
        b._topic_handler("".encode("UTF-8"))
        self.assertEqual(counter_a, 2)
        self.assertEqual(counter_b, 100-counter_a)
        b._topic_handler("PRESSED".encode("UTF-8"))
        self.assertEqual(counter_a, 3)
        self.assertEqual(counter_b, 100-counter_a)
        b._topic_handler("PRESSED_".encode("UTF-8"))
        self.assertEqual(counter_a, 3)
        self.assertEqual(counter_b, 100-counter_a)

    def test_3method_mqtt(self):
        method_invoked = threading.Event()
        method_invoked.clear()

        global counter
        counter = 10

        def method():
            global counter
            counter = counter + 2
            self.logger.info("test_3method_mqtt - methods resulting counter value: {}.".format(counter))
            method_invoked.set()

        b = Behavior(self.behavior_config, self.mqtt_client, self.logger)
        b.response_methods.append(method)

        b.start()

        self.assertEqual(counter, 10)
        self.mqtt_client.publish(b._topic_sub, "PRESSED")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 12)

        self.mqtt_client.publish(b._topic_sub, "PRESSED")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 14)

        self.mqtt_client.publish(b._topic_sub, "")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 14)

        self.mqtt_client.publish(b._topic_sub, "PRESSED")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 16)

        self.mqtt_client.publish(b._topic_sub, "pressed")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 16)

        time.sleep(1)
        b.stop()

        self.mqtt_client.publish(b._topic_sub, "PRESSED")
        method_invoked.wait(0.1)
        method_invoked.clear()
        self.assertEqual(counter, 16)


if __name__ == '__main__':
    unittest.main()
