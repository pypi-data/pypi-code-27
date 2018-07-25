import yaml, re, textwrap

from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter
from collections import OrderedDict

from .markdown import *

TYPE_1 = 1
TYPE_2 = 2
TYPE_3 = 3

def call(source, export_type, table_classes=[], tr_classes=[], th_classes=[], td_classes=[]):

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    Dumper.add_representer(OrderedDict, dict_representer)
    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

    Dumper.add_representer(str, SafeRepresenter.represent_str)

    with open(source, 'r') as stream:
        try:
            data = yaml.load(stream.read(), Loader=Loader)
        except Exception as e:
            raise(RuntimeError(e))

        table_format = detect_table_format(data)
        table_type, table, column_size = convert_to_table(data, table_format)

        if export_type == 'html':
            print_html(table_type, table, table_classes, tr_classes, th_classes, td_classes)

        elif export_type == 'markdown':
            print_markdown(table_type, table, column_size)


def call_data(data, export_type, table_classes=[], tr_classes=[], th_classes=[], td_classes=[]):

    table_format = detect_table_format(data)
    table_type, table, column_size = convert_to_table(data, table_format)

    if export_type == 'html':
        result = print_html(table_type, table, table_classes, tr_classes, th_classes, td_classes)

    elif export_type == 'markdown':
        result = print_markdown(table_type, table, column_size)

    elif export_type =='tex':
        result = print_tex(table_type, table)

    return result

def detect_table_format(data):

    if isinstance(data, dict):
        key = list(data.keys())[0]
        return [dict] + detect_table_format(data[key])
    elif isinstance(data, list):
        return [list] + detect_table_format(data[0])
    else:
        return []


def convert_to_table(data, table_type):

    if table_type == [list]:

        result = []
        column_size = []

        for one_data in data:
            result.append([one_data])

        return TYPE_1, result, column_size

    elif table_type == [dict, list]:

        table = [[]]
        column_size = []
        i = 0
        j = 0

        for element in data:
            table[0].append(element)
            i = 1

            column_size.append(len(element))

            values = []
            for value in data[element]:
                if i + 1 > len(table):
                    table.append([])
                values.append(value)
                table[i].append(value)
                i += 1

                if column_size[j] < len(value):
                    column_size[j] = len(value)

            j += 1

        new_table = [table[0]]
        for element in table[1:]:
            new_table.append((element, 0, False))

        return TYPE_2, new_table, column_size

    else:

        column_size = []
        voyager = data
        for field_type in table_type[:-1]:

            if field_type == list:
                voyager = voyager[0]
            elif field_type == dict:
                voyager = list(voyager.values())[0]

        nb_colum = len(voyager) + 1

        current_line = 0
        table = []

        colums = [' '] + [str(annee) for annee in voyager.keys()]
        creator = TableCreator(colums, nb_colum)
        creator.handler(data)

        return TYPE_3, creator.table, column_size

class TableCreator:

    def __init__(self, colums, nb_colum):
        self.table = []
        self.table.append(colums)
        self.nb_colum = nb_colum

    def handler(self, data):

        self._handler(data, 0)

    def _handler(self, data, level):

        if isinstance(data, dict):

            for key, subdata in data.items():

                result = re.match('col\[.*\]', key)
                if result:
                    key = key.replace('col[', '').replace(']', '')

                if isinstance(subdata, dict):
                    is_sub = False
                    for subdata2 in subdata.values():
                        if isinstance(subdata2, dict):
                            is_sub = True
                            break

                    line = [' ' for j in range(0, self.nb_colum)]
                    line[0] = key

                    if is_sub:
                        self.table.append((line, level, is_sub))
                        self._handler(subdata, level + 1)
                    else:
                        i = 1
                        for key, value in subdata.items():
                            line[i] = value
                            i += 1
                        self.table.append((line, level, is_sub))
                else:
                    line = [' ' for j in range(0, self.nb_colum)]
                    line[0] = key
                    line[1] = subdata
                    self.table.append((line, -1, False))


def print_html(table_type, table, table_classes, tr_classes, th_classes, td_classes):
    result = ''

    result += '<table class="{}">'.format(' '.join(table_classes)) if table_classes else '<table>'
    result += '  <tr class="{}">'.format('') if tr_classes else '  <tr>'

    column = 0
    for subelem in table[0]:
        subelem_str = subelem

        if table_type == TYPE_1:
            result += '    <td class="{}">{}</td>'.format(' '.join(td_classes), subelem_str) if td_classes else '    <td>{}</td>'.format(subelem_str)
        else:
            result += '    <th class="{}">{}</th>'.format(' '.join(th_classes), subelem_str) if th_classes else '    <th>{}</th>'.format(subelem_str)
        column += 1
    result += '  </tr>'

    for elem in table[1:]:

        if table_type == TYPE_1:
            result += '  <tr>'.format(elem, '')
            result += '    <td class="{}">{}</td>'.format(' '.join(td_classes), elem) if td_classes else '    <td>{}</td>'.format(elem[0])
            result += '  </tr>'
        else:
            name = elem[0][0]
            if isinstance(name, str):
                classname = name.replace(' ', '-').lower().replace('(', '').replace(')', '').replace('\'', '-').replace('&', 'and')
            else:
                classname = name

            if elem[2]:
                if table_type == TYPE_3:
                    result += '  <tr class="chokola-level-{0} chokola-{1} {2}">'.format(elem[1], classname, ' '.join(tr_classes) if tr_classes else '')
                elif table_type == TYPE_2:
                    result += '  <tr class="chokola-level-{0} {1}">'.format(elem[1], '')

            else:
                if table_type == TYPE_3:
                    result += '  <tr class="chokola-leef chokola-{1} {2}">'.format(elem[1], classname, ' '.join(tr_classes) if tr_classes else '')
                elif table_type == TYPE_2:
                    result += '  <tr class="chokola-leef {0}">'.format('')

            column = 0
            for subelem in elem[0]:
                result += '    <td class="{}">{}</td>'.format(' '.join(td_classes), subelem) if td_classes else '    <td>{}</td>'.format(subelem)
                column += 1
            result += '  </tr>'

    result += '</table>'
    return result


def print_tex(table_type, table):

    start = textwrap.dedent('''
        \def\\arraystretch{1.5}
        \\scriptsize''')

    columns = '| l |'
    for subelem in table[0][1:]:
        columns += ' r '
    columns += '|'
    col = textwrap.dedent('''\\begin{longtable}{%s }''' % columns)

    head = ''
    head += '\\rowcolor{black!90}'
    header_model = '\multicolumn{1}{c}{\color{white} \\textbf{%s}}'
    for subelem in table[0][:-1]:
        head += header_model % subelem
        head += ' & '
    head += header_model % table[0][-1]
    head += ' \\\\'

    body = ''
    for elem in table[1:]:

        if elem[2]:
            if elem[1] == 0:
                level = 80
            elif elem[1] == 1:
                level = 50
            elif elem[1] == 2:
                level = 20
            body += '\\rowcolor{lightgray!%s}' % level

        value = elem[0][0]
        value = value.replace('&', '\\&')
        body += '\\textbf{%s} & ' % value
        for subelem in elem[0][1:-1]:
            body += '%s & ' % subelem
        body += '%s' % elem[0][-1]
        body += ' \\\\\n'
        body += '\\hline\n'

    end = textwrap.dedent('''
        \end{longtable}''')

    result = start
    result += col
    result += '\\hline'
    result += head
    result += '\\hline'
    result += body
    result += end
    return result


def print_markdown(table_type, table, column_size):
    return 'not implemented yet, sorry :('
