import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from argaeus.controller.behavior.behaviorcontroller import BehaviorController
from pelops.mylogger import create_logger
from pelops.mqttclient import MQTTClient
from argaeus.controller.behavior.behaviortypes import BehaviorTypes
from pelops.read_config import read_config, validate_config
import random
import time


class Test_BehaviorController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_BehaviorController")
        cls.logger.info("start")
        cls.mqtt_client = MQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        self.behaviorcontroller_config = [
            {
                "name": "button1",
                "topic-sub": "/test/button1",
                "command-active": "PRESSED",
                "behavior": "to-default-mode"
            },
            {
                "name": "button2",
                "topic-sub": "/test/button2",
                "command-active": "PRESSED",
                "behavior": "Toggle-Active-Passive"
            },
            {
                "name": "button3",
                "topic-sub": "/test/button3",
                "command-active": "PRESSED",
                "behavior": "RESET-TO-DEFAULT-TEMP"
            }
        ]

    def tearDown(self):
        self.mqtt_client.unsubscribe_all()

    def test_0init(self):
        bc = BehaviorController(self.behaviorcontroller_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(bc)
        self.assertEqual(len(bc._behaviors), 3)
        self.assertIn(BehaviorTypes.ResetToDefaultTemp, list(bc._behaviors.keys()))
        self.assertIn(BehaviorTypes.ToggleActivePassive, list(bc._behaviors.keys()))
        self.assertIn(BehaviorTypes.ToDefaultMode, list(bc._behaviors.keys()))

    def test_1add_response_methods(self):
        def a():
            pass

        def b():
            pass

        def c():
            pass

        del self.behaviorcontroller_config[2]

        bc = BehaviorController(self.behaviorcontroller_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(bc)
        self.assertEqual(len(bc._behaviors), 2)
        self.assertNotIn(BehaviorTypes.ResetToDefaultTemp, list(bc._behaviors.keys()))
        self.assertIn(BehaviorTypes.ToggleActivePassive, list(bc._behaviors.keys()))
        self.assertIn(BehaviorTypes.ToDefaultMode, list(bc._behaviors.keys()))

        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToggleActivePassive][0].response_methods), 0)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods), 0)

        bc.add_response_method(BehaviorTypes.ToggleActivePassive, a)
        bc.add_response_method(BehaviorTypes.ToggleActivePassive, b)
        bc.add_response_method(BehaviorTypes.ToggleActivePassive, c)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToggleActivePassive][0].response_methods), 3)
        self.assertIn(a, list(bc._behaviors[BehaviorTypes.ToggleActivePassive][0].response_methods))
        self.assertIn(b, list(bc._behaviors[BehaviorTypes.ToggleActivePassive][0].response_methods))
        self.assertIn(c, list(bc._behaviors[BehaviorTypes.ToggleActivePassive][0].response_methods))

        bc.add_response_method(BehaviorTypes.ToDefaultMode, a)
        bc.add_response_method(BehaviorTypes.ToDefaultMode, b)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods), 2)
        self.assertIn(a, list(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods))
        self.assertIn(b, list(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods))

        with self.assertRaises(KeyError):
            bc.add_response_method(BehaviorTypes.ResetToDefaultTemp, c)

    def test_2multiple_behavior_with_same_type(self):
        def a():
            pass

        self.behaviorcontroller_config[1]["behavior"] = "to-default-mode"
        self.behaviorcontroller_config[2]["behavior"] = "to-default-mode"

        bc = BehaviorController(self.behaviorcontroller_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(bc)
        self.assertEqual(len(bc._behaviors), 1)
        self.assertIn(BehaviorTypes.ToDefaultMode, list(bc._behaviors.keys()))
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode]), 3)

        bc.add_response_method(BehaviorTypes.ToDefaultMode, a)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods), 1)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode][1].response_methods), 1)
        self.assertEqual(len(bc._behaviors[BehaviorTypes.ToDefaultMode][2].response_methods), 1)
        self.assertIn(a, list(bc._behaviors[BehaviorTypes.ToDefaultMode][0].response_methods))
        self.assertIn(a, list(bc._behaviors[BehaviorTypes.ToDefaultMode][1].response_methods))
        self.assertIn(a, list(bc._behaviors[BehaviorTypes.ToDefaultMode][2].response_methods))

    def test_3mqtt(self):
        global counter_a
        global counter_b
        global counter_c
        counter_a = 0
        counter_b = 0
        counter_c = 0

        global a
        global b
        global c
        a = 0
        b = 0
        c = 0

        def method_a():
            global counter_a
            counter_a += 1

        def method_b():
            global counter_b
            counter_b += 1

        def method_c():
            global counter_c
            counter_c += 1

        def publish_a():
            global a
            a = a + 1
            self.mqtt_client.publish(self.behaviorcontroller_config[0]["topic-sub"], pressed_cmd)

        def publish_b():
            global b
            b = b + 1
            self.mqtt_client.publish(self.behaviorcontroller_config[1]["topic-sub"], pressed_cmd)

        def publish_c():
            global c
            c = c + 1
            self.mqtt_client.publish(self.behaviorcontroller_config[2]["topic-sub"], pressed_cmd)

        bc = BehaviorController(self.behaviorcontroller_config, self.mqtt_client, self.logger)
        bc.add_response_method(BehaviorTypes.ToDefaultMode, method_a)
        bc.add_response_method(BehaviorTypes.ToggleActivePassive, method_b)
        bc.add_response_method(BehaviorTypes.ResetToDefaultTemp, method_c)

        bc.start()

        pressed_cmd = "PRESSED"

        publish_a()
        publish_b()
        publish_c()

        for i in range(100):
            if random.randint(1, 3) == 1:
                publish_a()
            if random.randint(1, 5) == 1:
                publish_b()
            if random.randint(1, 7) == 1:
                publish_c()

        time.sleep(0.5)
        bc.stop()

        self.assertEqual(a, counter_a)
        self.assertEqual(b, counter_b)
        self.assertEqual(c, counter_c)

    def test_4configfile(self):
        behavior_controller = BehaviorController(self.config["controller"]["button-controller"], self.mqtt_client,
                                                 self.logger)
        self.assertIsNotNone(behavior_controller)


if __name__ == '__main__':
    unittest.main()
