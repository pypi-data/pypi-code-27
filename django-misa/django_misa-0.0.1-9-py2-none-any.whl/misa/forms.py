# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import csv
from io import TextIOWrapper
from django import forms

from misa.models import (
    AssayDetail,
    StudyFactor,
    OntologyTerm,
    Study,
    Organism,
    OrganismPart,
    StudySample,
    ChromatographyProtocol,
    ChromatographyType,
    MeasurementTechnique,
    MeasurementProtocol,
    ExtractionProtocol,
    ExtractionType,
    SpeProtocol,
    SpeType,
    SampleCollectionProtocol,
    DataTransformationProtocol,
)
from misa.utils.isa_upload import check_mapping_details, file_upload_mapping_match


from mbrowse.forms import UploadMFilesBatchForm
from mbrowse.utils.mfile_upload import get_pths_from_field
from dal import autocomplete


class AssayDetailForm(forms.ModelForm):

    class Meta:
        model = AssayDetail
        fields = '__all__'
        exclude = ['code_field']


class UploadAssayDataFilesForm(UploadMFilesBatchForm):

    data_mappingfile = forms.FileField(label='Mapping file upload', required=False,
                                  help_text='csv file that maps the data files to the assay details. When empty'
                                            'will search for a file called "mapping.csv" within the selected'
                                            'directories (not possible when using the zip option)')

    create_assay_details = forms.BooleanField(label='Create assay details', initial=True, required=False,
                                  help_text='Assay details will be created on the fly')

    def __init__(self, user, *args, **kwargs):
        self.dir_pths = []
        self.mapping_l = []
        self.assayid = kwargs.pop('assayid')
        super(UploadAssayDataFilesForm, self).__init__(user, *args, **kwargs)


    def clean_datamappingfile(self):
        mappingfile = self.cleaned_data['data_mappingfile']

        # Check all required columns are present

        # Check if this type is available at all

        return self.cleaned_data['data_mappingfile']

    def clean(self):


        cleaned_data = super(UploadMFilesBatchForm, self).clean()
        data_zipfile = cleaned_data.get('data_zipfile')
        data_mappingfile = cleaned_data.get('data_mappingfile')
        use_directories = cleaned_data.get('use_directories')
        recursive = cleaned_data.get('recursive')
        create_assay_details = cleaned_data.get('create_assay_details')

        # check for any previous errors
        if any(self.errors):
            return self.errors


        # check directories
        dir_pths = get_pths_from_field(self.dir_fields, cleaned_data, self.user.username)
        self.check_zip_or_directories(data_zipfile, use_directories, dir_pths, recursive)


        #######################################################
        # Check matching files in zip and mapping file
        #######################################################
        filelist = self.filelist

        if not data_mappingfile and use_directories:
            found = False
            for dir_pth in dir_pths:
                for fn in os.listdir(dir_pth):
                    if fn == 'mapping.csv':
                        with open(os.path.join(dir_pth, fn)) as f:
                            mapping_l = list(csv.DictReader(f))
                        found = True
            if not found:
                msg = 'The mapping file was not found within the selected directories'
                raise forms.ValidationError(msg)

        elif not data_mappingfile:
            msg = 'The mapping file is required when using the zip option'
            raise forms.ValidationError(msg)
        else:

            mapping_l = list(csv.DictReader(TextIOWrapper(data_mappingfile, encoding='ascii', errors='replace')))

        missing_files = file_upload_mapping_match(filelist, mapping_l)
        missing_files = [os.path.basename(f) for f in missing_files]

        if missing_files:
            missing_files_str = ', '.join(missing_files)
            msg = 'The mapping file is missing the following files: {}'.format(missing_files_str)
            raise forms.ValidationError(msg)


        #######################################################
        # Check assay details are present
        #######################################################
        missing_inf = check_mapping_details(mapping_l, self.assayid)
        if missing_inf and not create_assay_details:
            missing_info_str = ', '.join(missing_inf)
            msg = 'The mapping file does not have corresponding assay details for the following files shown below' \
                  '(Please add the assay details, or run again with "create assay details") {}' \
                  ''.format(missing_info_str)
            raise forms.ValidationError(msg)

        # save some additional information to make processing the form easier
        self.mapping_l = mapping_l
        self.dir_pths = dir_pths

        return cleaned_data



class SearchOntologyTermForm(forms.Form):

    search_term = forms.CharField()


class StudySampleBatchCreateForm(forms.Form):

    study = forms.ModelChoiceField(queryset=Study.objects.all(), widget=autocomplete.ModelSelect2(url='study-autocomplete'))
    sample_list = forms.FileField()
    replace_duplicates = forms.BooleanField(required=False,
                                            help_text='If there is already a study sample with the same name for the '
                                                      'selected Study. Flag this option to remove the old sample '
                                                      'and replace with the one detailed in the new file. If this '
                                                      'option is not flagged the duplicate samples will be ignored')


class StudySampleForm(forms.ModelForm):

    class Meta:
        model = StudySample
        fields = ('study', 'sample_name', 'studyfactor', 'organism', 'organism_part', 'sampletype',)
        widgets = {
            'study': autocomplete.ModelSelect2(url='study-autocomplete'),
            'organism': autocomplete.ModelSelect2(url='organism-autocomplete'),
            'organism_part': autocomplete.ModelSelect2(url='organismpart-autocomplete'),
            'studyfactor': autocomplete.ModelSelect2Multiple(url='studyfactor-autocomplete'),
            'sampletype': autocomplete.ModelSelect2(url='sampletype-autocomplete'),
        }


class StudyFactorForm(forms.ModelForm):

    class Meta:
        model = StudyFactor
        fields = ('__all__')
        widgets = {
            'study': autocomplete.ModelSelect2(url='study-autocomplete'),
            'ontologyterm_type': autocomplete.ModelSelect2(url='ontologyterm-autocomplete'),
            'ontologyterm_value': autocomplete.ModelSelect2(url='ontologyterm-autocomplete'),
            'ontologyterm_unit': autocomplete.ModelSelect2(url='ontologyterm-autocomplete')
        }


class StudyForm(forms.ModelForm):

    class Meta:
        model = Study
        fields = ('__all__')
        widgets = {
            'investigation': autocomplete.ModelSelect2(url='investigation-autocomplete'),
            'submission_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'public_release_date':  forms.widgets.DateInput(attrs={'type': 'date'}),

            'study_design_descriptors': autocomplete.ModelSelect2Multiple(url='ontologyterm-autocomplete'),

        }


class OrganismForm(forms.ModelForm):
    class Meta:
        model = Organism
        fields = ('ontologyterm',)
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2(url='ontologyterm-autocomplete')
        }


class OrganismPartForm(forms.ModelForm):
    class Meta:
        model = OrganismPart
        fields = ('ontologyterm',)
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2(url='ontologyterm-autocomplete')
        }


class ChromatographyProtocolForm(forms.ModelForm):
    class Meta:
        model = ChromatographyProtocol
        fields = ('__all__')
        widgets = {
            'chromatographytype': autocomplete.ModelSelect2(url='chromatographytype-autocomplete'),
            # 'instrument_name': autocomplete.ModelSelect2(url='ontologyterm-autocomplete')
        }

class ChromatographyTypeForm(forms.ModelForm):
    class Meta:
        model = ChromatographyType
        fields = ('__all__')
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2Multiple(url='ontologyterm-autocomplete')
        }


class MeasurementTechniqueForm(forms.ModelForm):
    class Meta:
        model = MeasurementTechnique
        fields = ('__all__')
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2Multiple(url='ontologyterm-autocomplete')
        }


class MeasurementProtocolForm(forms.ModelForm):
    class Meta:
        model = MeasurementProtocol
        fields = ('__all__')
        widgets = {
            'measurementtechnique': autocomplete.ModelSelect2(url='measurementtechnique-autocomplete')
        }


class ExtractionProtocolForm(forms.ModelForm):
    class Meta:
        model = ExtractionProtocol
        fields = ('__all__')
        widgets = {
            'extractiontype': autocomplete.ModelSelect2(url='extractiontype-autocomplete')
        }


class ExtractionTypeForm(forms.ModelForm):
    class Meta:
        model = ExtractionType
        fields = ('__all__')
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2Multiple(url='ontologyterm-autocomplete')
        }


class SpeProtocolForm(forms.ModelForm):
    class Meta:
        model = SpeProtocol
        fields = ('__all__')
        widgets = {
            'spetype': autocomplete.ModelSelect2(url='spetype-autocomplete')
        }


class SpeTypeForm(forms.ModelForm):
    class Meta:
        model = SpeType
        fields = ('__all__')
        widgets = {
            'ontologyterm': autocomplete.ModelSelect2Multiple(url='ontologyterm-autocomplete')
        }


class SampleCollectionProtocolForm(forms.ModelForm):
    class Meta:
        model = SampleCollectionProtocol
        fields = ('__all__')


class DataTransformationProtocolForm(forms.ModelForm):
    class Meta:
        model = DataTransformationProtocol
        fields = ('__all__')
