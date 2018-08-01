# coding=utf-8

import os
import typing


class Align:
    pass


class Order:
    pass


class Column:
    name: str
    template: typing.Optional[str] = None
    _title: typing.Optional[str] = None

    def __init__(self,
                 name: str,
                 title: str = None,
                 align: str = None,
                 template: typing.Union[str, typing.Callable] = None):

        self.name = name
        self.title = title
        self.template = template

    @property
    def title(self) -> str:
        return self.name if self._title is None else self._title

    @title.setter
    def title(self, value: typing.Optional[str]):
        self._title = value

    pass


class Cell:
    pass


class Row:
    pass


class Border:
    horizontal: str = '-'
    vertical: str = '|'


class Section:
    pass


class Table:
    order_by: typing.Optional[str] = None
    columns: typing.List[Column]
    rows: typing.List[typing.Dict[str, typing.Any]]
    _columns_width: typing.Dict[str, int]

    def __init__(self, order_by: typing.Optional[str]=None):
        self.order_by = order_by
        self.columns = []
        self.rows = []

    def render(self) -> str:
        result = ''

        self._calculate_columns_width()

        result += self._render_top_line() + os.linesep
        result += self._render_header_line() + os.linesep

        if len(self.rows) == 0:
            result += self._render_bottom_line()

            return result

        result += self._render_middle_line() + os.linesep

        rows = self.rows

        if self.order_by is not None:
            rows = sorted(rows, key=lambda x: x[self.order_by])

        for row in rows:
            result += self._render_row_line(row) + os.linesep

        result += self._render_bottom_line()

        return result

    def print(self):
        print(self.render())

    def _calculate_columns_width(self):
        self._columns_width = {}

        for column in self.columns:
            column_width = len(column.title)
            column_template = '{0}' if column.template is None else column.template

            for row in self.rows:
                if column.name not in row:
                    continue

                if callable(column_template):
                    value = column_template(row[column.name])
                else:
                    value = column_template.format(row[column.name])

                column_width = max(column_width, len(value))

            self._columns_width[column.name] = column_width
        pass

    def _render_top_line(self) -> str:
        result = ''

        if len(self.columns) == 0:
            return result

        result += '+'

        for column in self.columns:
            result += '-' * (self._columns_width[column.name] + 2)
            result += '+'

        return result

    def _render_middle_line(self):
        result = ''

        if len(self.columns) == 0:
            return result

        result += '+'

        for column in self.columns:
            result += '-' * (self._columns_width[column.name] + 2)
            result += '+'

        return result

    def _render_bottom_line(self):
        result = ''

        if len(self.columns) == 0:
            return result

        result += '+'

        for column in self.columns:
            result += '-' * (self._columns_width[column.name] + 2)
            result += '+'

        return result

    def _render_header_line(self) -> str:
        result = ''

        if len(self.columns) == 0:
            return result

        result += '|'

        for column in self.columns:
            result += f' {column.title:<{self._columns_width[column.name]}} '
            result += '|'

        return result

    def _render_row_line(self, row: typing.Dict[str, typing.Any]):
        result = ''

        if len(self.columns) == 0:
            return result

        result += '|'

        for column in self.columns:
            column_template = '{0}' if column.template is None else column.template

            value = row.get(column.name, '')

            if callable(column_template):
                value = column_template(value)
            else:
                value = column_template.format(value)

            result += f' {value:<{self._columns_width[column.name]}} '
            result += '|'

        return result

    pass
