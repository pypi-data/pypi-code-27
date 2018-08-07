"""
    pyexcel_yuri.csvr
    ~~~~~~~~~~~~~~~~~~~

    Read csv file format using pandas

    :license: New BSD License
"""
import pandas
import math

from pyexcel_io.book import BookReader
from pyexcel_io.sheet import SheetReader
from pyexcel_io._compact import OrderedDict, irange


class CSVSheet(SheetReader):
    """
    Iterate through rows
    """
    @property
    def name(self):
        """sheet name"""
        return 'CSVSheet'

    def row_iterator(self):
        for row in self._native_sheet.values:
            yield row

    def column_iterator(self, row):
        for value in row:
            yield None if isinstance(value, float) and math.isnan(value) else value


class CSVBook(BookReader):
    """
    Open csv in pandas
    """
    def open(self, file_name, **keywords):
        BookReader.open(self, file_name, **keywords)
        self._load_the_file(file_name, **keywords)

    def open_stream(self, file_stream, **keywords):
        BookReader.open_stream(self, file_stream, **keywords)
        self._load_the_file(file_stream, **keywords)

    def read_sheet(self, native_sheet, sheet_name='CSVSheet'):
        sheet = CSVSheet(native_sheet, **self._keywords)
        return {sheet_name: sheet.to_array()}

    def read_sheet_by_name(self, sheet_name='CSVSheet'):
        sheet = self._native_book[0]
        return self.read_sheet(sheet, sheet_name)

    def read_sheet_by_index(self, sheet_index=0):
        return self.read_sheet_by_name()

    def read_all(self):
        result = OrderedDict()
        for sheet in self._native_book:
            data_dict = self.read_sheet(sheet)
            result.update(data_dict)
        return result

    def close(self):
        self._native_book = None

    @staticmethod
    def filter_kwargs(keywords):
        return {
            'sep': keywords.get('delimiter', ','),
            'error_bad_lines': keywords.get('skip_bad_lines', True),
            'encoding': keywords.get('encoding', 'utf-8'),
            'memory_map': keywords.get('memory_map', False),
            'compression': keywords.get('compression', 'infer')
        }

    def _load_the_file(self, file_alike_object, **keywords):
        self._native_book = [pandas.read_csv(file_alike_object, dtype=str, header=None, **self.filter_kwargs(keywords))]
