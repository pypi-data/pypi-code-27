#!/usr/bin/env python
import unittest
from parameterized import parameterized


from vmwvro2.workflow import Workflow, MultiRun
from vmwvro2.sessions import SessionList


sl = SessionList()
sl.load()
vro = ['dev-de', 'dev-ie', 'dev-it']

class UpdateAnIPManualy(unittest.TestCase):

    mt = MultiRun()

    @classmethod
    def setUpClass(cls):
        """
        WF: "Cramer, update an IP Manualy"
        """
        
        wf = Workflow()
        wf.id = "338beefa-9f7f-469b-89d4-914031ffbfb6"
        wf.name = "Cramer, update an IP Manualy"

        wf.param(name="ipAddress", value="10.10.10.10")
        wf.param(name="newStatus", value="In Service")
        wf.param(name="description", value="TestingCramer")
        wf.param(name="mailAddressList", value="")

        cls.mt.add(wf,sl,"dev")
        cls.mt.run("./sample-json/exeDetail2.json")
        cls.mt.wait()
        cls.mt.getLogs("./sample-json/exeDetail4.json")
        
        for alias in cls.mt.list:
            cls.mt.list[alias].print_workflow()

    @parameterized.expand(vro)
    def test_state(self,alias): 
        
        try:
            wfExe = self.mt.list[alias]
        except:
            raise unittest.SkipTest("Not performed")

        self.assertEqual(wfExe.state, "completed")
        

    @parameterized.expand(vro)
    def test_logs(self,alias):
        
        wfExe = self.mt.list[alias]
        out = wfExe.output_parameters
        
        self.assertRegexpMatches(wfExe.log, "Duplicated")	
        
        
            
if __name__ == '__main__':
    #unittest.main(testRunner=HTMLTestRunner(output='example_dir'))
    unittest.main()

