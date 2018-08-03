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

class Card(BaseObject):
    """
    
    """

    __config = {
        
        "28ce649d-55e5-4c8f-8847-6f41df607a35" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "create", ["X-Auth-Token"], []),
        
        "f1f358b8-a909-4476-8c08-2ec35c6d8f72" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "delete", ["X-Auth-Token"], []),
        
        "2a9b6941-5d21-4a28-8385-6c30540c79d4" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "query", ["X-Auth-Token"], []),
        
        "8de3a7cf-ae40-49a7-ae14-fb286c3bf68a" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "read", ["X-Auth-Token"], []),
        
        "67e41aee-b51b-44e9-a5fe-fa83c4f54b41" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "update", ["X-Auth-Token"], []),
        
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
        Creates object of type Card

        @param Dict mapObj, containing the required parameters to create a new object
        @return Card of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("28ce649d-55e5-4c8f-8847-6f41df607a35", Card(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Card by id

        @param str id
        @return Card of the response of the deleted instance.
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

        return BaseObject.execute("f1f358b8-a909-4476-8c08-2ec35c6d8f72", Card(mapObj))

    def delete(self):
        """
        Delete object of type Card

        @return Card of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("f1f358b8-a909-4476-8c08-2ec35c6d8f72", self)








    @classmethod
    def query(cls,criteria):
        """
        Query objects of type Card by id and optional criteria
        @param type criteria
        @return Card object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("2a9b6941-5d21-4a28-8385-6c30540c79d4", Card(criteria))





    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type Card by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Card
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("8de3a7cf-ae40-49a7-ae14-fb286c3bf68a", Card(mapObj))



    def update(self):
        """
        Updates an object of type Card

        @return Card object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("67e41aee-b51b-44e9-a5fe-fa83c4f54b41", self)






