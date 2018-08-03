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
from mastercarddisbursements import ResourceConfig

class Consumer(BaseObject):
    """
    
    """

    __config = {
        
        "238da63f-2d77-4df3-a83d-a326ed9b01ed" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "delete", [], []),
        
        "afbc5b52-9548-4e6f-b948-444c7f9f7cc1" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "create", [], []),
        
        "2c7f1b57-fd8e-46cd-8aa3-d193735c1fa3" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "read", [], []),
        
        "3cae48d1-c974-45df-bcf9-5f3665aac1b4" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "query", [], ["ref","contact_id_uri"]),
        
        "aa2c4b5c-b26f-4c3a-bf20-9032256371a1" : OperationConfig("/send/v1/partners/{partnerId}/consumers/search", "create", [], []),
        
        "da656c8b-07ea-4c4a-94ff-949f367f01c2" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "update", [], []),
        
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

        return BaseObject.execute("238da63f-2d77-4df3-a83d-a326ed9b01ed", Consumer(mapObj))

    def delete(self):
        """
        Delete object of type Consumer

        @return Consumer of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("238da63f-2d77-4df3-a83d-a326ed9b01ed", self)



    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("afbc5b52-9548-4e6f-b948-444c7f9f7cc1", Consumer(mapObj))










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

        return BaseObject.execute("2c7f1b57-fd8e-46cd-8aa3-d193735c1fa3", Consumer(mapObj))







    @classmethod
    def listByReferenceOrContactID(cls,criteria):
        """
        Query objects of type Consumer by id and optional criteria
        @param type criteria
        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("3cae48d1-c974-45df-bcf9-5f3665aac1b4", Consumer(criteria))

    @classmethod
    def listByReferenceContactIDOrGovernmentID(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("aa2c4b5c-b26f-4c3a-bf20-9032256371a1", Consumer(mapObj))







    def update(self):
        """
        Updates an object of type Consumer

        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("da656c8b-07ea-4c4a-94ff-949f367f01c2", self)






