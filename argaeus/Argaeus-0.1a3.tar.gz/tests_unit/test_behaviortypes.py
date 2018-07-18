import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from argaeus.controller.behavior.behaviortypes import BehaviorTypes


class Test_BehaviorTypes(unittest.TestCase):
    def test_todefaultmode(self):
        result = BehaviorTypes.factory("to-default-mode")
        self.assertEqual(result, BehaviorTypes.ToDefaultMode)

    def test_toggleactivepassive(self):
        result = BehaviorTypes.factory("Toggle-Active-Passive")
        self.assertEqual(result, BehaviorTypes.ToggleActivePassive)

    def test_resettodefaulttemp(self):
        result = BehaviorTypes.factory("RESET-TO-DEFAULT-TEMP")
        self.assertEqual(result, BehaviorTypes.ResetToDefaultTemp)

    def test_unkown(self):
        with self.assertRaises(ValueError):
            result = BehaviorTypes.factory("blablabla")


if __name__ == '__main__':
    unittest.main()
