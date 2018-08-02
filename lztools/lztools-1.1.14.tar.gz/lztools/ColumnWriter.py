#!  /usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, namedtuple
from lztools.text import create_line, center_on, pad_length

Row = namedtuple("Row", ["text", "marks"])

class ColumnWriter(object):
    columns = None
    rows = None
    tests = None
    time = 0
    width = -1
    fail_char = "~"
    bufferd = False
    buffer = None

    def write_line(self, text=""):
        self.buffer.append(text)

    def __init__(self, width=80, fail_char="_"):
        self.rows = []
        self.buffer = []
        self.columns = []
        self.width = width
        self.fail_char = fail_char

    def mark_column(self, text, column, mark):
        if column not in self.columns:
            self.columns.append(column)
        row = None
        for r in self.rows:
            if r.text == text:
                row = r
        if row is None:
            row = Row(text, {column: mark})
            self.rows.append(row)
        if mark not in row.marks:
            row.marks[column] = mark

    def get_column_header(self):
        column_header = "[{}]".format("] [".join(self.columns))
        return pad_length(column_header, self.width, ">")

    def get_statistics(self, text_column_width):
        res = ""
        show_statistics = len(self.columns) > 0
        if show_statistics:
            count = len(self.rows)
            ccounts = defaultdict(int)
            for row in self.rows:
                for column in self.columns:
                    if column in row.marks:
                        if row.marks[column] != self.fail_char:
                            ccounts[column] += 1

            if len(self.columns) > 0:
                res += u"{}".format(create_line(" ", text_column_width, "Statistics:"))
            for c in self.columns:
                text = u"{:.2f}%".format((float(100)/count) * ccounts[c])
                res += center_on(text, u"[{}]".format(c)) + u" "
        return show_statistics, res[0:self.width]

    def _text_width(self):
        column_header = ""
        for c in self.columns:
            column_header += u"[{}] ".format(c)
        column_header = column_header.rstrip()
        return self.width - len(column_header)

    def _create_columns(self):
        ch = self.get_column_header()
        t_width = self._text_width()
        if ch.strip() != "":
            self.write_line(ch)
        for row in self.rows:
            l = create_line(".", t_width, row.text)
            for column in self.columns:
                if column in row.marks:
                    l += center_on(row.marks[column], u"[{}]".format(column)) + " "
                else:
                    l += center_on(self.fail_char, u"[{}]".format(column)) + " "
            self.write_line(l[0:self.width])
        enable_stats, stats = self.get_statistics(t_width)
        if enable_stats:
            self.write_line(stats)

    def flush(self):
        if len(self.columns) > 0:
            self._create_columns()
            o = "\n".join(self.buffer)
            self.buffer = []
            return o
