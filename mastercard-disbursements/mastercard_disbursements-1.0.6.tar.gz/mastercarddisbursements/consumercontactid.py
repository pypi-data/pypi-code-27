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

class ConsumerContactID(BaseObject):
    """
    
    """

    __config = {
        
        "5f8da853-ded8-4318-bc5f-6871a3f594c3" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "create", [], []),
        
        "da633bd9-a56a-4495-9736-a68af136107f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "delete", [], []),
        
        "d8064492-dc91-4943-8b19-c54ebb83f57c" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "read", [], []),
        
        "d310ee64-daf9-4119-a79a-eaea000c55ff" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "query", [], []),
        
        "969c6ba4-eb02-46b9-b13a-dd6897d1542e" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "update", [], []),
        
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
        Creates object of type ConsumerContactID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerContactID of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("5f8da853-ded8-4318-bc5f-6871a3f594c3", ConsumerContactID(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerContactID by id

        @param str id
        @return ConsumerContactID of the response of the deleted instance.
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

        return BaseObject.execute("da633bd9-a56a-4495-9736-a68af136107f", ConsumerContactID(mapObj))

    def delete(self):
        """
        Delete object of type ConsumerContactID

        @return ConsumerContactID of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("da633bd9-a56a-4495-9736-a68af136107f", self)







    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerContactID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerContactID
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

        return BaseObject.execute("d8064492-dc91-4943-8b19-c54ebb83f57c", ConsumerContactID(mapObj))







    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerContactID by id and optional criteria
        @param type criteria
        @return ConsumerContactID object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("d310ee64-daf9-4119-a79a-eaea000c55ff", ConsumerContactID(criteria))


    def update(self):
        """
        Updates an object of type ConsumerContactID

        @return ConsumerContactID object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("969c6ba4-eb02-46b9-b13a-dd6897d1542e", self)






