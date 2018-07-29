import abc
import abjad
import copy
import hashlib
import os
import platform
import subprocess
import uqbar.graphs
from docutils import nodes

from abjadext.book.specifiers import ImageRenderSpecifier


class CodeOutputProxy(abjad.AbjadValueObject):
    r'''
    A code output proxy.

    >>> import abjadext.book
    >>> proxy = abjadext.book.CodeOutputProxy([
    ...     ">>> print('Hello, world!')",
    ...     'Hello, world!',
    ...     '>>> 1 + 1',
    ...     '2',
    ...     ])
    >>> print(format(proxy))
    abjadext.proxies.CodeOutputProxy(
        (
            ">>> print('Hello, world!')",
            'Hello, world!',
            '>>> 1 + 1',
            '2',
            )
        )

    >>> for line in proxy.as_latex():
    ...     line
    ...
    '\\begin{lstlisting}'
    ">>> print('Hello, world!')"
    'Hello, world!'
    '\\end{lstlisting}'
    '\\begin{lstlisting}'
    '>>> 1 + 1'
    '2'
    '\\end{lstlisting}'

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_code_block_specifier',
        '_payload',
    )

    ### INITIALIZER ###

    def __init__(self, payload, code_block_specifier=None):
        self._payload = tuple(payload)
        self._code_block_specifier = code_block_specifier

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
    ):
        '''
        Creates a docutils node representation of the code output proxy.

        Returns list of docutils nodes.
        '''
        result = []
        try:
            waiting_for_prompt = False
            lines = []
            for line in self.payload:
                if not line.startswith(('>>> ', '... ')):
                    waiting_for_prompt = True
                elif line.startswith('>>> ') and waiting_for_prompt:
                    waiting_for_prompt = False
                    code = u'\n'.join(lines)
                    block = nodes.literal_block(code, code)
                    result.append(block)
                    lines = []
                lines.append(line)
            if lines:
                code = u'\n'.join(lines)
                block = nodes.literal_block(code, code)
                result.append(block)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in self.payload:
                print(repr(line))
        return result

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
    ):
        '''
        Creates a LaTeX representation of the code output proxy.

        Returns list of strings.
        '''
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        start_command = latex_configuration.get(
            'code-block-start',
            [r'\begin{lstlisting}'],
            )
        start_command = '\n'.join(start_command)
        stop_command = latex_configuration.get(
            'code-block-stop',
            [r'\end{lstlisting}'],
            )
        stop_command = '\n'.join(stop_command)
        result = []
        result.append(start_command)
        waiting_for_prompt = False
        for line in self.payload:
            if not line.startswith(('>>> ', '... ')):
                waiting_for_prompt = True
            elif line.startswith('>>> ') and waiting_for_prompt:
                waiting_for_prompt = False
                result.append(stop_command)
                result.append(start_command)
            result.append(line)
        result.append(stop_command)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def code_block_specifier(self):
        '''
        Gets code block specifier.
        '''
        return self._code_block_specifier

    @property
    def payload(self):
        '''
        Gets code output proxy payload.

        Returns tuple of strings.
        '''
        return self._payload


class ImageOutputProxy(abjad.AbjadValueObject):
    '''
    Abstract base class for image output proxies.
    '''

    # ### CLASS VARIABLES ### #

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_image_layout_specifier',
        '_image_render_specifier',
        '_options',
        '_payload',
        )

    # ### INITIALIZER ### #

    def __init__(
        self,
        image_layout_specifier=None,
        image_render_specifier=None,
        **options
    ):
        self._image_layout_specifier = image_layout_specifier
        self._image_render_specifier = image_render_specifier
        self._options = options

    # ### PRIVATE METHODS ### #

    def _include_graphics(
        self,
        latex_configuration,
        options,
        page_number,
        relative_file_path,
    ):
        result = []
        if page_number:
            page_number = 'page={}'.format(page_number)
            if not options:
                options = page_number
            else:
                options = options.strip()
                if not options.endswith(','):
                    options += ', '
                options += page_number
        if options:
            string = '\\noindent\\includegraphics[{}]{{{}}}'.format(
                options,
                relative_file_path,
                )
        else:
            string = '\\noindent\\includegraphics{{{}}}'.format(
                relative_file_path,
                )
        before = self.options.get('before_includegraphics', ())
        if isinstance(before, str):
            before = (before,)
        if not before:
            before = latex_configuration.get('before-includegraphics', ())
        after = self.options.get('after_includegraphics', ())
        if isinstance(after, str):
            after = (after,)
        if not after:
            after = latex_configuration.get('after-includegraphics', ())
        result.extend(before)
        result.append(string)
        result.extend(after)
        return result

    def _render_pdf_source(
        self,
        temporary_directory,
        ):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
    ):
        '''
        Creates a LaTeX representation of the image output proxy.
        '''
        import PyPDF2  # type: ignore
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        options_key = '{}-options'.format(self.file_name_prefix)
        options = self.options.get(options_key.replace('-', '_'), ())
        if isinstance(options, str):
            options = (options,)
        if not options:
            options = latex_configuration.get(options_key, ())
        options = ''.join(options)
        file_extension = '.pdf'
        file_name = self.file_name_without_extension + file_extension
        output_directory = output_directory or relative_output_directory
        absolute_file_path = os.path.join(
            output_directory,
            file_name,
            )
        relative_file_path = os.path.join(
            relative_output_directory,
            file_name,
            )
        # Windows hack for test suite.
        relative_file_path = relative_file_path.replace(os.path.sep, '/')
        page_count = 1
        if os.path.exists(absolute_file_path):
            with open(absolute_file_path, 'rb') as file_pointer:
                pdf_reader = PyPDF2.PdfFileReader(file_pointer)
                page_count = pdf_reader.getNumPages()
        result = []
        if page_count == 1:
            result.extend(self._include_graphics(
                latex_configuration,
                options,
                None,
                relative_file_path,
                ))
        else:
            result.extend(self._include_graphics(
                latex_configuration,
                options,
                1,
                relative_file_path,
                ))
            for page_number in range(2, page_count + 1):
                result.append(r'\newline')
                result.append(r'\newline')
                result.extend(self._include_graphics(
                    latex_configuration,
                    options,
                    page_number,
                    relative_file_path,
                    ))
        return result

    def render_for_latex(
        self,
        absolute_output_directory,
    ):
        '''
        Renders the image output proxy payload for LaTeX inclusion.
        '''
        target_pdf_path = os.path.join(
            absolute_output_directory,
            self.file_name_without_extension + '.pdf',
            )
        if os.path.exists(target_pdf_path):
            return
        self._render_pdf_source(absolute_output_directory)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def file_name_prefix(self):
        '''
        Gets image output proxy file name prefix.

        Returns string.
        '''
        raise NotImplementedError

    @property
    def file_name_without_extension(self):
        '''
        Gets image output proxy filename without file extension.

        Returns string.
        '''
        payload = '\n'.join(format(self.payload))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    @property
    def image_layout_specifier(self):
        '''
        Gets image specifier.
        '''
        return self._image_layout_specifier

    @property
    def image_render_specifier(self):
        '''
        Gets image specifier.
        '''
        return self._image_render_specifier

    @property
    def options(self):
        return self._options

    @property
    def payload(self):
        '''
        Gets images output proxy payload.

        Returns string.
        '''
        return self._payload


class GraphvizOutputProxy(ImageOutputProxy):
    r'''
    A Graphviz output proxy.

    >>> import abjadext.book
    >>> meter = abjad.Meter((4, 4))
    >>> proxy = abjadext.book.GraphvizOutputProxy(meter)
    >>> print(format(proxy))
    ...
    abjadext.proxies.GraphvizOutputProxy(
        <uqbar.graphs.Graph.Graph object at 0x...>,
        layout='dot',
        )

    >>> print(format(proxy.payload, 'graphviz'))
    digraph G {
        graph [bgcolor=transparent,
            fontname=Arial,
            penwidth=2,
            truecolor=true];
        node [fontname=Arial,
            fontsize=12,
            penwidth=2];
        edge [penwidth=2];
        node_0 [label="4/4",
            shape=triangle];
        node_1 [label="1/4",
            shape=box];
        node_2 [label="1/4",
            shape=box];
        node_3 [label="1/4",
            shape=box];
        node_4 [label="1/4",
            shape=box];
        subgraph cluster_offsets {
            graph [style=rounded];
            node_5_0 [color=white,
                fillcolor=black,
                fontcolor=white,
                fontname="Arial bold",
                label="{ <f_0_0> 0 | <f_0_1> ++ }",
                shape=Mrecord,
                style=filled];
            node_5_1 [color=white,
                fillcolor=black,
                fontcolor=white,
                fontname="Arial bold",
                label="{ <f_0_0> 1/4 | <f_0_1> + }",
                shape=Mrecord,
                style=filled];
            node_5_2 [color=white,
                fillcolor=black,
                fontcolor=white,
                fontname="Arial bold",
                label="{ <f_0_0> 1/2 | <f_0_1> + }",
                shape=Mrecord,
                style=filled];
            node_5_3 [color=white,
                fillcolor=black,
                fontcolor=white,
                fontname="Arial bold",
                label="{ <f_0_0> 3/4 | <f_0_1> + }",
                shape=Mrecord,
                style=filled];
            node_5_4 [label="{ <f_0_0> 1 | <f_0_1> ++ }",
                shape=Mrecord];
        }
        node_0 -> node_1;
        node_0 -> node_2;
        node_0 -> node_3;
        node_0 -> node_4;
        node_1 -> node_5_0 [style=dotted];
        node_1 -> node_5_1 [style=dotted];
        node_2 -> node_5_1 [style=dotted];
        node_2 -> node_5_2 [style=dotted];
        node_3 -> node_5_2 [style=dotted];
        node_3 -> node_5_3 [style=dotted];
        node_4 -> node_5_3 [style=dotted];
        node_4 -> node_5_4 [style=dotted];
    }

    >>> proxy.as_latex(relative_output_directory='assets')
    ['\\noindent\\includegraphics{assets/graphviz-a20bf977ab8d78c92f80a64305ccbe7b.pdf}']

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_layout',
    )

    ### INITIALIZER ###

    def __init__(
        self,
        payload,
        layout='dot',
        image_layout_specifier=None,
        image_render_specifier=None,
        ):
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
        )
        if not isinstance(payload, uqbar.graphs.Graph):
            payload = payload.__graph__()
        payload = copy.deepcopy(payload)
        self._payload = payload
        self._layout = layout

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory,
        ):
        dot_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.dot',
        )
        source = format(self.payload, 'graphviz')
        with open(dot_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        pdf_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.pdf',
        )
        if platform.system() == 'Darwin':
            command = '{} -v -Tpdf:quartz:quartz {} -o {}'
        else:
            command = '{} -v -Tpdf {} -o {}'
        command = command.format(
            self.layout,
            dot_file_path,
            pdf_file_path,
        )
        exit_code = subprocess.call(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if exit_code:
            print(source)
            raise AssertionError
        assert os.path.exists(pdf_file_path)
        assert abjad.IOManager.find_executable('pdfcrop')
        command = 'pdfcrop {path} {path}'.format(path=pdf_file_path)
        exit_code = subprocess.call(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        assert exit_code == 0
        return pdf_file_path

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
    ):
        '''
        Creates a docutils node representation of the output proxy.

        >>> import abjadext.book
        >>> meter = abjad.Meter((4, 4))
        >>> proxy = abjadext.book.GraphvizOutputProxy(meter)
        >>> for node in proxy.as_docutils():
        ...     print(node.pformat())
        ...
        <abjad_output_block image_layout_specifier... image_render_specifier... layout="dot" renderer="graphviz" xml:space="preserve">
            digraph G {
                graph [bgcolor=transparent,
                    fontname=Arial,
                    penwidth=2,
                    truecolor=true];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2];
                edge [penwidth=2];
                node_0 [label="4/4",
                    shape=triangle];
                node_1 [label="1/4",
                    shape=box];
                node_2 [label="1/4",
                    shape=box];
                node_3 [label="1/4",
                    shape=box];
                node_4 [label="1/4",
                    shape=box];
                subgraph cluster_offsets {
                    graph [style=rounded];
                    node_5_0 [color=white,
                        fillcolor=black,
                        fontcolor=white,
                        fontname="Arial bold",
                        label="{ <f_0_0> 0 | <f_0_1> ++ }",
                        shape=Mrecord,
                        style=filled];
                    node_5_1 [color=white,
                        fillcolor=black,
                        fontcolor=white,
                        fontname="Arial bold",
                        label="{ <f_0_0> 1/4 | <f_0_1> + }",
                        shape=Mrecord,
                        style=filled];
                    node_5_2 [color=white,
                        fillcolor=black,
                        fontcolor=white,
                        fontname="Arial bold",
                        label="{ <f_0_0> 1/2 | <f_0_1> + }",
                        shape=Mrecord,
                        style=filled];
                    node_5_3 [color=white,
                        fillcolor=black,
                        fontcolor=white,
                        fontname="Arial bold",
                        label="{ <f_0_0> 3/4 | <f_0_1> + }",
                        shape=Mrecord,
                        style=filled];
                    node_5_4 [label="{ <f_0_0> 1 | <f_0_1> ++ }",
                        shape=Mrecord];
                }
                node_0 -> node_1;
                node_0 -> node_2;
                node_0 -> node_3;
                node_0 -> node_4;
                node_1 -> node_5_0 [style=dotted];
                node_1 -> node_5_1 [style=dotted];
                node_2 -> node_5_1 [style=dotted];
                node_2 -> node_5_2 [style=dotted];
                node_3 -> node_5_2 [style=dotted];
                node_3 -> node_5_3 [style=dotted];
                node_4 -> node_5_3 [style=dotted];
                node_4 -> node_5_4 [style=dotted];
            }
        <BLANKLINE>

        Returns list of docutils nodes.
        '''
        from abjadext.book import SphinxDocumentHandler
        result = []
        try:
            code = format(self.payload, 'graphviz')
            node = SphinxDocumentHandler.abjad_output_block(
                code, code)
            node['image_layout_specifier'] = self.image_layout_specifier
            node['image_render_specifier'] = self.image_render_specifier
            node['layout'] = self.layout
            node['renderer'] = 'graphviz'
            result.append(node)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in code.splitlines():
                print(repr(line))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        '''
        Gets file name prefix of Graphviz output proxy.

        Returns string.
        '''
        return 'graphviz'

    @property
    def file_name_without_extension(self):
        '''
        Gets file name extension of Graphviz output proxy.

        Returns string.
        '''
        payload = '\n'.join(format(self.payload, 'graphviz'))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    @property
    def layout(self):
        '''
        Gets layout engine name of Graphviz output.

        Returns string.
        '''
        return self._layout


class LilyPondOutputProxy(ImageOutputProxy):
    r"""
    A LilyPond output proxy.

    >>> import abjadext.book
    >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
    >>> proxy = abjadext.book.LilyPondOutputProxy(staff)
    >>> print(format(proxy))
    abjadext.proxies.LilyPondOutputProxy(
        abjad.LilyPondFile(
            comments=[],
            includes=[],
            items=[
                abjad.Block(
                    name='score',
                    ),
                ],
            lilypond_language_token=abjad.LilyPondLanguageToken(),
            lilypond_version_token=abjad.LilyPondVersionToken(
                version_string='2.19.0',
                ),
            )
        )

    >>> proxy.as_latex(relative_output_directory='assets')
    ['\\noindent\\includegraphics{assets/lilypond-d3ecbde01b2f252633e28953dae06eea.pdf}']

    """

    # ### CLASS VARIABLES ### #

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_strict',
    )

    # ### INITIALIZER ### #

    def __init__(
        self,
        payload,
        image_layout_specifier=None,
        image_render_specifier=None,
        strict=None,
    ):
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
        )
        payload = copy.deepcopy(payload)
        if image_render_specifier is None:
            image_render_specifier = ImageRenderSpecifier()
        if (
            not image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
        ):
            payload = abjad.LilyPondFile.new(payload)
        lilypond_file = payload
        assert isinstance(lilypond_file, abjad.LilyPondFile)
        if lilypond_file.header_block:
            if getattr(lilypond_file.header_block, 'tagline') is False:
                # default.ily stylesheet already sets tagline = ##f
                delattr(lilypond_file.header_block, 'tagline')
            if lilypond_file.header_block.empty():
                lilypond_file.items.remove(lilypond_file.header_block)
        if lilypond_file.layout_block and lilypond_file.layout_block.empty():
            lilypond_file.items.remove(lilypond_file.layout_block)
        if lilypond_file.paper_block and lilypond_file.paper_block.empty():
            lilypond_file.items.remove(lilypond_file.paper_block)
        lilypond_file._date_time_token = None
        token = abjad.LilyPondVersionToken("2.19.0")
        lilypond_file._lilypond_version_token = token
        if (
            image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
        ):
            if not lilypond_file.includes:
                lilypond_file._use_relative_includes = True
                includes = [image_render_specifier.stylesheet]
                lilypond_file._includes = tuple(includes)
        self._payload = lilypond_file
        self._strict = strict

    # ### PRIVATE METHODS ### #

    def _render_pdf_source(self, temporary_directory):
        ly_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.ly',
            )
        source = format(self.payload)
        with open(ly_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        abjad.IOManager.run_lilypond(ly_file_path)
        pdf_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.pdf',
            )
        if not os.path.exists(pdf_file_path):
            print(format(self.payload))
            raise AssertionError
        assert abjad.IOManager.find_executable('pdfcrop')
        command = f'pdfcrop {pdf_file_path} {pdf_file_path}'
        process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = process.communicate()
        if not process.returncode == 0:
            raise Exception(stdout)
        return pdf_file_path

    # ### PUBLIC PROPERTIES ### #

    @property
    def file_name_prefix(self):
        """
        Gets file name prefix of LilyPond output proxy.

        Returns string.
        """
        return 'lilypond'

    @property
    def strict(self):
        """
        Is true when LilyPond file should format strict.

        Returns true, false or none.
        """
        return self._strict

    # ### PUBLIC METHODS ### #

    def as_docutils(self, configuration=None, output_directory=None):
        r"""
        Creates a docutils node representation of the output proxy.

        >>> import abjadext.book
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> proxy = abjadext.book.LilyPondOutputProxy(staff)
        >>> for node in proxy.as_docutils():
        ...     print(node.pformat())
        ...
        <abjad_output_block image_layout_specifier="True" image_render_specifier="True" renderer="lilypond" xml:space="preserve">
            \version "2.19.0"
            \language "english"
        <BLANKLINE>
            \score {
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }
        <BLANKLINE>

        Returns list of docutils nodes.
        """
        from abjadext.book import SphinxDocumentHandler
        result = []
        assert self.strict is not False, repr(self.strict)
        try:
            code = format(self.payload, 'lilypond')
            if isinstance(self.strict, int):
                code = abjad.LilyPondFormatManager.align_tags(
                    code,
                    self.strict,
                    )
            if self.strict:
                if isinstance(self.strict, int):
                    realign = self.strict
                else:
                    realign = None
                code = abjad.LilyPondFormatManager.left_shift_tags(
                    code,
                    realign=realign,
                    )
            node = SphinxDocumentHandler.abjad_output_block(code, code)
            node['image_layout_specifier'] = self.image_layout_specifier
            node['image_render_specifier'] = self.image_render_specifier
            node['renderer'] = 'lilypond'
            result.append(node)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in code.splitlines():
                print(repr(line))
        return result


class RawLilyPondOutputProxy(ImageOutputProxy):
    r"""
    A raw LilyPond output proxy.

    >>> import abjadext.book
    >>> raw_lilypond = '{ c d e f }'
    >>> proxy = abjadext.book.RawLilyPondOutputProxy(raw_lilypond)
    >>> print(format(proxy))
    abjadext.proxies.RawLilyPondOutputProxy(
        '\\version "2.19.0"\n\n{ c d e f }'
        )

    >>> proxy.as_latex(relative_output_directory='assets')
    ['\\noindent\\includegraphics{assets/lilypond-678fb46ce202b3d770361f814e6e1946.pdf}']

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        payload,
        image_layout_specifier=None,
        image_render_specifier=None,
        **options
        ):
        import abjadext.book
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            **options
            )
        if image_render_specifier is None:
            image_render_specifier = abjadext.book.ImageRenderSpecifier()
        preamble = []
        if not payload.startswith(r'\version'):
            preamble.extend([r'\version "2.19.0"', ''])
        if (
            image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
            ):
            preamble.extend([
                "#(ly:set-option 'relative-includes #t)",
                '\include "{}"'.format(image_render_specifier.stylesheet),
                '',
                ])
        if preamble:
            payload = '\n'.join(preamble) + '\n' + payload
        self._payload = payload

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory,
        ):
        from abjad import abjad_configuration
        log_file_path = abjad_configuration.lilypond_log_file_path
        ly_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.ly',
            )
        source = format(self.payload)
        with open(ly_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        abjad.IOManager.run_lilypond(ly_file_path)
        pdf_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.pdf',
            )
        if not os.path.exists(pdf_file_path):
            print(format(self.payload))
            with open(log_file_path) as file_pointer:
                print(file_pointer.read())
            raise AssertionError
        assert abjad.IOManager.find_executable('pdfcrop')
        command = 'pdfcrop {path} {path}'.format(path=pdf_file_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = process.communicate()
        if not process.returncode == 0:
            raise Exception(stdout)
        return pdf_file_path

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        """
        Gets file name prefix of LilyPond output proxy.

        Returns string.
        """
        return 'lilypond'


__all__ = [
    'CodeOutputProxy',
    'GraphvizOutputProxy',
    'ImageOutputProxy',
    'LilyPondOutputProxy',
    'RawLilyPondOutputProxy',
]
