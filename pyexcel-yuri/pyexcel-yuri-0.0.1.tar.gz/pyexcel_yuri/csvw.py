"""
    pyexcel_yuri.csvw
    ~~~~~~~~~~~~~~~~~~~

    The lower level xlsx file format writer using xlsxwriter

    :copyright: (c) 2016 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
import pandas

from pyexcel_io.book import BookWriter
from pyexcel_io.sheet import SheetWriter


class CSVSheetWriter(SheetWriter):
    """
    xlsx sheet writer
    """
    def set_sheet_name(self, name):
        self.current_row = 0

    def write_row(self, array):
        """
        write a row into the file
        """
        self._native_sheet.append(array)
        self.current_row += 1


class CSVWriter(BookWriter):
    """
    xlsx writer
    """
    def __init__(self):
        BookWriter.__init__(self)
        self._native_book = None
        self.file_name = None

    def open(self, file_name, **keywords):
        """
        Open a file for writing
        """
        BookWriter.open(self, file_name, **keywords)
        self.file_name = file_name
        self._native_book = {}

    def create_sheet(self, name):
        if len(self._native_book) >= 1:
            raise ValueError('CSV file can only contain one sheet')
        self._native_book[name] = []
        return CSVSheetWriter(self._native_book, self._native_book[name], name)

    @staticmethod
    def filter_kwargs(keywords):
        return {
            'sep': keywords.get('delimiter', ','),
            'encoding': keywords.get('encoding', 'utf-8'),
            'compression': keywords.get('compression')
        }

    def close(self):
        """
        This call actually save the file
        """
        for name, sheet in self._native_book.items():
            pd = pandas.DataFrame(sheet)
            pd.to_csv(self.file_name, header=None, index=False, **self.filter_kwargs(self._keywords))
        self._native_book = None
