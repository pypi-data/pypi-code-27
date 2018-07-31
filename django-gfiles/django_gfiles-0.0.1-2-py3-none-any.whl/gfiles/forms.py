from django import forms
from gfiles.models import GenericFile


class GFileForm(forms.ModelForm):
    """ Form class for :class:`gfiles.models.GenericFiles
    """
    class Meta:
        model = GenericFile
        fields = ['data_file']