# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
try:
    # Python 3
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest

from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View
from django_tables2 import RequestConfig
from django.urls import reverse_lazy

from misa.utils.sample_batch_create import sample_batch_create

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from dal import autocomplete

from gfiles.models import GenericFile
from mbrowse.models import MFile

from misa.models import (
    Investigation,
    Assay,
    AssayDetail,
    Study,
    StudySample,
    StudyFactor,
    SampleType,
    OntologyTerm,
    OrganismPart,
    Organism,
    ChromatographyProtocol,
    ChromatographyType,
    MeasurementProtocol,
    MeasurementTechnique,
    ExtractionProtocol,
    ExtractionType,
    SpeProtocol,
    SpeType,
    SampleCollectionProtocol,
    DataTransformationProtocol,


)

from misa.forms import (
    UploadAssayDataFilesForm,
    SearchOntologyTermForm,

    StudyFactorForm,
    StudyForm,
    OrganismPartForm,
    OrganismForm,
    StudySampleForm,
    ChromatographyProtocolForm,
    ChromatographyTypeForm,
    MeasurementProtocolForm,
    MeasurementTechniqueForm,
    ExtractionProtocolForm,
    ExtractionTypeForm,
    SpeProtocolForm,
    SpeTypeForm,
    SampleCollectionProtocolForm,
    DataTransformationProtocolForm,
    StudySampleBatchCreateForm
)

from misa.utils.isa_upload import upload_assay_data_files_zip
from misa.utils.create_isa_files import create_isa_files
from misa.utils.ontology_utils import search_ontology_term, search_ontology_term_shrt
from misa.tasks import upload_assay_data_files_dir_task
from misa.tables import (
    AssayFileTable,
    AssayDetailTable,
    ISAFileSelectTable,
    InvestigationTable,
    AssayTable,
    OntologyTermTable,
    OntologyTermTableLocal,
    SampleCollectionProtocolTable,
    ExtractionProtocolTable,
    ExtractionTypeTable,
    ChromatographyProtocolTable,
    ChromatographyTypeTable,
    SpeProtocolTable,
    SpeTypeTable,
    MeasurementProtocolTable,
    MeasurementTechniqueTable,
    DataTransformationProtocolTable,
    StudySampleTable,
    StudyFactorTable,
    OrganismTable,
    OrganismPartTable,


)
from misa.filter import (
    ISAFileFilter,
    InvestigationFilter,
    AssayFilter,
    ExtractionProtocolFilter,
    ExtractionTypeFilter,
    ChromatographyProtocolFilter,
    ChromatographyTypeFilter,
    SpeProtocolFilter,
    SpeTypeFilter,
    MeasurementProtocolFilter,
    MeasurementTechniqueFilter,
    SampleCollectionProtocolFilter,
    DataTransformationProtocolFilter,
    OntologyTermFilter,
    StudySampleFilter,
    StudyFactorFilter,
    OrganismFilter,
    OrganismPartFilter

)

from django.shortcuts import redirect

def success(request):
    return render(request, 'misa/success.html')



############################################################################################
# Export json
############################################################################################
class ISAJsonExport(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        inv = Investigation.objects.filter(pk=self.kwargs['pk'])

        if inv:
            isa_out, json_out = create_isa_files(inv[0].id)

        else:
            json_out = {}

        return HttpResponse(json_out, content_type="application/json")


############################################################################################
# Adding ontology terms
############################################################################################
class OntologyTermCreateView(LoginRequiredMixin, CreateView):
    model = OntologyTerm
    success_url = reverse_lazy('list_ontologyterm')
    fields = '__all__'

class OntologyTermUpdateView(LoginRequiredMixin, UpdateView):
    model = OntologyTerm
    success_url = reverse_lazy('list_ontologyterm')
    fields = '__all__'

class OntologyTermDeleteView(DeleteView):
    model = OntologyTerm
    success_url = reverse_lazy('list_ontologyterm')
    template_name = 'misa/confirm_delete.html'


class OntologyTermListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = OntologyTermTableLocal
    model = OntologyTerm
    filterset_class = OntologyTermFilter
    template_name = 'misa/ontologyterm_list.html'


class OntologyTermSearchView(LoginRequiredMixin, View):

    redirect_to = '/misa/search_ontologyterm_result/'

    template_name = 'misa/searchontologyterm_form.html'
    def get(self, request, *args, **kwargs):

        form = SearchOntologyTermForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SearchOntologyTermForm(request.POST, request.FILES)

        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            res = search_ontology_term(search_term)
            request.session['res'] = res  # set in session
            return redirect(self.redirect_to)

            # return render(request, 'misa/ontology_search_results.html', {'table': ont_table})
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})


class OntologyTermSearchResultView(LoginRequiredMixin, View):

    template_name = 'misa/ontology_search_results.html'
    def get(self, request, *args, **kwargs):
        res = request.session.get('res')
        ont_table = OntologyTermTable(res)
        RequestConfig(request).configure(ont_table)
        return render(request, self.template_name, {'table': ont_table})



class AddOntologyTermView(LoginRequiredMixin, CreateView):
    model = OntologyTerm
    success_url = reverse_lazy('list_ontologyterm')
    fields = '__all__'

    def get_initial(self):
        res = self.request.session.get('res')

        c = self.kwargs['c']
        for row in res:
            if row['c']==int(c):
                return row
        return {}





class OntologyTermAutocomplete(autocomplete.Select2QuerySetView):
    model_class = OntologyTerm

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return self.model_class.objects.none()

        qs = self.model_class.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


############################################################################################
# Organism Views
############################################################################################
class OrganismCreateView(LoginRequiredMixin, CreateView):
    model = Organism
    success_url = reverse_lazy('org_list')
    form_class = OrganismForm


class OrganismUpdateView(LoginRequiredMixin, UpdateView):
    model = Organism
    form_class = OrganismForm
    success_url = reverse_lazy('org_list')


class OrganismDeleteView(DeleteView):
    model = Organism
    success_url = reverse_lazy('org_list')
    template_name = 'misa/confirm_delete.html'


class OrganismListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = OrganismTable
    model = Organism
    filterset_class = OrganismFilter
    template_name = 'misa/organism_list.html'


############################################################################################
# Organism Part Views
############################################################################################
class OrganismPartCreateView(LoginRequiredMixin, CreateView):
    form_class = OrganismPartForm
    model = OrganismPart
    success_url = reverse_lazy('orgpart_list')


class OrganismPartUpdateView(LoginRequiredMixin, UpdateView):
    model = OrganismPart
    form_class = OrganismPartForm
    success_url = reverse_lazy('orgpart_list')


class OrganismPartDeleteView(DeleteView):
    model = OrganismPart
    success_url = reverse_lazy('orgpart_list')
    template_name = 'misa/confirm_delete.html'

class OrganismPartListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = OrganismPartTable
    model = OrganismPart
    filterset_class = OrganismPartFilter
    template_name = 'misa/organism_part_list.html'


class OrganismAutocomplete(OntologyTermAutocomplete):
    model_class = Organism


class OrganismPartAutocomplete(OntologyTermAutocomplete):
    model_class = OrganismPart


############################################################################################
# Protocol views
###########################################################################################
#=======================================
# Sample Collection Protocol
#=======================================
class SampleCollectionProtocolCreateView(LoginRequiredMixin, CreateView):
    model = SampleCollectionProtocol
    form_class = SampleCollectionProtocolForm
    success_url = reverse_lazy('scp_list')


class SampleCollectionProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = SampleCollectionProtocol
    form_class = SampleCollectionProtocolForm
    success_url = reverse_lazy('scp_list')


class SampleCollectionProtocolDeleteView(DeleteView):
    model = SampleCollectionProtocol
    success_url = reverse_lazy('scp_list')
    template_name = 'misa/confirm_delete.html'


class SampleCollectionProtocolListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = SampleCollectionProtocolTable
    model = SampleCollectionProtocol
    filterset_class = SampleCollectionProtocolFilter
    template_name = 'misa/sample_collection_protocol_list.html'



#=======================================
# Sample Collection Protocol
#=======================================
class DataTransformationProtocolCreateView(LoginRequiredMixin, CreateView):
    model = DataTransformationProtocol
    form_class = DataTransformationProtocolForm
    success_url = reverse_lazy('dp_list')


class DataTransformationProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = DataTransformationProtocol
    form_class = DataTransformationProtocolForm
    success_url = reverse_lazy('dp_list')


class DataTransformationProtocolDeleteView(DeleteView):
    model = DataTransformationProtocol
    success_url = reverse_lazy('dp_list')
    template_name = 'misa/confirm_delete.html'


class DataTransformationProtocolListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = DataTransformationProtocolTable
    model = DataTransformationProtocol
    filterset_class = DataTransformationProtocolFilter
    template_name = 'misa/data_transformation_protocol_list.html'




#=======================================
# Extraction Protocol
#=======================================
class ExtractionProtocolCreateView(LoginRequiredMixin, CreateView):
    model = ExtractionProtocol
    form_class = ExtractionProtocolForm
    success_url = reverse_lazy('ep_list')


class ExtractionProtocolListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = ExtractionProtocolTable
    model = ExtractionProtocol
    filterset_class = ExtractionProtocolFilter
    template_name = 'misa/extraction_protocol_list.html'


class ExtractionProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = ExtractionProtocol
    form_class = ExtractionProtocolForm
    success_url = reverse_lazy('ep_list')


class ExtractionProtocolDeleteView(DeleteView):
    model = ExtractionProtocol
    success_url = reverse_lazy('ep_list')
    template_name = 'misa/confirm_delete.html'


#=======================================
# Extraction Type
#=======================================
class ExtractionTypeCreateView(LoginRequiredMixin, CreateView):
    model = ExtractionType
    form_class = ExtractionTypeForm
    success_url = reverse_lazy('et_list')


class ExtractionTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ExtractionType
    form_class = ExtractionTypeForm
    success_url = reverse_lazy('et_list')

class ExtractionTypeDeleteView(DeleteView):
    model = ExtractionType
    success_url = reverse_lazy('et_list')
    template_name = 'misa/confirm_delete.html'


class ExtractionTypeListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = ExtractionTypeTable
    model = ExtractionType
    filterset_class = ExtractionTypeFilter
    template_name = 'misa/extraction_type_list.html'

class ExtractionTypeAutocomplete(OntologyTermAutocomplete):
    model_class = ExtractionType


#=======================================
# Chromatography protocol
#=======================================
class ChromatographyProtocolCreateView(LoginRequiredMixin, CreateView):
    model = ChromatographyProtocol
    form_class = ChromatographyProtocolForm
    success_url = reverse_lazy('cp_list')

class ChromatographyProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = ChromatographyProtocol
    form_class = ChromatographyProtocolForm
    success_url = reverse_lazy('cp_list')

class ChromatographyProtocolDeleteView(DeleteView):
    model = ChromatographyProtocol
    success_url = reverse_lazy('cp_list')
    template_name = 'misa/confirm_delete.html'

class ChromatographyProtocolListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = ChromatographyProtocolTable
    model = ChromatographyProtocol
    filterset_class = ChromatographyProtocolFilter
    template_name = 'misa/chromatography_protocol_list.html'


#=======================================
# Chromatography type
#=======================================
class ChromatographyTypeCreateView(LoginRequiredMixin, CreateView):
    model = ChromatographyType
    form_class = ChromatographyTypeForm
    success_url = reverse_lazy('ct_list')

class ChromatographyTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ChromatographyType
    form_class = ChromatographyTypeForm
    success_url = reverse_lazy('ct_list')

class ChromatographyTypeDeleteView(DeleteView):
    model = ChromatographyType
    success_url = reverse_lazy('ct_list')
    template_name = 'misa/confirm_delete.html'

class ChromatographyTypeListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = ChromatographyTypeTable
    model = ChromatographyType
    filterset_class = ChromatographyTypeFilter
    template_name = 'misa/chromatography_type_list.html'


class ChromatographyTypeAutocomplete(OntologyTermAutocomplete):
    model_class = ChromatographyType


#=======================================
# SPE protocol
#=======================================
class SpeProtocolCreateView(LoginRequiredMixin, CreateView):
    model = SpeProtocol
    form_class = SpeProtocolForm
    success_url = reverse_lazy('spep_list')


class SpeProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = SpeProtocol
    form_class = SpeProtocolForm
    success_url = reverse_lazy('spep_list')


class SpeProtocolDeleteView(DeleteView):
    model = SpeProtocol
    success_url = reverse_lazy('spep_list')
    template_name = 'misa/confirm_delete.html'


class SpeProtocolListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = SpeProtocolTable
    model = SpeProtocol
    filterset_class = SpeProtocolFilter
    template_name = 'misa/spe_protocol_list.html'


#=======================================
# SPE type
#=======================================
class SpeTypeCreateView(LoginRequiredMixin, CreateView):
    model = SpeType
    form_class = SpeTypeForm
    success_url = reverse_lazy('spet_list')


class SpeTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = SpeType
    form_class = SpeTypeForm
    success_url = reverse_lazy('spet_list')


class SpeTypeDeleteView(DeleteView):
    model = SpeType
    success_url = reverse_lazy('spet_list')
    template_name = 'misa/confirm_delete.html'


class SpeTypeListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = SpeTypeTable
    model = SpeType
    filterset_class = SpeTypeFilter
    template_name = 'misa/spe_type_list.html'


class SpeTypeAutocomplete(OntologyTermAutocomplete):
    model_class = SpeType



#=======================================
# Measurement protocol
#=======================================
class MeasurementProtocolCreateView(LoginRequiredMixin, CreateView):
    model = MeasurementProtocol
    form_class = MeasurementProtocolForm
    success_url = reverse_lazy('mp_list')


class MeasurementProtocolUpdateView(LoginRequiredMixin, UpdateView):
    model = MeasurementProtocol
    form_class = MeasurementProtocolForm
    success_url = reverse_lazy('mp_list')


class MeasurementProtocolDeleteView(DeleteView):
    model = MeasurementProtocol
    success_url = reverse_lazy('mp_list')
    template_name = 'misa/confirm_delete.html'


class MeasurementProtocolListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = MeasurementProtocolTable
    model = MeasurementProtocol
    filterset_class = MeasurementProtocolFilter
    template_name = 'misa/measurement_protocol_list.html'


#=======================================
# Measurement technique
#=======================================
class MeasurementTechniqueCreateView(LoginRequiredMixin, CreateView):
    model = MeasurementTechnique
    form_class = MeasurementTechniqueForm
    success_url = reverse_lazy('mt_list')


class MeasurementTechniqueUpdateView(LoginRequiredMixin, UpdateView):
    model = MeasurementTechnique
    form_class = MeasurementTechniqueForm
    success_url = reverse_lazy('mt_list')


class MeasurementTechniqueDeleteView(DeleteView):
    model = MeasurementTechnique
    success_url = reverse_lazy('mt_list')
    template_name = 'misa/confirm_delete.html'


class MeasurementTechniqueListView(LoginRequiredMixin,  SingleTableMixin,  FilterView):
    table_class = MeasurementTechniqueTable
    model = MeasurementTechnique
    filterset_class = MeasurementTechniqueFilter
    template_name = 'misa/measurement_technique_list.html'

class MeasurementTechniqueAutocomplete(OntologyTermAutocomplete):
    model_class = MeasurementTechnique










############################################################################################
# Investigation views
############################################################################################
class InvestigationCreateView(LoginRequiredMixin, CreateView):
    model = Investigation
    success_msg = "Investigation created"
    success_url = reverse_lazy('ilist')
    fields = '__all__'


class InvestigationUpdateView(LoginRequiredMixin, UpdateView):
    model = Investigation
    success_msg = "Investigation updated"
    success_url = reverse_lazy('ilist')
    fields = '__all__'


class InvestigationDetailView(LoginRequiredMixin, DetailView):
    model = Investigation
    fields = '__all__'


class InvestigationAutocomplete(OntologyTermAutocomplete):
    model_class = Investigation


class InvestigationDetailTablesView(LoginRequiredMixin, View):
    '''
    Run a registered workflow
    '''

    template_name = 'misa/investigation_detail_tables.html'


    def get_queryset(self):
        return Investigation.objects.get(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):

        l, investigation = self.page_setup(request)

        return render(request, self.template_name, {'list': l, 'investigation': investigation})

    def page_setup(self, request):
        # Need to setup a config for the tables (only 1 required per template page)
        rc = RequestConfig(request, paginate={'per_page': 20})

        investigation = self.get_queryset()

        atables = []
        afilters = []

        stables = []
        sfilters = []

        studies = []
        c = 0
        # loop through all the data_inputs from the associated workflow
        for s in investigation.study_set.all():
            assay_track = 'assay{}'.format(c)
            sample_track = 'sample{}'.format(c)

            assays = s.assay_set.all()

            # Create an invidivual filter for each table (assays)
            af = AssayFilter(request.GET, queryset=assays, prefix=c)

            atable = AssayTable(af.qs, prefix=c, attrs={'name': assay_track, 'id': assay_track, 'class': 'paleblue'})
            # load the table into the requestconfig
            rc.configure(atable)

            # Create an invidivual filter for each table (samples)
            sf = StudySampleFilter(request.GET, queryset=s.studysample_set.all(), prefix=c+1)
            stable = StudySampleTable(sf.qs, prefix=c, attrs={'name': sample_track, 'id': sample_track, 'class': 'paleblue'})
            # load the table into the requestconfig
            rc.configure(stable)

            # add the tables and filters to the list used in the template
            atables.append(atable)
            afilters.append(af)
            stables.append(stable)
            sfilters.append(sf)
            studies.append(s)

            c+=2

        # create a list of all the information. Using a simple list format as it is just easy to use in the template
        l = zip(studies, atables, afilters, stables, sfilters)
        return l, investigation



class InvestigationListViewOLD(LoginRequiredMixin, ListView):
    model = Investigation
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(InvestigationListViewOLD, self).get_context_data(**kwargs)
        context['now'] = 1
        # Investigation.objects.filter(self.kwargs['company']).order_by('-pk')
        return context

class InvestigationListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    # table_class = ISAFileSelectTable
    # model = GenericFile
    # template_name = 'misa/isa_file_select.html'
    # filterset_class =  ISAFileFilter

    table_class = InvestigationTable
    model = Investigation
    template_name = 'misa/investigation_list.html'
    filterset_class = InvestigationFilter

    # def post(self, request, *args, **kwargs):
        # workflow_sync(request.user)
        # redirects to show the current available workflows
        # return redirect('workflow_summary')


############################################################################################
# Study views
############################################################################################
class StudyCreateView(LoginRequiredMixin, CreateView):
    model = Study
    success_url = reverse_lazy('ilist')
    form_class = StudyForm


class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = Study
    success_url = reverse_lazy('ilist')
    form_class = StudyForm


class StudyListView(LoginRequiredMixin, ListView):
    model = Study
    fields = '__all__'


class StudyDeleteView(DeleteView):
    model = Study
    success_url = reverse_lazy('ilist')
    template_name = 'misa/confirm_delete.html'


class StudyAutocomplete(OntologyTermAutocomplete):
    model_class = Study


############################################################################################
# Assay views
############################################################################################
class AssayCreateView(LoginRequiredMixin, CreateView):
    model = Assay
    success_url = reverse_lazy('ilist')
    fields = '__all__'


class AssayUpdateView(LoginRequiredMixin, UpdateView):
    model = Assay
    success_url = reverse_lazy('ilist')
    fields = '__all__'

class AssayListView(LoginRequiredMixin, ListView):
    model = Assay
    fields = '__all__'


class UploadAssayDataFilesView(LoginRequiredMixin, View):

    # initial = {'key': 'value'}
    template_name = 'misa/upload_assay_data_files.html'

    def get(self, request, *args, **kwargs):
        form = UploadAssayDataFilesForm(user=self.request.user, assayid=self.kwargs['assayid'])

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadAssayDataFilesForm(request.user, request.POST, request.FILES, assayid=self.kwargs['assayid'])

        if form.is_valid():

            data_zipfile = form.cleaned_data['data_zipfile']
            data_mappingfile = form.cleaned_data['data_mappingfile']
            assayid = kwargs['assayid']
            create_assay_details = form.cleaned_data['create_assay_details']


            if data_zipfile:
                upload_assay_data_files_zip(assayid, data_zipfile,  form.mapping_l, request.user, create_assay_details)
                return render(request, 'misa/investigation_list.html')
            else:
                save_as_link = form.cleaned_data['save_as_link']
                # recursive = form.cleaned_data['recursive']
                # dir_pths = get_pths_from_field(form.dir_fields, form.cleaned_data, request.user.username)

                # rstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                # unique_folder = os.path.join(settings.MEDIA_ROOT, 'mapping', rstring)
                # os.makedirs(unique_folder)
                # data_mappingfile_pth = os.path.join(unique_folder, data_mappingfile.name)
                # with default_storage.open(data_mappingfile_pth, 'wb+') as destination:
                #     for chunk in data_mappingfile.chunks():
                #         print chunk
                #         destination.write(chunk)

                # mapping_l = list(csv.DictReader(data_mappingfile))

                result = upload_assay_data_files_dir_task.delay(form.filelist, request.user.username,
                                                                form.mapping_l, assayid, save_as_link,
                                                                create_assay_details)
                request.session['result'] = result.id
                return render(request, 'gfiles/status.html', {'s': 0, 'progress': 0})


        return render(request, self.template_name, {'form': form})


class AssayDeleteView(DeleteView):
    model = Assay
    success_url = reverse_lazy('ilist')
    template_name = 'misa/confirm_delete.html'



############################################################################################
# Study sample views
############################################################################################
class StudySampleCreateView(LoginRequiredMixin, CreateView):
    form_class = StudySampleForm
    model = StudySample
    success_url = reverse_lazy('ssam_list')


class StudySampleUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StudySampleForm
    model = StudySample
    success_url = reverse_lazy('ssam_list')


class StudySampleDeleteView(DeleteView):
    model = StudySample
    success_url = reverse_lazy('ssam_list')
    template_name = 'misa/confirm_delete.html'

class StudySampleListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = StudySampleTable
    model = StudySample
    filterset_class = StudySampleFilter
    template_name = 'misa/study_sample_list.html'


class StudySampleBatchCreate(LoginRequiredMixin, View):

    success_msg = "batch of samples created"
    # initial = {'key': 'value'}
    template_name = 'misa/study_sample_batch_create.html'

    def get(self, request, *args, **kwargs):
        form = StudySampleBatchCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudySampleBatchCreateForm(request.POST, request.FILES)

        if form.is_valid():

            study = form.cleaned_data['study']
            sample_list = form.cleaned_data['sample_list']
            replace_duplicates = form.cleaned_data['replace_duplicates']
            sample_batch_create(study, sample_list, replace_duplicates)

            return redirect('ssam_list')

        return render(request, self.template_name, {'form': form})


############################################################################################
# Study factor views
############################################################################################
class StudyFactorCreateView(LoginRequiredMixin, CreateView):
    model = StudyFactor
    form_class = StudyFactorForm
    success_url = reverse_lazy('sflist')


class StudyFactorUpdateView(LoginRequiredMixin, UpdateView):
    model = StudyFactor
    form_class =  StudyFactorForm
    success_url = reverse_lazy('sflist')


class StudyFactorDeleteView(DeleteView):
    model = StudyFactor
    success_url = reverse_lazy('sflist')
    template_name = 'misa/confirm_delete.html'


class StudyFactorListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = StudyFactorTable
    model = StudyFactor
    filterset_class = StudyFactorFilter
    template_name = 'misa/study_factor_list.html'


class StudyFactorAutocomplete(OntologyTermAutocomplete):
    model_class = StudyFactor

class SampleTypeAutocomplete(OntologyTermAutocomplete):
    model_class = SampleType



############################################################################################
# Assay file views
###########################################################################################
class ISAFileSummaryView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    View and initiate a run for all registered workflows.

    Workflows can also be synced here as well
    '''
    table_class = ISAFileSelectTable
    model = GenericFile
    template_name = 'misa/isa_file_select.html'
    filterset_class =  ISAFileFilter

    # def post(self, request, *args, **kwargs):
    #     workflow_sync(request.user)
    #     # redirects to show the current available workflows
    #     return redirect('workflow_summary')




class AssayFileSummaryView(LoginRequiredMixin, View):

    # initial = {'key': 'value'}
    template_name = 'misa/assay_files.html'

    def get(self, request, *args, **kwargs):
        mfiles = MFile.objects.filter(run__assayrun__assaydetail__assay_id=kwargs['assayid'])
        table = AssayFileTable(mfiles)
        RequestConfig(request).configure(table)

        i = Investigation.objects.get(study__assay__id=kwargs['assayid'])

        return render(request, self.template_name,  {'table': table, 'investigation_id':i.id})

    # def post(self, request, *args, **kwargs):
    #     form = UploadAssayDataFilesForm(request.POST, request.FILES, assayid=self.kwargs['assayid'])
    #
    #     if form.is_valid():
    #
    #         data_zipfile = form.cleaned_data['data_zipfile']
    #         data_mappingfile = form.cleaned_data['data_mappingfile']
    #         assayid = kwargs['assayid']
    #         upload_assay_data_files(assayid, data_zipfile, data_mappingfile)
    #
    #         # result = update_workflows_task.delay(self.kwargs['dmaid'])
    #         # request.session['result'] = result.id
    #         return render(request, 'dma/submitted.html')
    #
    #     return render(request, self.template_name, {'form': form})


class AssayDetailSummaryView(LoginRequiredMixin, View):

    # initial = {'key': 'value'}
    template_name = 'misa/assay_details.html'

    def get(self, request, *args, **kwargs):
        mfiles = AssayDetail.objects.filter(assay_id=kwargs['assayid'])
        table = AssayDetailTable(mfiles)
        RequestConfig(request).configure(table)
        i = Investigation.objects.get(study__assay__id=kwargs['assayid'])

        return render(request, self.template_name,  {'table': table, 'investigation_id':i.id})




