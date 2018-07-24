# -*- coding: utf-8 -*-

#
#    fhirgfe fhirGFE.
#    Copyright (c) 2018 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#

# gfefhir = GfeFHIR(smart=smart)
# gfe_obs = gfefhir.annotate(id='')
# reponse = gfefhir.annotate_create(id='')
# reponse = gfe_obs.create(smart.server)

import json
import uuid
import fhirclient.models.patient as patient
import fhirclient.models.codeableconcept as codeableconcept
import fhirclient.models.coding as coding
import fhirclient.models.fhirreference as fhirreference
from fhirclient.client import FHIRClient
from gfe_client import AnnotateApi
import gfe_client
import fhirclient.models.observation as o
import fhirclient.models.specimen as sp
import fhirclient.models.sequence as s
import fhirclient.models.codeableconcept as cc
import fhirclient.models.fhirreference as r
import fhirclient.models.coding as c


def mkCoding(**keywords):
    '''
    returns a Coding using keyword/values
    '''
    cod = c.Coding()
    for key in keywords:
        setattr(cod, key, keywords[key])
    return cod


class GfeFHIR(object):
    '''
    classdocs
    '''
    def __init__(self,
                 smart: FHIRClient=None,
                 gfeapi: AnnotateApi=None,
                 verbose: bool=False,
                 verbosity=1):
        '''
        Constructor
        '''
        self.smart = smart
        if not gfeapi:
            config = gfe_client.Configuration()
            config.host = "http://act.b12x.org"
            api = gfe_client.ApiClient(configuration=config)
            self.gfeapi = gfe_client.AnnotateApi(api_client=api)
        else:
            self.gfeapi = gfeapi

    def annotate(self, obsid):
        obs = o.Observation()
        obs.uuid = uuid.uuid4().urn
        observation = o.Observation.read(obsid, self.smart.server)
        obs.specimen = observation.specimen
        obs.related = observation.related
        obs.basedOn = observation.basedOn
        obs.code = observation.code
        obs.component = observation.component
        obs.method = observation.method
        seq_id = observation.related[0].target.reference.split("/")[1]
        seq = s.Sequence.read(seq_id, self.smart.server)
        obseverved_seq = seq.observedSeq
        annotation = self.gfeapi.annotate_get(obseverved_seq, imgthla_version="3.31.0")
        gfe = annotation.gfe
        bodysite3 = cc.CodeableConcept()
        bodySiteCoding3 = mkCoding(system='http://act.b12x.org',
                                   code='261063000',
                                   version="0.0.5")

        bodysite3.coding = [bodySiteCoding3]
        bodysite3.text = gfe
        obs.valueCodeableConcept = bodysite3
        obs.status = 'final'
        obs.subject = observation.subject
        return obs









