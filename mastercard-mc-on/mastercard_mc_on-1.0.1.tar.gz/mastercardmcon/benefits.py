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

class Benefits(BaseObject):
    """
    
    """

    __config = {
        
        "0ee9d692-2964-4443-8741-69b8bb0c236b" : OperationConfig("/loyalty/v1/benefits/assigned", "query", ["x-client-correlation-id"], ["ica","userId","channel","preferredLanguage"]),
        
        "0da05caa-0840-4e18-b6be-b00c0fd0cffa" : OperationConfig("/loyalty/v1/benefits/{benefitId}/detail", "query", ["x-client-correlation-id"], ["ica","channel","preferredLanguage"]),
        
        "76924d89-3720-4bec-94ac-d2800e0cc319" : OperationConfig("/loyalty/v1/benefits", "query", ["x-client-correlation-id"], ["ica","cardProductType","channel","preferredLanguage"]),
        
        "24be1b6e-7781-44e0-9263-19fa8933facf" : OperationConfig("/loyalty/v1/benefits", "create", ["x-client-correlation-id"], []),
        
        "66901251-293b-4e4e-b0a6-178142eb7dc0" : OperationConfig("/loyalty/v1/benefits/programterms", "query", ["x-client-correlation-id"], ["ica","preferredLanguage"]),
        
        "5d411ea9-4a8d-47b1-948b-f18a5f9758e8" : OperationConfig("/loyalty/v1/users/{userId}/benefits", "query", ["x-client-correlation-id"], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def getAssignedBenefits(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("0ee9d692-2964-4443-8741-69b8bb0c236b", Benefits(criteria))






    @classmethod
    def getBenefitDetail(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("0da05caa-0840-4e18-b6be-b00c0fd0cffa", Benefits(criteria))






    @classmethod
    def getBenefits(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("76924d89-3720-4bec-94ac-d2800e0cc319", Benefits(criteria))

    @classmethod
    def selectBenefits(cls,mapObj):
        """
        Creates object of type Benefits

        @param Dict mapObj, containing the required parameters to create a new object
        @return Benefits of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("24be1b6e-7781-44e0-9263-19fa8933facf", Benefits(mapObj))











    @classmethod
    def getProgramTerms(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("66901251-293b-4e4e-b0a6-178142eb7dc0", Benefits(criteria))






    @classmethod
    def userBenefitsRegistrationStatus(cls,criteria):
        """
        Query objects of type Benefits by id and optional criteria
        @param type criteria
        @return Benefits object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("5d411ea9-4a8d-47b1-948b-f18a5f9758e8", Benefits(criteria))


