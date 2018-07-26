#!/usr/bin/env python

import json
from vmwvro2.workflow import Workflow, WorkflowRun
from vmwvro2.parameters import WorkflowParameter



#Workflow
wf = Workflow()
wf.id = ""
wf.param(name="vmname", value="some_vm_name", _type="VC:VirtualMachine")
wf.param(name="user", value="some_user", _type="string")

v = [ "aa", "bb", "cc", "dd" ]
p1 = WorkflowParameter(name = "mio", _type = "Array/string", value = v )
wf.param(param=p1)

print wf.input_parameters
wf.to_json()


#WorkflowRun
wfExe = WorkflowRun(wf)

print wfExe.reqBody

# Aux for test
with open('./sample-json/exeDetail2.json', 'r') as myfile:
    data=myfile.read()
jData = json.loads(data)
wfExe.from_json(jData)

print wfExe.name
print wfExe.version
print wfExe.id

#exit
# connect with server
vro = ""
#wfExe.run(vro)
#wfExe.status()
#wfExe.wait()


