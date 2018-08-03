from mistune import Markdown, Renderer, InlineLexer, BlockLexer


class MdFmtInlineLexer(InlineLexer):

    default_rules = ['text']


class MdFmtBlockLexer(BlockLexer):

    default_rules = [
        'table', 'paragraph', 'text']


class MdFmtMarkdown(Markdown):

    def __init__(self, renderer, **kwargs):
        if 'inline' not in kwargs:
            kwargs['inline'] = MdFmtInlineLexer(renderer)
        if 'block' not in kwargs:
            kwargs['block'] = MdFmtBlockLexer()
        super(MdFmtMarkdown, self).__init__(renderer, **kwargs)


class MdFmtRenderer(Renderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = []
        self.align = []
        self.line = []
        self.tab = []
        self.columns = 0

    def paragraph(self, text):
        return text + '\n\n'

    def table(self, header, body):
        column_sizes = []
        column_number = len(self.header)

        for i in range(0, len(self.header)):
            column_size = len(self.header[i])
            for line in self.tab:
                if i < len(line) and len(line[i]) > column_size:
                    column_size = len(line[i])
            column_sizes.append(column_size)

        md = ''

        # header
        md += '|'
        for element, align, column_size in list(zip(self.header, self.align, column_sizes)):
            md += ' '
            if align == 'center':
                md += element.center(column_size)
            elif align == 'left':
                md += element.ljust(column_size)
            elif align == 'right':
                md += element.rjust(column_size)
            else:
                md += element.ljust(column_size)
            md += ' |'
        md += '\n'

        # alignment
        md += '|'
        for align, column_size in list(zip(self.align, column_sizes)):
            before = ' '
            after = ' '
            if align == 'center':
                before = ':'
                after = ':'
            elif align == 'left':
                before = ':'
                after = ' '
            elif align == 'right':
                before = ' '
                after = ':'

            md += before + ('-' * column_size) + after + '|'
        md += '\n'

        # table
        for line in self.tab:
            md += '|'
            while len(line) < self.columns:
                line.append('')
            for element, align, column_size in list(zip(line, self.align, column_sizes)):
                md += ' '
                if align == 'center':
                    md += element.center(column_size)
                elif align == 'left':
                    md += element.ljust(column_size)
                elif align == 'right':
                    md += element.rjust(column_size)
                else:
                    md += element.ljust(column_size)
                md += ' |'
            md += '\n'

        self.header = []
        self.align = []
        self.line = []
        self.tab = []
        md += '\n'

        return md

    def table_row(self, content):
        if self.columns < len(self.line):
            self.columns = len(self.line)

        if self.line != []:
            self.tab.append(self.line.copy())
            self.line = []
        return ''

    def table_cell(self, content, header, align):
        if header:
            self.header.append(content)
            self.align.append(align)
        else:
            self.line.append(content)

        return ''
