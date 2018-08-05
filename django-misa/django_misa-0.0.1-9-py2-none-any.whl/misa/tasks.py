# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from misa.utils.isa_upload import upload_assay_data_files_dir

@shared_task(bind=True)
def upload_assay_data_files_dir_task(self, filelist, username, mapping_l, assayid, save_as_link, create_assay_details):
    """
    """
    upload_assay_data_files_dir(filelist, username, mapping_l, assayid, create_assay_details, save_as_link, self)



