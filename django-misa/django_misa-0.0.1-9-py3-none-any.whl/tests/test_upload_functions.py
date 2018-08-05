# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.test import TestCase
#
# from metab.models import  MFile
# from misa.models import AssayRun
# from misa.utils.isa_upload import upload_assay_data_files
# import os
# from init_setup import upload_assay_data_form_setup
#
# class UploadAssayDataFilesFunctionTestCase(TestCase):
#     def setUp(self):
#         upload_assay_data_form_setup(self)
#
#     def test_upload_assay_data_files(self):
#         """
#         Test to check unit testing running
#         """
#         data_zipfile_pth = os.path.join(os.path.dirname(__file__), 'data', 'DUMMY_P_WAX1_PHE.zip')
#         mapping_file = os.path.join(os.path.dirname(__file__), 'data', 'mapping_file.csv')
#
#         upload_assay_data_files(self.assay.id, data_zipfile_pth, data_mappingfile=open(mapping_file, 'r'))
#
#         self.assertIs(len(MFile.objects.all()), 14)
#         self.assertIs(len(AssayRun.objects.all()), 12)
#
#
#
#
#
#
#
#
