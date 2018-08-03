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

class Order(BaseObject):
    """
    
    """

    __config = {
        
        "30cebb3f-f454-4e4d-a0c3-bec095f12539" : OperationConfig("/labs/proxy/qkr2/internal/api2/order/pat", "create", [], []),
        
        "4b8a9fcf-dda6-48c7-b687-186a10a83052" : OperationConfig("/labs/proxy/qkr2/internal/api2/order/pat/{id}", "delete", [], []),
        
        "92e80890-d196-48a6-a241-9a4f2f7a7de9" : OperationConfig("/labs/proxy/qkr2/internal/api2/order/pat/{id}", "read", [], []),
        
        "a6908b39-8c04-4820-abd9-d4ae0a56c58c" : OperationConfig("/labs/proxy/qkr2/internal/api2/order/pat/{id}", "update", [], []),
        
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
        Creates object of type Order

        @param Dict mapObj, containing the required parameters to create a new object
        @return Order of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("30cebb3f-f454-4e4d-a0c3-bec095f12539", Order(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Order by id

        @param str id
        @return Order of the response of the deleted instance.
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

        return BaseObject.execute("4b8a9fcf-dda6-48c7-b687-186a10a83052", Order(mapObj))

    def delete(self):
        """
        Delete object of type Order

        @return Order of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("4b8a9fcf-dda6-48c7-b687-186a10a83052", self)







    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type Order by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Order
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

        return BaseObject.execute("92e80890-d196-48a6-a241-9a4f2f7a7de9", Order(mapObj))



    def update(self):
        """
        Updates an object of type Order

        @return Order object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("a6908b39-8c04-4820-abd9-d4ae0a56c58c", self)






