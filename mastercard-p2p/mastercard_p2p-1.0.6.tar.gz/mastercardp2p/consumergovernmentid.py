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

class ConsumerGovernmentID(BaseObject):
    """
    
    """

    __config = {
        
        "ea45ac43-2139-4688-ae17-82463272b39b" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "create", [], []),
        
        "907fec6a-cd24-4a77-8736-3f2ad80cc614" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "delete", [], []),
        
        "0b8e421d-4da7-44ef-89c8-69049e63b0b3" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "read", [], []),
        
        "3fe7cc17-3176-4a98-afa9-bcce57c81eca" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "query", [], []),
        
        "ece86d89-47a2-4e23-8138-e7c0cce57372" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "update", [], []),
        
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
        Creates object of type ConsumerGovernmentID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerGovernmentID of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("ea45ac43-2139-4688-ae17-82463272b39b", ConsumerGovernmentID(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerGovernmentID by id

        @param str id
        @return ConsumerGovernmentID of the response of the deleted instance.
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

        return BaseObject.execute("907fec6a-cd24-4a77-8736-3f2ad80cc614", ConsumerGovernmentID(mapObj))

    def delete(self):
        """
        Delete object of type ConsumerGovernmentID

        @return ConsumerGovernmentID of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("907fec6a-cd24-4a77-8736-3f2ad80cc614", self)







    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerGovernmentID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerGovernmentID
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

        return BaseObject.execute("0b8e421d-4da7-44ef-89c8-69049e63b0b3", ConsumerGovernmentID(mapObj))







    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerGovernmentID by id and optional criteria
        @param type criteria
        @return ConsumerGovernmentID object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("3fe7cc17-3176-4a98-afa9-bcce57c81eca", ConsumerGovernmentID(criteria))


    def update(self):
        """
        Updates an object of type ConsumerGovernmentID

        @return ConsumerGovernmentID object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("ece86d89-47a2-4e23-8138-e7c0cce57372", self)






