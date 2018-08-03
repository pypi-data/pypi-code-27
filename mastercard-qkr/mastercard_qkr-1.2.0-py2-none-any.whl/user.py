#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardqkr import ResourceConfig

class User(BaseObject):
    """
    
    """

    __config = {
        
        "e7cede6a-7026-4ca0-9afc-ff07a155ac2a" : OperationConfig("/labs/proxy/qkr2/internal/api2/user", "create", ["X-Auth-Token"], []),
        
        "624a1ec0-6140-45a9-8c94-ad24e8f94d01" : OperationConfig("/labs/proxy/qkr2/internal/api2/user", "delete", ["X-Auth-Token"], []),
        
        "dd6965f9-d6f5-4fdc-90e8-a48a940db593" : OperationConfig("/labs/proxy/qkr2/internal/api2/user", "query", ["X-Auth-Token"], []),
        
        "70cba2ea-41b3-4d71-9f1a-d7151aa7c36a" : OperationConfig("/labs/proxy/qkr2/internal/api2/user", "update", ["X-Auth-Token"], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type User

        @param Dict mapObj, containing the required parameters to create a new object
        @return User of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("e7cede6a-7026-4ca0-9afc-ff07a155ac2a", User(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type User by id

        @param str id
        @return User of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("624a1ec0-6140-45a9-8c94-ad24e8f94d01", User(mapObj))

    def delete(self):
        """
        Delete object of type User

        @return User of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("624a1ec0-6140-45a9-8c94-ad24e8f94d01", self)








    @classmethod
    def query(cls,criteria):
        """
        Query objects of type User by id and optional criteria
        @param type criteria
        @return User object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("dd6965f9-d6f5-4fdc-90e8-a48a940db593", User(criteria))


    def update(self):
        """
        Updates an object of type User

        @return User object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("70cba2ea-41b3-4d71-9f1a-d7151aa7c36a", self)






