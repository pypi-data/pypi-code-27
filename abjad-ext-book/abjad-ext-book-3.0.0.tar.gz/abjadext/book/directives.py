import os
import re
import subprocess
from docutils import nodes  # type: ignore
from docutils.nodes import literal_block  # type: ignore
from docutils.parsers.rst import Directive  # type: ignore
from docutils.parsers.rst import directives  # type: ignore
from sphinx.util.nodes import set_source_info  # type: ignore
from typing import Dict  # noqa


class AbjadDirective(Directive):
    '''
    An abjad-book interpreter directive.

    Represents a portion of an interactive session.

    Generates an ``abjad_input_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    ### CLASS VARIABLES ###

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'allow-exceptions': directives.flag,
        'hide': directives.flag,
        'no-resize': directives.flag,
        'no-stylesheet': directives.flag,
        'no-trim': directives.flag,
        'pages': str,
        'reveal-label': str,
        'strip-prompt': directives.flag,
        'stylesheet': str,
        'text-width': int,
        'with-columns': int,
        'with-thumbnail': directives.flag,
        }

    ### PRIVATE METHODS ###

    @staticmethod
    def _parse_pages_string(pages_string):
        pattern = re.compile(r'(\d+)-(\d+)')
        page_selections = []
        for part in (_.strip() for _ in pages_string.split(',')):
            match = pattern.match(part)
            page_range = None
            if match is not None:
                start, stop = match.groups()
                start = int(start)
                stop = int(stop)
                if start == stop:
                    page_range = (start,)
                elif start < stop:
                    page_range = tuple(range(start, stop + 1))
                else:
                    page_range = tuple(range(start, stop - 1, -1))
            elif part.isdigit():
                page = int(part)
                page_range = (page,)
            else:
                continue
            if page_range:
                page_selections.extend(page_range)
        return tuple(page_selections)

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        from abjadext.book import SphinxDocumentHandler
        self.assert_has_content()
        code = u'\n'.join(self.content)
        literal = literal_block(code, code)
        literal.line = self.content_offset  # set the content line number
        block = SphinxDocumentHandler.abjad_input_block(code, literal)
        # Only set flags if true, for a thinner node repr.
        for key in (
            'allow-exceptions',
            'hide',
            'no-resize',
            'no-stylesheet',
            'no-trim',
            'strip-prompt',
            'with-thumbnail',
        ):
            if key in self.options:
                block[key] = True
        pages = self.options.get('pages', None)
        if pages is not None:
            block['pages'] = self._parse_pages_string(pages)
        if 'reveal-label' in self.options:
            block['reveal-label'] = self.options.get('reveal-label')
        stylesheet = self.options.get('stylesheet', None)
        if block.get('no-stylesheet'):
            stylesheet = None
        if stylesheet:
            block['stylesheet'] = stylesheet
        text_width = self.options.get('text-width', None)
        if text_width is not None:
            block['text-width'] = text_width
        with_columns = self.options.get('with-columns', None)
        if with_columns is not None:
            block['with-columns'] = with_columns
        set_source_info(self, block)
        return [block]


class AbjadDoctestDirective(Directive):
    '''
    An abjad-book doctest directive.

    Contributes no formatting to documents built by Sphinx.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}  # type: Dict[str, object]

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        self.assert_has_content()
        return []


class ImportDirective(Directive):
    '''
    An abjad-book import directive.

    Represents a class or function to be imported into an interactive session.

    Generates an ``abjad_import_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'hide': directives.flag,
        'reveal-label': str,
        }

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        from abjadext.book import SphinxDocumentHandler
        path = self.arguments[0]
        block = SphinxDocumentHandler.abjad_import_block()
        block['path'] = path
        if 'hide' in self.options:
            block['hide'] = True
        if 'reveal-label' in self.options:
            block['reveal-label'] = self.options.get('reveal-label')
        set_source_info(self, block)
        return [block]


class RevealDirective(Directive):
    '''
    An abjad-book reveal directive.

    Generates an ``abjad_reveal_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}  # type: Dict[str, object]

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        from abjadext.book import SphinxDocumentHandler
        block = SphinxDocumentHandler.abjad_reveal_block()
        block['reveal-label'] = self.arguments[0]
        set_source_info(self, block)
        return [block]


class ShellDirective(Directive):
    '''
    An abjad-book shell directive.

    Represents a shell session.

    Generates a docutils ``literal_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}  # type: Dict[str, object]

    ### PRIVATE METHODS ###

    def _read_from_pipe(self, pipe):
        lines = []
        string = pipe.read()
        for line in string.splitlines():
            line = line.decode('utf-8')
            lines.append(line)
        return '\n'.join(lines)

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        from abjad import abjad_configuration
        self.assert_has_content()
        os.chdir(abjad_configuration.abjad_directory)
        result = []
        for line in self.content:
            curdir = os.path.basename(os.path.abspath(os.path.curdir))
            prompt = '{}$ '.format(curdir)
            prompt += line
            result.append(prompt)
            process = subprocess.Popen(
                line,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
            stdout = self._read_from_pipe(process.stdout)
            stderr = self._read_from_pipe(process.stderr)
            result.append(stdout)
            result.append(stderr)
        code = '\n'.join(result)
        literal = nodes.literal_block(code, code)
        literal['language'] = 'console'
        set_source_info(self, literal)
        return [literal]


class ThumbnailDirective(Directive):
    '''
    A thumbnail directive.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'class': directives.class_option,
        'group': directives.unchanged,
        'title': directives.unchanged,
        }
    optional_arguments = 0
    required_arguments = 1

    ### PUBLIC METHODS ###

    def run(self):
        '''Executes the directive.
        '''
        from abjadext.book import SphinxDocumentHandler
        node = SphinxDocumentHandler.abjad_thumbnail_block()
        node['classes'] += self.options.get('class', '')
        node['group'] = self.options.get('group', '')
        node['title'] = self.options.get('title', '')
        node['uri'] = self.arguments[0]
        environment = self.state.document.settings.env
        environment.images.add_file('', node['uri'])
        return [node]


__all__ = [
    'AbjadDirective',
    'AbjadDoctestDirective',
    'ImportDirective',
    'RevealDirective',
    'ShellDirective',
    'ThumbnailDirective',
]
