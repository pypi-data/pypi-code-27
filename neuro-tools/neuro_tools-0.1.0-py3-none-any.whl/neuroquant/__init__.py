__all__ = ['neuroquant']

# Basic modules
import os, glob, re, warnings, shutil

# Checking if openpyxl exists
import importlib
if not importlib.util.find_spec("openpyxl"):
    os.system("pip install openpyxl")

if not importlib.util.find_spec("pydicom"):
    os.system("pip install -U pydicom")

# Module to manipule XLS files
from openpyxl import Workbook, load_workbook
# Module to read DICOM
import pydicom

class neuroquant:
    repo = ''
    xls  = ''
    
    def __init__( self, subj_data ):
        (self.subj, self.subjdir) = subj_data;
        self.__extract_subjid();
        self.__extract_dcm_header();
        
    def __extract_subjid( self ):
        self.subjid = self.subj.split('_')[0]
        
    def __extract_dcm_header( self ):
        items = glob.glob( '%s/*dcm' % self.get_3dt1_path() )
        dcm = pydicom.dcmread( items[0] )
        dir(dcm)
        self.PatientName = dcm.PatientName
        self.PatientBirthDate = dcm.PatientBirthDate
        self.PatientID = dcm.PatientID
        self.SeriesDate = dcm.SeriesDate
        
    def print_patient(self):
        print('Patient :     %s' % self.PatientName)
        print('ID Pac. :     %s' % self.PatientID)
        print('Birth Date :  %s' % self.PatientBirthDate)
        print('Series Date : %s' % self.SeriesDate)
        
    def nq_subjdir(self):
        return '%s/%s' % (Neuroquant.repo , self.subj)
    
    def mkdir( directory ):
        if not os.path.exists( directory ):
            os.mkdir( directory )

    # Copy 3DT1 to NeuroQuant repository
    def cp_3dt1(self):
        print("%s - Copying 3DT1" % self.subjid)
        folder_t1 = self.get_3dt1_path()
        out_dir = '%s/3DT1_orig' % self.nq_subjdir
        # Copy only if found 3DT1 image and destination directory don't exist
        if folder_t1 and not os.path.exists( out_dir ):
            Neuroquant.mkdir( self.nq_subjdir() )
            shutil.copytree( folder_t1, out_dir )
        
    def get_3dt1_path(self):
        items = glob.glob( '%s/t1_mprage*' % self.subjdir )
        if items:
            return items[0]
        return None
        
    def history(self):
        warnings.filterwarnings("ignore") # To surpress openpyxl warnings for xlsx files
        print('TODO: history')
        warnings.filterwarnings("default")