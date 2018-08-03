from .formatter import Formatter


class Renderer():

    def __init__(self, formatter):
        self.markdown = '|'
        self.formatter = formatter

    def __call__(self, data):
        self.header(data)
        self.alignment(data)
        self.rows(data)
        return self.markdown

    def header(self, data):
        for column_number, cell in enumerate(data[0]):
            content = self.formatter.col_header(cell, column_number)
            self.markdown += ' {} |'.format(content)
        self.markdown += '\n'

    def alignment(self, data):
        self.markdown += '|'
        for column_number, _ in enumerate(data[0]):
            align = self.formatter.alignment(column_number)
            if align == Formatter.CENTER or align == Formatter.LEFT:
                self.markdown += ':'
            else:
                self.markdown += ' '
            self.markdown += '-'
            if align == Formatter.CENTER or align == Formatter.RIGHT:
                self.markdown += ':|'
            else:
                self.markdown += ' |'
        self.markdown += '\n'

    def rows(self, data):
        for row_number, row in enumerate(data[1:]):
            self.markdown += '|'
            for column_number, cell in enumerate(row):
                content = self.formatter.cell(cell, column_number, row_number)
                if column_number == 0:
                    content = self.formatter.row_header(content, row_number)
                self.markdown += ' {} |'.format(content)
            self.markdown += '\n'