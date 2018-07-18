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

class Offers(BaseObject):
    """
    
    """

    __config = {
        
        "e4cf1bb6-bf03-48e8-9d9a-57a64cae0502" : OperationConfig("/loyalty/v1/offers", "list", ["x-client-correlation-id"], ["userId","preferredLanguage","sort","category","featured","favorite","partner","latitude","longitude","searchRadius"]),
        
        "7f9c856b-9f61-49f4-a679-7c42abd38d3d" : OperationConfig("/loyalty/v1/offers/{offerId}/activate", "create", ["x-client-correlation-id"], []),
        
        "53d0b07d-12ee-46ef-ac39-bd9ad3cd0c81" : OperationConfig("/loyalty/v1/offers/{offerId}/detail", "query", ["x-client-correlation-id"], ["userId","preferredLanguage"]),
        
        "3c09dd04-9ed4-4e12-b990-0d5cfcf2aaa1" : OperationConfig("/loyalty/v1/offers/{offerId}/favorite", "create", ["x-client-correlation-id"], []),
        
        "7a5d82e6-a016-46c2-851a-bec25eb164a1" : OperationConfig("/loyalty/v1/offers/{offerId}/redeem", "create", ["x-client-correlation-id"], []),
        
        "865a1660-1a58-47ec-a679-38aebda03fa0" : OperationConfig("/loyalty/v1/offers/{offerId}/unfavorite", "create", ["x-client-correlation-id"], []),
        
        "19b68755-4149-455a-a978-c4ca239c138b" : OperationConfig("/loyalty/v1/offers/promo", "create", ["x-client-correlation-id"], []),
        
        "72fb5247-d236-4963-987a-99e333dc8fab" : OperationConfig("/loyalty/v1/offers/redeemed", "list", ["x-client-correlation-id"], ["userId","preferredLanguage"]),
        
        "03bfa1ea-cbb7-4e8c-a4ac-6024c19c7f18" : OperationConfig("/loyalty/v1/points/expiring", "query", ["x-client-correlation-id"], ["userId"]),
        
        "4a2c7983-684d-4be0-aeed-c931436db12f" : OperationConfig("/loyalty/v1/points", "query", ["x-client-correlation-id"], ["userId"]),
        
        "5b6b90bb-5d91-4ca7-b310-6c0224369158" : OperationConfig("/loyalty/v1/users/{userId}/offers", "query", ["x-client-correlation-id"], []),
        
        "eef640eb-bd91-4564-9611-d01cbc4a370e" : OperationConfig("/loyalty/v1/vouchers", "list", ["x-client-correlation-id"], ["userId"]),
        
        "2b60cb7b-4ec2-4791-bb06-6f1f35bce119" : OperationConfig("/loyalty/v1/vouchers/{voucherId}/detail", "query", ["x-client-correlation-id"], ["userId"]),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())




    @classmethod
    def getOffers(cls,criteria=None):
        """
        List objects of type Offers

        @param Dict criteria
        @return Array of Offers object matching the criteria.
        @raise ApiException: raised an exception from the response status
        """

        if not criteria :
            return BaseObject.execute("e4cf1bb6-bf03-48e8-9d9a-57a64cae0502", Offers())
        else:
            return BaseObject.execute("e4cf1bb6-bf03-48e8-9d9a-57a64cae0502", Offers(criteria))




    @classmethod
    def activateOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("7f9c856b-9f61-49f4-a679-7c42abd38d3d", Offers(mapObj))











    @classmethod
    def getOfferDetail(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("53d0b07d-12ee-46ef-ac39-bd9ad3cd0c81", Offers(criteria))

    @classmethod
    def favoriteOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("3c09dd04-9ed4-4e12-b990-0d5cfcf2aaa1", Offers(mapObj))






    @classmethod
    def redeemOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("7a5d82e6-a016-46c2-851a-bec25eb164a1", Offers(mapObj))






    @classmethod
    def unfavoriteOffer(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("865a1660-1a58-47ec-a679-38aebda03fa0", Offers(mapObj))






    @classmethod
    def submitOfferPromo(cls,mapObj):
        """
        Creates object of type Offers

        @param Dict mapObj, containing the required parameters to create a new object
        @return Offers of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("19b68755-4149-455a-a978-c4ca239c138b", Offers(mapObj))








    @classmethod
    def getRedeemedOffers(cls,criteria=None):
        """
        List objects of type Offers

        @param Dict criteria
        @return Array of Offers object matching the criteria.
        @raise ApiException: raised an exception from the response status
        """

        if not criteria :
            return BaseObject.execute("72fb5247-d236-4963-987a-99e333dc8fab", Offers())
        else:
            return BaseObject.execute("72fb5247-d236-4963-987a-99e333dc8fab", Offers(criteria))









    @classmethod
    def getPointsExpiring(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("03bfa1ea-cbb7-4e8c-a4ac-6024c19c7f18", Offers(criteria))






    @classmethod
    def getPoints(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("4a2c7983-684d-4be0-aeed-c931436db12f", Offers(criteria))






    @classmethod
    def userOffersRegistrationStatus(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("5b6b90bb-5d91-4ca7-b310-6c0224369158", Offers(criteria))



    @classmethod
    def getVouchers(cls,criteria=None):
        """
        List objects of type Offers

        @param Dict criteria
        @return Array of Offers object matching the criteria.
        @raise ApiException: raised an exception from the response status
        """

        if not criteria :
            return BaseObject.execute("eef640eb-bd91-4564-9611-d01cbc4a370e", Offers())
        else:
            return BaseObject.execute("eef640eb-bd91-4564-9611-d01cbc4a370e", Offers(criteria))









    @classmethod
    def getVoucherDetail(cls,criteria):
        """
        Query objects of type Offers by id and optional criteria
        @param type criteria
        @return Offers object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("2b60cb7b-4ec2-4791-bb06-6f1f35bce119", Offers(criteria))


