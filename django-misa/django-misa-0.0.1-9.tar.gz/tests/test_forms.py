# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from __future__ import unicode_literals

from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User

from misa.models import PolarityType
from misa.models import ExtractionProtocol, SpeProtocol, ChromatographyProtocol, MeasurementProtocol, SampleCollectionProtocol
from misa.models import ExtractionProcess, SpeProcess, ChromatographyProcess, MeasurementProcess,SampleCollectionProcess
from misa.models import StudySample, Assay, AssayDetail, AssayRun
from misa.utils.isa_upload import upload_assay_data_files_zip
from misa.forms import AssayDetailForm, UploadAssayDataFilesForm
from .init_setup import upload_assay_data_form_setup

import os

from django.core.files.uploadedfile import SimpleUploadedFile

class AssayDetailFormTestCase(TestCase):
    def setUp(self):
        upload_assay_data_form_setup(self)

    def test_form_submission(self):
        """
        Test to check unit testing running
        """
        #Using a model form as a validator that is not a HTTP request (as per page 165 of Two Scoops of Django 1.11
        assay = Assay.objects.filter(description='P_WAX[1]_PHE[0]_LC-MS_LC-MSMS')[0]
        ss = StudySample.objects.filter(sample_name='B')[0]

        sc = SampleCollectionProcess(
            samplecollectionprotocol=SampleCollectionProtocol.objects.get(code_field='DIATOM'))
        sc.save()

        ei = ExtractionProcess(extractionprotocol=ExtractionProtocol.objects.filter(code_field='DOM')[0])
        ei.save()

        # Create SPE process
        spei = SpeProcess(spefrac=2, speprotocol=SpeProtocol.objects.filter(code_field='DOM')[0])
        spei.save()

        # Create chromtography process
        ci = ChromatographyProcess(chromatographyfrac=0,
                                    chromatographyprotocol=ChromatographyProtocol.objects.filter(
                                        code_field='SFRP')[0])
        ci.save()

        # create measurement process
        mi = MeasurementProcess(measurementprotocol=MeasurementProtocol.objects.filter(code_field='FT-ICR')[0],
                                 polaritytype=PolarityType.objects.filter(type='POSITIVE')[0])
        mi.save()

        data_in = {'assay': assay.id,
                   'studysample': ss.id,
                   'samplecollectionprocess': sc.id,
                   'extractionprocess': ei.id,
                   'speprocess': spei.id,
                   'chromatographyprocess': ci.id,
                   'measurementprocess': mi.id}

        form = AssayDetailForm(data_in)
        self.assertTrue(form.is_valid())

        ad = form.save()

        self.assertEqual(ad.chromatographyprocess.chromatographyfrac, 0)
        self.assertEqual(ad.speprocess.spefrac, 2)
        self.assertEqual(ad.code_field, 'B_DIATOM_DOM_DOM_2_SFRP_0_FT-ICR_POSITIVE')
        self.assertIs(len(AssayDetail.objects.all()), 5)


    # def test_form_submission_dma(self):
    #     """
    #     Test to check unit testing running
    #     """
    #     #Using a model form as a validator that is not a HTTP request (as per page 165 of Two Scoops of Django 1.11
    #     assay = Assay.objects.filter(description='P_WAX[1]_PHE[0]_LC-MS_LC-MSMS')[0]
    #     ss = StudySample.objects.filter(sample_name='BLANK')[0]
    #
    #     ei = ExtractionProcess(extractionprotocol=ExtractionProtocol.objects.filter(code_field='P')[0])
    #     ei.save()
    #
    #     # Create SPE process
    #     spei = SpeProcess(spefrac=2, speprotocol=SpeProtocol.objects.filter(code_field='WAX')[0])
    #     spei.save()
    #
    #     # Create chromtography process
    #     ci = ChromatographyProcess(chromatographyfrac=0,
    #                                 chromatographyprotocol=ChromatographyProtocol.objects.filter(
    #                                     code_field='PHE')[0])
    #     ci.save()
    #
    #     # create measurement process
    #     mi = MeasurementProcess(measurementprotocol=MeasurementProtocol.objects.filter(code_field='LC-MS')[0],
    #                              polaritytype=PolarityType.objects.filter(type='POSITIVE')[0])
    #     mi.save()
    #
    #     data_in = {'assay': assay.id,
    #                'studysample': ss.id,
    #                'extractionprocess': ei.id,
    #                'speprocess': spei.id,
    #                'chromatographyprocess': ci.id,
    #                'measurementprocess': mi.id}
    #
    #     form = AssayDetailForm(data_in)
    #
    #     form = AssayDetailForm(data_in)
    #     self.assertTrue(form.is_valid())
    #
    #     ad = form.save()
    #
    #     self.assertEqual(ad.chromatographyprocess.chromatographyfrac, 0)
    #     self.assertEqual(ad.speprocess.spefrac, 2)
    #     self.assertEqual(ad.code_field, 'BLANK_P_WAX_2_PHE_0_LC-MS_POSITIVE')
    #     self.assertIs(len(AssayDetail.objects.all()), 7)


# class UploadAssayDataFilesFormTestCase(TestCase):
#     def setUp(self):
#         upload_assay_data_form_setup(self)
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@…', password='top_secret')
#
#     def test_upload_assay_data_files(self):
#         """
#         Test to check unit testing running
#         """
#         # Using a model form as a validator that is not a HTTP request (as per page 165 of Two Scoops of Django 1.11
#         data_zipfile_pth = os.path.join(os.path.dirname(__file__), 'data', 'DUMMY_P_WAX1_PHE.zip')
#         data_zipfile = SimpleUploadedFile('DUMMY_P_WAX1_PHE.zip', open(data_zipfile_pth, 'r').read())
#         data_mapping_file = os.path.join(os.path.dirname(__file__), 'data', 'mapping_file.csv')
#
#         files_in = {'data_zipfile': data_zipfile,
#                     'data_mappingfile': File(open(data_mapping_file), 'r')}
#
#         form = UploadAssayDataFilesForm(self.user, {}, files_in,  assayid=self.assay.id)
#
#
#         print 'is form valid?', form.valid()
#
#         # self.assertTrue(form.is_valid())
#         # form.save()
#
#         data_zipfile = form.cleaned_data['data_zipfile']
#         data_mappingfile = form.cleaned_data['data_mappingfile']
#         assayid = self.assay.id
#         upload_assay_data_files_zip(assayid, data_zipfile, data_mappingfile, self.user, True)
#
#         self.assertIs(len(MFile.objects.all()), 14)
#         self.assertIs(len(AssayRun.objects.all()), 12)