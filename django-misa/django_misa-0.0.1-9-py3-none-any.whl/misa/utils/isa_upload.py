# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import zipfile
import os
import six

from django.contrib.auth.models import User
from django import forms

from mbrowse.utils.mfile_upload import upload_files_from_zip
from mbrowse.models import Polarity
from mbrowse.utils.mfile_upload import add_runs_mfiles_filelist

from misa.models import Study, AssayDetail, AssayRun
from misa.models import ExtractionProtocol, SpeProtocol, ChromatographyProtocol, MeasurementProtocol, SampleCollectionProtocol
from misa.models import ExtractionProcess, SpeProcess, ChromatographyProcess, MeasurementProcess, SampleCollectionProcess
from misa.models import StudySample
from misa.models import PolarityType





def upload_assay_data_files_zip(assayid, data_zipfile, data_mappingfile, user, create_assay_details):

    # Upload the files
    if zipfile.is_zipfile(data_zipfile):
        runs, mfiles = upload_files_from_zip(data_zipfile, user)
    else:
        print('data needs to be in zip file format')
        return 0

    mappingd = get_mapping_d(data_mappingfile, assayid=assayid, create_assay_details=create_assay_details)
    # then go through the mapping file and upload to relevant assay_run section adding replicates if present
    map_run_to_assaydetail(runs, mappingd)





def map_run_to_assaydetail(runs, mappingd):
    # get the unique runs we need
    unique_runs = list(set([run for filename, run in six.iteritems(runs)]))

    # loop through the runs
    for run in unique_runs:
        ## we presume that the correct checks have been performed before so that all files from the same
        ## run are will have the same assay details
        mfile = run.mfile_set.all()
        fn = mfile[0].original_filename
        # should only be 1 assay details
        md = mappingd[fn]

        ad = md['assaydetails']

        # this is a workaround so that we don't have to import MISA for metab. In the future it might be better
        # if we have a separate package just for mass spectrometry information (e.g. polarity, instruments etc)
        run.polarity = Polarity.objects.get(polarity=ad.measurementprocess.polaritytype.type.lower())
        run.save()


        arun = AssayRun(assaydetail=md['assaydetails'],
                        technical_replicate=md['rowdetails']['technical_replicate'],
                        run=run)
        arun.save()


def get_mapping_d(mapping_l, assayid, create_assay_details=False):



    mapping_d = {}
    for row in mapping_l:
        # update each time
        qs = AssayDetail.objects.filter(assay_id=assayid)
        fn = row['filename']
        if not fn:
            continue

        ad = search_assay_detail(row, qs)

        if create_assay_details and not ad:
            ad = create_assay_detail(row, assayid)

        mapping_d[fn] = {'assaydetails': ad,
                            'rowdetails':row}

    return mapping_d

def search_assay_detail(row, qs):
    code_field = row_2_codefield(row)

    match = qs.filter(code_field=code_field)
    if match:
        return match[0]
    else:
        return ''


def create_assay_detail(row, assayid):
    from misa.forms import AssayDetailForm
    sc = SampleCollectionProcess(samplecollectionprotocol=SampleCollectionProtocol.objects.get(code_field=row['sample_collection']))
    sc.save()

    cfrac, spefrac = frac2numbers(row)
    ei = ExtractionProcess(extractionprotocol=ExtractionProtocol.objects.get(code_field=row['extraction']))
    ei.save()

    # Create SPE process
    spei = SpeProcess(spefrac=spefrac, speprotocol=SpeProtocol.objects.get(code_field=row['spe']))
    spei.save()

    # Create chromtography process
    ci = ChromatographyProcess(chromatographyfrac=cfrac, chromatographyprotocol=
    ChromatographyProtocol.objects.get(code_field=row['chromatography']))
    ci.save()

    # create measurement process
    mi = MeasurementProcess(measurementprotocol=MeasurementProtocol.objects.get(code_field=row['measurement']),
                            polaritytype=PolarityType.objects.get(type=row['polarity']),
                            )
    mi.save()

    ss = StudySample.objects.get(sample_name=row['sample'], study=Study.objects.get(assay__id=assayid))

    data_in = {'assay': assayid,
               'studysample': ss.id,
               'samplecollectionprocess': sc.id,
               'extractionprocess': ei.id,
               'speprocess': spei.id,
               'chromatographyprocess': ci.id,
               'measurementprocess': mi.id}

    form = AssayDetailForm(data_in)
    form.is_valid()
    ad = form.save()
    return ad


def frac2numbers(row):
    if row['chromatography_frac'] == 'NA':
        cfrac = 0
    else:
        cfrac = row['chromatography_frac']

    if row['spe_frac'] == 'NA':
        spefrac = 0
    else:
        spefrac = row['spe_frac']

    return cfrac, spefrac


def row_2_codefield(row):
    cfrac, spefrac = frac2numbers(row)

    return '{}_{}_{}_{}_{}_{}_{}_{}'.format(      row['sample'],
                                                  row['sample_collection'],
                                                  row['extraction'],
                                                  row['spe'],
                                                  spefrac,
                                                  row['chromatography'],
                                                  cfrac,
                                                  row['measurement'],
                                                  row['polarity'].upper())


def file_upload_mapping_match(filenames, mapping_l):
    missing_files = []
    for fn in filenames:

        matched = False
        for row in mapping_l:

            map_filename = row['filename']
            if os.path.basename(fn) == map_filename:
                matched = True

        if not matched:
            missing_files.append(fn)

    return missing_files

def check_mapping_details(mapping_l, assayid):

    qs = AssayDetail.objects.filter(assay_id=assayid)

    missing_inf = []
    for row in mapping_l:
        fn = row['filename']
        if not fn:
            continue

        if not check_frac(row['spe_frac']) or not check_frac(row['chromatography_frac']):

            msg = 'Fraction columns (spe_frac & chromatography_frac) can only be integers or NA, please check these columns' \
                  'in the mapping file'
            raise forms.ValidationError(msg)

        if not search_assay_detail(row, qs):
           missing_inf.append(fn)

    return missing_inf



def check_frac(frac):
    if frac == 'NA':
        return True
    else:
        try:
            int(frac)
        except ValueError:
            return False
        else:
            return True



def upload_assay_data_files_dir(filelist, username, mapping_l, assayid, create_assay_details, save_as_link, celery_obj):
    """
    """
    user = User.objects.get(username=username)

    runs, mfiles = add_runs_mfiles_filelist(filelist, user, save_as_link, celery_obj)

    mappingd = get_mapping_d(mapping_l, assayid=assayid, create_assay_details=create_assay_details)

    if celery_obj:
        celery_obj.update_state(state='Mapping files to assay details',
                      meta={'current': 99, 'total': 100})

    # then go through the mapping file and upload to relevant assay_run section adding replicates if present
    map_run_to_assaydetail(runs, mappingd)