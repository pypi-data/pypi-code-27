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

from .config import URL_RUN_WORKFLOW_BY_ID
from .utils import format_url,safeget


class ParametersError(Exception):
    """Parameters Exception."""
    pass




class WorkflowParameter:

    def __init__(self, name=None, value=None, _type=None, scope="local", description=None):
        """
        Returns a new _WorkflowParameter instance.

        :param name: parameter name
        :param value:  parameter value
        :param _type: parameter value
        :param scope: parameter scope
        :param description: parameter description
        """
        self.name = name
        self.value = value
        self.type = _type
        self.scope = scope
        self.description = description

    def __str__(self):

        if self.type == "boolean" or self.type == "String" or self.type == "string" or self.type == "number" or self.type == "Array/string":
            return self.name + " = " + str(self.value)
        
        return self.name + " = <"+self.type+">"


    def from_json(self,data):
        """
        Read a parameter from REST wf run answer
        """
        self.name=data.get('name')
        self.scope=data.get('scope')
        self.type=data.get('type')
        self.description=data.get("description")
        
        if self.type == "String":
            self.type = "string"
        
        sTypes = [ "boolean", "string", "number"]
        
        if self.type in sTypes:
            self.value=safeget(data,'value',self.type,'value')

        elif self.type == "Array/string":
            self.value = []

            eList = safeget(data, 'value', 'array', 'elements')
            if eList is None:
                 eList = []

            for e in eList:
                v=safeget(e,'string','value')
                self.value.append(v)
        else:
             self.value = "<no suported>" 


    def to_json(self):

        data = {
            "name" : self.name,
            "type" : self.type,
            "scope" : self.scope,
        }

        if self.type == "string" or self.type == "number":

            value = { "value" : { self.type : { "value": self.value } } }
            data.update(value)


        elif self.type == "Array/string":

            els = []
            for v in self.value:
                els.append({ 'string' : { 'value' : v } })

            value = {  'value' : { 'array' : { 'elements' : els } } }    
            data.update(value)


        else:

            value = { 'value': "<No suported>" }
            data.update(value)


        return data


class WorkflowParameters:

    def __init__(self):
        """Returns a new WorkflowParameters instance.

        This collection object holds one or more vRO parameters.
        """
        self._params = list()

    def __len__(self):
        return len(self._params)

    def __iter__(self):
        for param in self._params:
            yield param

    def add(self, name, value, _type="string", scope="local", description=None):
        """
        Add a parameter to the collection.

        :param name: parameter name
        :param value: parameter value
        :param _type: parameter type, default is 'string'
        :param scope: parameter scope, default is 'local'
        :param description: parameter description, default is None
        """
        self._params.append(WorkflowParameter(name, value, _type, scope, description))

    def to_json(self):
        """Returns this instance in JSON format."""
        data = '{"parameters":['

        num_of_params = len(self._params)
        cur_param = 1

        for param in self._params:
            data += '{"type":"%s","scope":"%s","name":"%s","description":"%s","value":{"%s":{"value":"%s"}}}' % (
                param.type, param.scope, param.name, param.description, param.type, param.value
            )
            if cur_param < num_of_params:
                data += ","
            cur_param += 1

        data += "]}"

        return data

    def to_xml(self):
        """Returns this instance in XML format."""
        data = '<execution-context xmlns="http://www.vmware.com/vco"><parameters>'

        for param in self._params:
            data += '<parameter name="%s" type="%s"><%s>%s</%s></parameter>' % (
                param.name, param.type, param.type, param.value, param.type
            )

        data += '</parameters></execution-context>'

        return data
