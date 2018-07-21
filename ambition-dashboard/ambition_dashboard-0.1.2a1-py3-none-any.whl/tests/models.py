from django.db import models
from django.db.models.deletion import PROTECT
from edc_appointment.models import Appointment
from edc_base.model_mixins import BaseUuidModel


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(
        max_length=25,
        null=True,
        editable=False)


class BloodResultModel(models.Model):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    platelets = models.IntegerField(
        null=True,)

    neutrophil = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        null=True,)

    alt = models.IntegerField(
        null=True)


class DeathReport(models.Model):

    subject_identifier = models.CharField(max_length=25)


class StudyTerminationConclusion(models.Model):

    subject_identifier = models.CharField(max_length=25)


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class SubjectOffstudy(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class SubjectRequisition(BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    panel_name = models.CharField(max_length=25)


class SubjectScreening(BaseUuidModel):

    screening_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)


class SubjectConsent(BaseUuidModel):

    subject_screening = models.ForeignKey(
        SubjectScreening, null=True, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25, default='M')

    initials = models.CharField(max_length=25, default='XX')

    first_name = models.CharField(max_length=25, default='NOAM')
