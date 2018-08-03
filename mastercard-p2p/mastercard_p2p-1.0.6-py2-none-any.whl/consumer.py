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
from mastercardp2p import ResourceConfig

class Consumer(BaseObject):
    """
    
    """

    __config = {
        
        "76345b0e-7fee-4723-b725-1a8b5519ecd7" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "delete", [], []),
        
        "31b0be4f-3c4c-4cf6-b1c4-af7ea4cd1a53" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "create", [], []),
        
        "8175f1fd-ff51-4262-94f9-10a42012203c" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "read", [], []),
        
        "469f5799-e1f9-4872-9590-cfab08c9dcd0" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "query", [], ["ref","contact_id_uri"]),
        
        "86ebf72d-4ce5-404f-94eb-8b9d2a7c8601" : OperationConfig("/send/v1/partners/{partnerId}/consumers/search", "create", [], []),
        
        "805ee3fb-4906-4c09-a901-5a3bb5d673ca" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())





    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Consumer by id

        @param str id
        @return Consumer of the response of the deleted instance.
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

        return BaseObject.execute("76345b0e-7fee-4723-b725-1a8b5519ecd7", Consumer(mapObj))

    def delete(self):
        """
        Delete object of type Consumer

        @return Consumer of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("76345b0e-7fee-4723-b725-1a8b5519ecd7", self)



    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("31b0be4f-3c4c-4cf6-b1c4-af7ea4cd1a53", Consumer(mapObj))










    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type Consumer by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Consumer
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

        return BaseObject.execute("8175f1fd-ff51-4262-94f9-10a42012203c", Consumer(mapObj))







    @classmethod
    def listByReferenceOrContactID(cls,criteria):
        """
        Query objects of type Consumer by id and optional criteria
        @param type criteria
        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("469f5799-e1f9-4872-9590-cfab08c9dcd0", Consumer(criteria))

    @classmethod
    def listByReferenceContactIDOrGovernmentID(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("86ebf72d-4ce5-404f-94eb-8b9d2a7c8601", Consumer(mapObj))







    def update(self):
        """
        Updates an object of type Consumer

        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("805ee3fb-4906-4c09-a901-5a3bb5d673ca", self)






