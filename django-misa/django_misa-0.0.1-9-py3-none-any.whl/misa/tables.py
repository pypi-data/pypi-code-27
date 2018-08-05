# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import django_tables2 as tables
from mbrowse.models import MFile
from misa.models import (
    ExtractionProtocol,
    ExtractionType,
    ChromatographyProtocol,
    ChromatographyType,
    SpeProtocol,
    SpeType,
    MeasurementProtocol,
    MeasurementTechnique,
    AssayDetail,
    Investigation,
    Assay,
    OntologyTerm,
    SampleCollectionProtocol,
    DataTransformationProtocol,
    StudySample,
    StudyFactor,
    Organism,
    OrganismPart,

)
from django.utils.safestring import mark_safe
from django_tables2_column_shifter.tables import ColumnShiftTable
from gfiles.models import GenericFile
from django_tables2.utils import A

class AssayFileTable(ColumnShiftTable):
    study = tables.Column(accessor='run.assayrun.assaydetail.assay.study.name',
                                  verbose_name='Study')

    assay = tables.Column(accessor='run.assayrun.assaydetail.assay.name',
                          verbose_name='Assay')

    sample_name = tables.Column(accessor='run.assayrun.assaydetail.studysample.sample_name',
                                verbose_name='Sample name')

    technical_replicate = tables.Column(accessor='run.assayrun.technical_replicate',
                                        verbose_name='tech replicate')

    samplecollection = tables.LinkColumn(accessor='run.assayrun.assaydetail.samplecollectionprocess.samplecollectionprotocol.code_field',
                                verbose_name='Sample collection', viewname='scp_list')

    lpe = tables.Column(accessor='run.assayrun.assaydetail.extractionprocess.extractionprotocol.code_field',
                                verbose_name='Liquid Phase Extraction (LPE)')


    spetype = tables.Column(accessor='run.assayrun.assaydetail.speprocess.speprotocol.code_field',
                            verbose_name='Solid Phase Extraction (SPE)')

    spefrac = tables.Column(accessor='run.assayrun.assaydetail.speprocess.spefrac',
                            verbose_name='SPE frac')

    chromatography = tables.Column(
        accessor='run.assayrun.assaydetail.chromatographyprocess.chromatographyprotocol.code_field',
        verbose_name='Chromatography')

    chromatographyfrac = tables.Column(accessor='run.assayrun.assaydetail.chromatographyprocess.chromatographyfrac',
                                       verbose_name='Chromatography frac')

    measurement = tables.Column(
        accessor='run.assayrun.assaydetail.measurementprocess.measurementprotocol.code_field',
        verbose_name='Measurement')

    polarity = tables.Column(accessor='run.assayrun.assaydetail.measurementprocess.polaritytype.type',
                             verbose_name='Polarity')

    code_field = tables.Column(accessor='run.assayrun.assaydetail.code_field',
                             verbose_name='Code field')


    class Meta:
        model = MFile
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id','original_filename', 'data_file')


class AssayDetailTable(ColumnShiftTable):


    study = tables.Column(accessor='assay.study.name',
                                  verbose_name='Study')

    assay = tables.Column(accessor='assay.name',
                          verbose_name='Assay')

    sample_name = tables.Column(accessor='studysample.sample_name',
                                verbose_name='Sample name')


    samplecollection = tables.Column(accessor='samplecollectionprocess.samplecollectionprotocol.code_field',
                                verbose_name='Sample collection')

    lpe = tables.Column(accessor='extractionprocess.extractionprotocol.code_field',
                                verbose_name='Liquid Phase Extraction (LPE)')


    spetype = tables.Column(accessor='speprocess.speprotocol.code_field',
                            verbose_name='Solid Phase Extraction (SPE)')

    spefrac = tables.Column(accessor='speprocess.spefrac',
                            verbose_name='SPE frac')

    chromatography = tables.Column(
        accessor='chromatographyprocess.chromatographyprotocol.code_field',
        verbose_name='Chromatography')

    chromatographyfrac = tables.Column(accessor='chromatographyprocess.chromatographyfrac',
                                       verbose_name='Chromatography frac')

    measurement = tables.Column(
        accessor='measurementprocess.measurementprotocol.code_field',
        verbose_name='Measurement')

    polarity = tables.Column(accessor='measurementprocess.polaritytype.type',
                             verbose_name='Polarity')

    code_field = tables.Column(accessor='code_field',
                             verbose_name='Code field')


    class Meta:
        model = AssayDetail
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id',)




class ISAFileSelectTable(ColumnShiftTable):

    user = tables.Column(accessor='user',
                         verbose_name='user')

    file = tables.Column(accessor='data_file',
                         verbose_name='Full path')

    non_mfile_investigation = tables.Column(accessor='misafile.investigation',
                         verbose_name='Investigation (non-mfile)')

    original_filename = tables.Column(accessor='original_filename',
                                      verbose_name='File name')

    filesuffix = tables.Column(accessor='mfile.mfilesuffix.suffix',
                               verbose_name='File suffix')

    investigation = tables.Column(accessor='mfile.run.assayrun.assaydetail.assay.study.investigation.name',
                            verbose_name='Investigation')

    study = tables.Column(accessor='mfile.run.assayrun.assaydetail.assay.study.name',
                                  verbose_name='Study')

    assay = tables.Column(accessor='mfile.run.assayrun.assaydetail.assay.name',
                          verbose_name='Assay')

    sample_name = tables.Column(accessor='mfile.run.assayrun.assaydetail.studysample.sample_name',
                                verbose_name='Sample name')

    technical_replicate = tables.Column(accessor='mfile.run.assayrun.technical_replicate',
                                        verbose_name='tech replicate')

    samplecollection = tables.LinkColumn(accessor='mfile.run.assayrun.assaydetail.samplecollectionprocess.samplecollectionprotocol.code_field',
                                verbose_name='Sample collection', viewname='scp_list')

    lpe = tables.Column(accessor='mfile.run.assayrun.assaydetail.extractionprocess.extractionprotocol.code_field',
                                verbose_name='Liquid Phase Extraction (LPE)')


    spetype = tables.Column(accessor='mfile.run.assayrun.assaydetail.speprocess.speprotocol.code_field',
                            verbose_name='Solid Phase Extraction (SPE)')

    spefrac = tables.Column(accessor='mfile.run.assayrun.assaydetail.speprocess.spefrac',
                            verbose_name='SPE frac')

    chromatography = tables.Column(
        accessor='mfile.run.assayrun.assaydetail.chromatographyprocess.chromatographyprotocol.code_field',
        verbose_name='Chromatography')

    chromatographyfrac = tables.Column(accessor='mfile.run.assayrun.assaydetail.chromatographyprocess.chromatographyfrac',
                                       verbose_name='Chromatography frac')

    measurement = tables.Column(
        accessor='mfile.run.assayrun.assaydetail.measurementprocess.measurementprotocol.code_field',
        verbose_name='Measurement')

    polarity = tables.Column(accessor='mfile.run.assayrun.assaydetail.measurementprocess.polaritytype.type',
                             verbose_name='Polarity')

    code_field = tables.Column(accessor='mfile.run.assayrun.assaydetail.code_field',
                             verbose_name='Code field')


    def get_column_default_show(self):
        self.column_default_show = ['id', 'user', 'original_filename', 'sample_name', 'technical_replicate', 'study', 'assay']
        return super(ISAFileSelectTable, self).get_column_default_show()

    class Meta:
        model = GenericFile
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id',)





class ISAFileSelectTableWithCheckBox(ISAFileSelectTable):

    check = tables.CheckBoxColumn(accessor="pk",
                                  attrs={
                                      "th__input": {"onclick": "toggle(this)"},
                                      "td__input": {"onclick": "addfile(this)"}},
                                  orderable=False)

    class Meta:
        model = GenericFile
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id',)

    def get_column_default_show(self):
        self.column_default_show = ['id', 'user', 'original_filename', 'sample_name', 'technical_replicate',
                                    'investigation', 'study', 'assay', 'check']
        return super(ISAFileSelectTableWithCheckBox, self).get_column_default_show()




class InvestigationTable(ColumnShiftTable):
    details = tables.LinkColumn('idetail_tables', text='details', args=[A('id')])
    export = tables.LinkColumn('export_isa_json', text='export', verbose_name='Export ISA-JSON', args=[A('id')])

    class Meta:
        model = Investigation
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id','name','description', 'details')


class AssayTable(tables.Table):
    upload = tables.LinkColumn('upload_assay_data_files',  text='upload', verbose_name='Upload Assay Data Files', args=[A('id')])
    details = tables.LinkColumn('assaydetail_summary', text='details',verbose_name='Assay details', args=[A('id')])
    files = tables.LinkColumn('assayfile_summary',  text='files', verbose_name='Assay files', args=[A('id')])
    delete = tables.LinkColumn('adelete', text='delete', verbose_name='Delete', args=[A('id')])



    class Meta:
        model = Assay
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'name',)


class OntologyTermTable(ColumnShiftTable):
    add = tables.LinkColumn('add_ontologyterm', text='add', verbose_name='Add Ontology Term',
                               args=[A('c')])

    c = tables.Column(verbose_name='Match count')

    class Meta:
        model = OntologyTerm
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class OntologyTermTableLocal(ColumnShiftTable):
    update = tables.LinkColumn('update_ontologyterm', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('delete_ontologyterm', text='delete', verbose_name='Delete', args=[A('id')])

    class Meta:
        model = OntologyTerm
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class ExtractionProtocolTable(tables.Table):
    extractiontype = tables.LinkColumn('et_list', verbose_name='Type')
    update = tables.LinkColumn('ep_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('ep_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = ExtractionProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class ExtractionTypeTable(tables.Table):

    update = tables.LinkColumn('et_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('et_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = ExtractionType
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'type', 'description', 'all_ontologyterms')


class SpeProtocolTable(tables.Table):
    spetype = tables.LinkColumn('spet_list', verbose_name='Type')
    update = tables.LinkColumn('spep_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('spep_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = SpeProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class SpeTypeTable(tables.Table):

    update = tables.LinkColumn('spet_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('spet_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = SpeType
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'type', 'description', 'all_ontologyterms')


class ChromatographyProtocolTable(tables.Table):
    chromatographytype = tables.LinkColumn('ct_list', verbose_name='Type')
    update = tables.LinkColumn('cp_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('cp_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = ChromatographyProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class ChromatographyTypeTable(tables.Table):

    update = tables.LinkColumn('ct_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('ct_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = ChromatographyType
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'type', 'description', 'all_ontologyterms')


class MeasurementProtocolTable(tables.Table):
    measurementtechnique = tables.LinkColumn('mt_list', verbose_name='Technique')
    update = tables.LinkColumn('mp_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('mp_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = MeasurementProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class MeasurementTechniqueTable(tables.Table):

    update = tables.LinkColumn('mt_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('mt_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = MeasurementTechnique
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'type', 'description', 'all_ontologyterms')


class SampleCollectionProtocolTable(tables.Table):

    update = tables.LinkColumn('scp_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('scp_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = SampleCollectionProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class DataTransformationProtocolTable(tables.Table):

    update = tables.LinkColumn('dtp_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('dtp_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = DataTransformationProtocol
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'


class MarkSafeLinkColumn(tables.LinkColumn):
    def render(self, value, record, bound_column):
        return self.render_link(
            self.compose_url(record, bound_column),
            record=record,
            value=mark_safe(value)
        )



class StudySampleTable(tables.Table):

    investigation = tables.Column(accessor='study.investigation.name', verbose_name='Investigation')
    study = tables.Column(accessor='study.name', verbose_name='Study')
    all_studyfactors = MarkSafeLinkColumn('sflist', verbose_name='Study Factors')
    organism = tables.LinkColumn('org_list')
    organism_part = tables.LinkColumn('orgpart_list')

    update = tables.LinkColumn('ssam_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('ssam_delete', text='delete', verbose_name='Delete', args=[A('id')])


    class Meta:
        model = StudySample
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'
        fields = ('id', 'investigation', 'study', 'sample_name', 'all_studyfactors', 'organism', 'organism_part', 'update', 'delete')


class StudyFactorTable(tables.Table):

    update = tables.LinkColumn('sfupdate', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('sfdelete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = StudyFactor
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'



class OrganismTable(tables.Table):

    update = tables.LinkColumn('org_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('org_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = Organism
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'



class OrganismPartTable(tables.Table):

    update = tables.LinkColumn('orgpart_update', text='update', verbose_name='Update', args=[A('id')])
    delete = tables.LinkColumn('orgpart_delete', text='delete', verbose_name='Delete', args=[A('id')])
    class Meta:
        model = OrganismPart
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/bootstrap.html'

