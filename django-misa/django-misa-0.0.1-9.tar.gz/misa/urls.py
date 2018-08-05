from django.conf.urls import url
from misa import views

from misa.models import OntologyTerm
from dal import autocomplete

urlpatterns = [

    url(r'^$', views.InvestigationListView.as_view(), name='ilist'),

    # Ontology
    url(r'^create_ontologyterm/$', views.OntologyTermCreateView.as_view(), name='create_ontologyterm'),
    url(r'^update_ontologyterm/$', views.OntologyTermUpdateView.as_view(), name='update_ontologyterm'),
    url(r'^delete_ontologyterm/$', views.OntologyTermDeleteView.as_view(), name='delete_ontologyterm'),
    url(r'^list_ontologyterm/$', views.OntologyTermListView.as_view(), name='list_ontologyterm'),

    # ontology term searching EBI ontology service
    url(r'^search_ontologyterm/$', views.OntologyTermSearchView.as_view(), name='search_ontologyterm'),
    url(r'^search_ontologyterm_result/$', views.OntologyTermSearchResultView.as_view(), name='search_ontologyterm_result'),
    url(r'^add_ontologyterm/(?P<c>\d+)/$', views.AddOntologyTermView.as_view(), name='add_ontologyterm'),

    url(r'^update_ontologyterm/(?P<pk>\d+)/$', views.OntologyTermUpdateView.as_view(), name='update_ontologyterm'),
    url(r'^delete_ontologyterm/(?P<pk>[\w]+)/$', views.OntologyTermDeleteView.as_view(), name='delete_ontologyterm'),
    url(r'^list_ontologyterm/$', views.OntologyTermListView.as_view(), name='list_ontologyterm'),

    url(r'^ontologyterm-autocomplete/$', views.OntologyTermAutocomplete.as_view(), name='ontologyterm-autocomplete'),
    url(r'^ontologyterm-autocompleteTEST/$', autocomplete.Select2QuerySetView.as_view(model=OntologyTerm),name='select2_fk',),

    # Organism
    url(r'^org_create/$', views.OrganismCreateView.as_view(), name='org_create'),
    url(r'^org_list/$', views.OrganismListView.as_view(), name='org_list'),
    url(r'^org_update/(?P<pk>\d+)/$', views.OrganismUpdateView.as_view(), name='org_update'),
    url(r'^org_delete/(?P<pk>[\w]+)/$', views.OrganismDeleteView.as_view(), name='org_delete'),
    url(r'^organism-autocomplete/$', views.OrganismAutocomplete.as_view(), name='organism-autocomplete'),

    # Organism part
    url(r'^orgpart_create/$', views.OrganismPartCreateView.as_view(), name='orgpart_create'),
    url(r'^orgpart_list/$', views.OrganismPartListView.as_view(), name='orgpart_list'),
    url(r'^orgpart_update/(?P<pk>\d+)/$', views.OrganismPartUpdateView.as_view(), name='orgpart_update'),
    url(r'^orgpart_delete/(?P<pk>[\w]+)/$', views.OrganismPartDeleteView.as_view(), name='orgpart_delete'),
    url(r'^organismpart-autocomplete/$', views.OrganismPartAutocomplete.as_view(), name='organismpart-autocomplete'),

    # sample collection protocol
    url(r'^scp_create/$', views.SampleCollectionProtocolCreateView.as_view(), name='scp_create'),
    url(r'^scp_list/$', views.SampleCollectionProtocolListView.as_view(), name='scp_list'),
    url(r'^scp_update/(?P<pk>\d+)/$', views.SampleCollectionProtocolUpdateView.as_view(), name='scp_update'),
    url(r'^scp_delete/(?P<pk>[\w]+)/$', views.SampleCollectionProtocolDeleteView.as_view(), name='scp_delete'),

    # extraction protocol
    url(r'^ep_create/$', views.ExtractionProtocolCreateView.as_view(), name='ep_create'),
    url(r'^ep_list/$', views.ExtractionProtocolListView.as_view(), name='ep_list'),
    url(r'^ep_update/(?P<pk>\d+)/$', views.ExtractionProtocolUpdateView.as_view(), name='ep_update'),
    url(r'^ep_delete/(?P<pk>[\w]+)/$', views.ExtractionProtocolDeleteView.as_view(), name='ep_delete'),

    # extraction type
    url(r'^et_create/$', views.ExtractionTypeCreateView.as_view(), name='et_create'),
    url(r'^et_list/$', views.ExtractionTypeListView.as_view(), name='et_list'),
    url(r'^et_update/(?P<pk>\d+)/$', views.ExtractionTypeUpdateView.as_view(), name='et_update'),
    url(r'^et_delete/(?P<pk>[\w]+)/$', views.ExtractionTypeDeleteView.as_view(), name='et_delete'),
    url(r'^extractiontype-autocomplete/$', views.ExtractionTypeAutocomplete.as_view(),
        name='extractiontype-autocomplete'),

    # chromatography protocol
    url(r'^cp_create/$', views.ChromatographyProtocolCreateView.as_view(), name='cp_create'),
    url(r'^cp_list/$', views.ChromatographyProtocolListView.as_view(), name='cp_list'),
    url(r'^cp_update/(?P<pk>\d+)/$', views.ChromatographyProtocolUpdateView.as_view(), name='cp_update'),
    url(r'^cp_delete/(?P<pk>[\w]+)/$', views.ChromatographyProtocolDeleteView.as_view(), name='cp_delete'),

    # chromatography type
    url(r'^ct_create/$', views.ChromatographyTypeCreateView.as_view(), name='ct_create'),
    url(r'^ct_list/$', views.ChromatographyTypeListView.as_view(), name='ct_list'),
    url(r'^ct_update/(?P<pk>\d+)/$', views.ChromatographyTypeUpdateView.as_view(), name='ct_update'),
    url(r'^ct_delete/(?P<pk>[\w]+)/$', views.ChromatographyTypeDeleteView.as_view(), name='ct_delete'),
    url(r'^chromatographytype-autocomplete/$', views.ChromatographyTypeAutocomplete.as_view(), name='chromatographytype-autocomplete'),

    # spe protocol
    url(r'^spep_create/$', views.SpeProtocolCreateView.as_view(), name='spep_create'),
    url(r'^spep_list/$', views.SpeProtocolListView.as_view(), name='spep_list'),
    url(r'^spep_update/(?P<pk>\d+)/$', views.SpeProtocolUpdateView.as_view(), name='spep_update'),
    url(r'^spep_delete/(?P<pk>[\w]+)/$', views.SpeProtocolDeleteView.as_view(), name='spep_delete'),

    # spe type
    url(r'^spet_create/$', views.SpeTypeCreateView.as_view(), name='spet_create'),
    url(r'^spet_list/$', views.SpeTypeListView.as_view(), name='spet_list'),
    url(r'^spet_update/(?P<pk>\d+)/$', views.SpeTypeUpdateView.as_view(), name='spet_update'),
    url(r'^spet_delete/(?P<pk>[\w]+)/$', views.SpeTypeDeleteView.as_view(), name='spet_delete'),
    url(r'^spetype-autocomplete/$', views.SpeTypeAutocomplete.as_view(), name='spetype-autocomplete'),

    # measurement protocol
    url(r'^mp_create/$', views.MeasurementProtocolCreateView.as_view(), name='mp_create'),
    url(r'^mp_list/$', views.MeasurementProtocolListView.as_view(), name='mp_list'),
    url(r'^mp_update/(?P<pk>\d+)/$', views.MeasurementProtocolUpdateView.as_view(), name='mp_update'),
    url(r'^mp_delete/(?P<pk>[\w]+)/$', views.MeasurementProtocolDeleteView.as_view(), name='mp_delete'),

    # measurement technique
    url(r'^mt_create/$', views.MeasurementTechniqueCreateView.as_view(), name='mt_create'),
    url(r'^mt_list/$', views.MeasurementTechniqueListView.as_view(), name='mt_list'),
    url(r'^mt_update/(?P<pk>\d+)/$', views.MeasurementTechniqueUpdateView.as_view(), name='mt_update'),
    url(r'^mt_delete/(?P<pk>[\w]+)/$', views.MeasurementTechniqueDeleteView.as_view(), name='mt_delete'),
    url(r'^measurementtechnique-autocomplete/$', views.MeasurementTechniqueAutocomplete.as_view(),
        name='measurementtechnique-autocomplete'),

    # data transformation protocol
    url(r'^dp_create/$', views.DataTransformationProtocolCreateView.as_view(), name='dp_create'),
    url(r'^dp_list/$', views.DataTransformationProtocolListView.as_view(), name='dp_list'),
    url(r'^dp_update/(?P<pk>\d+)/$', views.DataTransformationProtocolUpdateView.as_view(), name='dp_update'),
    url(r'^dp_delete/(?P<pk>[\w]+)/$', views.DataTransformationProtocolDeleteView.as_view(), name='dp_delete'),

    # ISA export
    url(r'^export_isa_json/(?P<pk>\d+)/$', views.ISAJsonExport.as_view(), name='export_isa_json'),

    # Investigation
    url(r'^icreate/$', views.InvestigationCreateView.as_view(), name='icreate'),
    url(r'^iupdate/(?P<pk>\d+)/$', views.InvestigationUpdateView.as_view(), name='iupdate'),
    url(r'^idetail/(?P<pk>\d+)/$', views.InvestigationDetailView.as_view(), name='idetail'),
    url(r'^idetail_tables/(?P<pk>\d+)/$', views.InvestigationDetailTablesView.as_view(), name='idetail_tables'),
    url(r'^investigation-autocomplete/$', views.InvestigationAutocomplete.as_view(), name='investigation-autocomplete'),

    # Study
    url(r'^screate/$', views.StudyCreateView.as_view(), name='screate'),
    url(r'^supdate/(?P<pk>\d+)/$', views.StudyUpdateView.as_view(), name='supdate'),
    url(r'^sdelete/(?P<pk>[\w]+)/$', views.StudyDeleteView.as_view(), name='sdelete'),
    url(r'^slist/$', views.StudyListView.as_view(), name='slist'),
    url(r'^study-autocomplete/$', views.StudyAutocomplete.as_view(), name='study-autocomplete'),

    # Assay
    url(r'^acreate/$', views.AssayCreateView.as_view(), name='acreate'),
    url(r'^aupdate/(?P<pk>\d+)/$', views.AssayUpdateView.as_view(), name='aupdate'),
    url(r'^alist/$', views.AssayListView.as_view(), name='alist'),

    # Study Sample
    url(r'^ssam_create/$', views.StudySampleCreateView.as_view(), name='ssam_create'),
    url(r'^ssam_update/(?P<pk>\d+)/$', views.StudySampleUpdateView.as_view(), name='ssam_update'),
    url(r'^ssam_list/$', views.StudySampleListView.as_view(), name='ssam_list'),
    url(r'^ssam_delete/(?P<pk>[\w]+)/$', views.StudySampleListView.as_view(), name='ssam_delete'),
    url(r'^ssam_batch_create/$', views.StudySampleBatchCreate.as_view(), name='ssam_batch_create'),
    url(r'^sampletype-autocomplete/$', views.SampleTypeAutocomplete.as_view(), name='sampletype-autocomplete'),


    # Study Factor
    url(r'^sfcreate/$', views.StudyFactorCreateView.as_view(), name='sfcreate'),
    url(r'^sfupdate/(?P<pk>\d+)/$', views.StudyFactorUpdateView.as_view(), name='sfupdate'),
    url(r'^sfdelete/(?P<pk>\d+)/$', views.StudyFactorDeleteView.as_view(), name='sfdelete'),
    url(r'^sflist/$', views.StudyFactorListView.as_view(), name='sflist'),
    url(r'^studyfactor-autocomplete/$', views.StudyFactorAutocomplete.as_view(), name='studyfactor-autocomplete'),


    url(r'^upload_assay_data_files/(?P<assayid>\d+)$', views.UploadAssayDataFilesView.as_view(), name='upload_assay_data_files'),

    url(r'^view_isa_data_files/$', views.ISAFileSummaryView.as_view(), name='view_isa_data_files'),


    url(r'^assayfile_summary/(?P<assayid>\d+)$', views.AssayFileSummaryView.as_view(), name='assayfile_summary'),
    url(r'^assaydetail_summary/(?P<assayid>\d+)$', views.AssayDetailSummaryView.as_view(), name='assaydetail_summary'),


    url(r'^success/$', views.success, name='success'),
    url(r'^adelete/(?P<pk>[\w]+)/$', views.AssayDeleteView.as_view(), name='adelete')

]