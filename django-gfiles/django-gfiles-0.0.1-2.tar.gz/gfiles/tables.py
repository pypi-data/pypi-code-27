import django_tables2 as tables
from .models import GenericFile
from django_tables2_column_shifter.tables import ColumnShiftTable


class GFileTable(ColumnShiftTable):
    """ Class for django-tables2 table of :class:`gfiles.models.GenericFiles`.

    Inherits the ColumnShiftTable, that is a modified django-tables2 class that allows columns to be dynamically
    selected
    """
    filename = tables.Column(accessor='original_filename', verbose_name='Filename')

    class Meta:
        model = GenericFile
        attrs = {'class': 'paleblue'}
        template = 'django_tables2/boostrap.html'

        fields = ('id', )


class GFileTableWithCheck(GFileTable):
    """ Class for django-tables2 table of :class:`gfiles.models.GenericFiles` with a check box column

    Inherits :class:`gfiles.models.GFileTable` and just adds checkbox.
    """
    check = tables.CheckBoxColumn(accessor="pk",
                                           attrs={
                                               "th__input": {"onclick": "toggle(this)"},
                                               "td__input": {"onclick": "addfile(this)"}},
                                           orderable=False)

    class Meta:
        model = GenericFile
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'paleblue'}
        fields = ('id', 'filename', 'user', 'check')








