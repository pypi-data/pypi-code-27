# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from __future__ import unicode_literals
from django.test import TestCase
from misa.models import PolarityType
from misa.models import StudySample, AssayDetail
from misa.models import ExtractionProtocol, SpeProtocol, ChromatographyProtocol, MeasurementProtocol
from misa.models import ExtractionProcess, SpeProcess, ChromatographyProcess, MeasurementProcess


from .init_setup import protocol_setup


class AssayDetailsCreateTestCase(TestCase):
    def setUp(self):
        protocol_setup(self)


    # def test_create_lcms_assay_details(self):
    #
    #     # ANIMAL_WAX[1]_C30[0]_LC-MS_POS
    #     ei = ExtractionProcess(extractionprotocol=ExtractionProtocol.objects.filter(code_field='P')[0])
    #     ei.save()
    #
    #     # Create SPE process
    #     spei = SpeProcess(spefrac=1, speprotocol=SpeProtocol.objects.filter(code_field='WAX')[0])
    #     spei.save()
    #
    #     # Create chromtography process
    #     ci = ChromatographyProcess(chromatographyfrac=0, chromatographyprotocol= ChromatographyProtocol.objects.filter(code_field='PHE')[0])
    #     ci.save()
    #
    #     # create measurement process
    #     mi = MeasurementProcess(measurementprotocol=MeasurementProtocol.objects.filter(code_field='LC-MS')[0],
    #                             polaritytype=PolarityType.objects.filter(type='POSITIVE')[0]
    #                             )
    #     mi.save()
    #
    #     ss = StudySample.objects.filter(sample_name='ANIMAL')[0]
    #
    #     ad = AssayDetail(assay=self.assay,
    #                studysample=ss,
    #                extractionprocess= ei,
    #                speprocess=spei,
    #                chromatographyprocess=ci,
    #                measurementprocess= mi)
    #
    #     ad.save()
    #     self.assertEqual(ad.code_field, 'ANIMAL_P_WAX_1_PHE_0_LC-MS_POSITIVE')
    #
