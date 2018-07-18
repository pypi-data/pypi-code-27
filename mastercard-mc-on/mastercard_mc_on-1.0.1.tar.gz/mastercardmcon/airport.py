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
from mastercardmcon import ResourceConfig

class Airport(BaseObject):
    """
    
    """

    __config = {
        
        "6042215f-e827-4c44-991f-66208b69e6f9" : OperationConfig("/loyalty/v1/airport/lounges", "query", ["x-client-correlation-id"], ["searchText","preferredLanguage"]),
        
        "607aa96c-bc6f-4909-a8f9-018bb3c8feab" : OperationConfig("/loyalty/v1/airport/lounges/{loungeId}/detail", "query", ["x-client-correlation-id"], ["preferredLanguage"]),
        
        "b5a8c2da-0351-48ff-ac1d-b89dc358c26e" : OperationConfig("/loyalty/v1/airport/lounges/{loungeId}/history", "query", ["x-client-correlation-id"], ["userId"]),
        
        "26133a38-3d60-4188-a27e-a2278528f4be" : OperationConfig("/loyalty/v1/airport/{userId}/dmc", "query", ["x-client-correlation-id"], []),
        
        "c336a95a-2657-48e9-ba6b-68fafd841db5" : OperationConfig("/loyalty/v1/users/{userId}/airport", "query", ["x-client-correlation-id"], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def getLounges(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("6042215f-e827-4c44-991f-66208b69e6f9", Airport(criteria))






    @classmethod
    def getLoungeDetail(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("607aa96c-bc6f-4909-a8f9-018bb3c8feab", Airport(criteria))






    @classmethod
    def getLoungeHistory(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("b5a8c2da-0351-48ff-ac1d-b89dc358c26e", Airport(criteria))






    @classmethod
    def getDMC(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("26133a38-3d60-4188-a27e-a2278528f4be", Airport(criteria))






    @classmethod
    def userAirportRegistrationStatus(cls,criteria):
        """
        Query objects of type Airport by id and optional criteria
        @param type criteria
        @return Airport object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("c336a95a-2657-48e9-ba6b-68fafd841db5", Airport(criteria))


