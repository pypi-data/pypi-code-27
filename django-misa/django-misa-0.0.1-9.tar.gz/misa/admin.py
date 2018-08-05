# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib import admin

from misa.models import SampleType, ExtractionType,SpeType, MeasurementTechnique, PolarityType, ChromatographyType
from misa.models import Investigation, Study, Assay, AssayDetail, StudySample, AssayRun, StudyFactor
from misa.models import  Organism, OntologyTerm
from misa.models import ExtractionProtocol, SpeProtocol, MeasurementProtocol, ChromatographyProtocol
from misa.models import ExtractionProcess, SpeProcess, MeasurementProcess, ChromatographyProcess

from misa.forms import StudyFactorForm

class StudyFactorAdmin(admin.ModelAdmin):
    form = StudyFactorForm


admin.site.register(SampleType)
admin.site.register(ExtractionType)
admin.site.register(SpeType)
admin.site.register(ChromatographyType)
admin.site.register(PolarityType)
admin.site.register(MeasurementTechnique)

admin.site.register(Organism)
admin.site.register(OntologyTerm)

admin.site.register(Investigation)
admin.site.register(Study)
admin.site.register(AssayDetail)
admin.site.register(AssayRun)
admin.site.register(Assay)
admin.site.register(StudySample)
admin.site.register(StudyFactor, StudyFactorAdmin)

admin.site.register(ExtractionProtocol)
admin.site.register(SpeProtocol)
admin.site.register(MeasurementProtocol)
admin.site.register(ChromatographyProtocol)

admin.site.register(ExtractionProcess)
admin.site.register(SpeProcess)
admin.site.register(MeasurementProcess)
admin.site.register(ChromatographyProcess)


