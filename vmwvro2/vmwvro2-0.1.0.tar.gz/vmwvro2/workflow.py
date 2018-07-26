"""
VMware vRealize Workflow implementation and supporting objects.

Copyright (c) 2018, Jose Ibanez

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import requests
import time
import json

from .config import URL_RUN_WORKFLOW_BY_ID, FINISHED_STATES
from .utils import format_url,safeget
from .parameters import WorkflowParameter

class WorkflowError(Exception):
    """Parameters Exception."""
    pass

class WorkflowRunError(Exception):
    """Run Exception."""
    pass




class Workflow:
    """
    Workflow object, contain:
     - an id 
     - a name
     - list of input paramenters

    You can:
     - add paramenters
     - convert to json object
    """


    def __init__(self, id=None, name=None):
        """
        Returns a new Workflow instance.
        """
        self.id = id
        self.input_parameters = []


    def param(self, name=None, value=None, _type="string", param=None):
        if param:
            p = param
        else:
            p = WorkflowParameter(name=name, value=value, _type=_type)
        self.input_parameters.append(p)


    def to_json(self):
        self.body = {"parameters": [] }
        for p in self.input_parameters:
            param = p.to_json()
            self.body['parameters'].append(param)

        return self.body





class WorkflowRun:
    """
    Workflow object to contain execution object
    """

    def __init__(self, wf, session=None):
        """
        Returns a new Workflow instance.
        """
        self.id = None
        self.name = None
        self.version = None
        self.workflowId = wf.id
        self.reqBody = wf.to_json()
        self.vro = None
        self.startUrl= None
        self.href = None
        self.state = None
        self.exception = None
        self.input_parameters = []
        self.output_parameters = []
        self.session = session

		
    def __str__(self):
        return self.session.alias+"/"+self.name+": "+self.state+" "+str(self.exception)
   

    def from_json(self, data):
        """
        load the object from json object or file
        """
        self.answerBody = data
        self.description = data.get("description")
        self.name = data.get("name")
        self.href = data.get("href")
        self.id = data.get("id")
        self.version = data.get("version")
        self.state = data.get("state")
        self.exception = data.get("content-exception")    

        self.output_parameters = []
        for jParam in  data.get('output-parameters'):
            p = WorkflowParameter()
            p.from_json(jParam)
            self.output_parameters.append(p)
        		 
        self.input_parameters = []
        for jParam in  data.get('input-parameters'):
            p = WorkflowParameter()
            p.from_json(jParam)
            self.input_parameters.append(p)


    def print_paramenters(self):
        for p in self.input_parameters:
            print "IN:  " + str(p)
        for p in self.output_parameters:
            print "OUT: " + str(p)
            
            
    def run(self, session=None):
        """
        Starts the Workflow on vRO server defined in Sesion parameter
        """

        if self.state in FINISHED_STATES:
            return 0

        if session is not None:
            self.session = session

        if self.session is None:
            self.state = "failed"
            self.exception = "No vRO session defined"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
		
        url = format_url(URL_RUN_WORKFLOW_BY_ID,
                         base_url=self.session.url,
                         id=self.workflowId)

        body = json.dumps(self.reqBody)		
		
        try:
            r = requests.post(url,
                          auth=self.session.basic_auth,
                          verify=self.session.verify_ssl,
                          headers=headers,
                          proxies=self.session.proxies,
                          data=body)

            status_code = r.status_code

        except requests.exceptions.RequestException as e:
            status_code = 999
            print e


        if status_code != 202:
            self.state = "failed"
            self.exception = "Wrong HTTP code received: "+str(status_code)
            return


        self.href = r.headers.get("Location")
        return 0



    def update(self):
        """
        Update the state, logs and content of this Workflow Run.
        """

        if self.state in FINISHED_STATES:
            return

        if self.href is None:
            self.state = "failed"
            return

        headers = {"Content-Type": "application/json"}

        try:
            r = requests.get(self.href,
                         auth=self.session.basic_auth,
                         verify=self.session.verify_ssl,
                         proxies=self.session.proxies,
                         headers=headers)

            status_code = r.status_code

        except requests.exceptions.RequestException as e:
            status_code = 999
            print e


        if status_code < 200 or status_code >299:
            self.state = "failed"
            self.exception = "Wrong HTTP code received: "+str(status_code)
            return

        self.from_json(r.json())
        return 0
        

        
    def wait(self):
        """
        Wait for execution finished
        """
        secToWait = [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ]
        
        for t in secToWait:

            self.update()
            if self.state in FINISHED_STATES:
                break
                
            print "Waiting for " + self.name + ", " + str(t) + " Sec."
            time.sleep(t)



    def from_file(self, path):
        """
        Load answer from file, used in testing
        """

        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)
        self.from_json(jData)



class MultiRun:
    """
    Manage a list of executions
    """

    def __init__(self):
        self.list = dict()

        
    def add(self, wf, sessionList, filter="*"):
        """
        To create a list of WF executions with a list of sessions (vRO servers)
         - wf: Workflow 
         - sessionList: SessionList
         - filter: string

        The same workflow will executed in several vRO's hosts
        """

        for alias in sessionList.list:
            s = sessionList.list.get(alias)

            if filter not in s.tags and filter != alias and filter != "*":
                continue

            self.list[alias]=WorkflowRun(wf,s)

            
    
    def run(self, path=None):
        """
        To start the those list of WF/vRO servers

        If a path is provied, no executions will perfomed, a file will be used as REST answer, used in testing
        """

        for alias in self.list:
        
            if path is None:
                self.list[alias].run()
            else:
                self.list[alias].from_file(path)

            print "Running: "+alias+" "+str(self.list[alias].name)

    
    
    
    def wait(self):
        """
        Wait for all list finished
        """

        secToWait = [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ]
        secToWait = [ 1, 1, 2, 3, 5 ]
        
        for t in secToWait:
   
            nRunning = 0
        
            for alias in self.list:
                self.list[alias].update()
                if self.list[alias].state not in FINISHED_STATES:
                    print self.list[alias].state
                    nRunning += 1
            
            if nRunning == 0:
                break

            print "Waiting for " + alias + ", " + str(t) + " Sec."
            time.sleep(t)
                
            
                
        print "Result:"
        for alias in self.list:
            print "vRO:"+alias+", WF:"+str(self.list[alias].name)+", Result:"+self.list[alias].state
        
        
        
        
        
    