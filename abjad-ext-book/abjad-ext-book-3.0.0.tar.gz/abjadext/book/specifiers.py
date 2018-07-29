import abjad


class CodeBlockSpecifier(abjad.AbjadValueObject):
    '''
    A code block specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_allow_exceptions',
        '_hide',
        '_strip_prompt',
        '_text_width',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_exceptions=None,
        hide=None,
        strip_prompt=None,
        text_width=None,
        ):
        self._allow_exceptions = bool(allow_exceptions) or None
        self._hide = bool(hide) or None
        self._strip_prompt = bool(strip_prompt) or None
        if text_width is not None:
            if text_width is True:
                text_width = 80
            try:
                text_width = int(text_width)
                if text_width < 1:
                    text_width = None
            except Exception:
                text_width = None
        self._text_width = text_width

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        '''
        Creates code block specifier from `options` dictionary.

        Returns code block specifier.
        '''
        allow_exceptions = None
        if 'allow_exceptions' in options:
            allow_exceptions = options.pop('allow_exceptions')
        hide = None
        if 'hide' in options:
            hide = options.pop('hide')
        strip_prompt = None
        if 'strip_prompt' in options:
            strip_prompt = options.pop('strip_prompt')
        text_width = None
        if 'text_width' in options:
            text_width = options.pop('text_width')
        if all(_ is None for _ in (
            allow_exceptions,
            hide,
            strip_prompt,
            text_width,
            )):
            return None, options
        return cls(
            allow_exceptions=allow_exceptions,
            hide=hide,
            strip_prompt=strip_prompt,
            text_width=text_width,
            ), options

    ### PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        '''
        Is true if code block allows exceptions. Otherwise false.

        Returns true or false.
        '''
        return self._allow_exceptions

    @property
    def hide(self):
        '''
        Is true if code block should be hidden. Otherwise false.

        Returns true or false.
        '''
        return self._hide

    @property
    def strip_prompt(self):
        '''
        Is true if code block should strip Python prompt from output.
        Otherwise false.

        Returns true or false.
        '''
        return self._strip_prompt

    @property
    def text_width(self):
        '''
        Gets text width wrap of code block.

        Returns integer or none.
        '''
        return self._text_width


class ImageLayoutSpecifier(abjad.AbjadValueObject):
    '''
    An image layout specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_pages',
        '_with_columns',
        '_with_thumbnail',
    )

    ### INITIALIZER ###

    def __init__(
        self,
        pages=None,
        with_columns=None,
        with_thumbnail=None,
        ):
        self._pages = pages or None
        if with_columns is not None:
            with_columns = int(with_columns)
            if with_columns < 1:
                with_columns = None
        self._with_columns = with_columns or None
        self._with_thumbnail = with_thumbnail or None

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        '''
        Creates image specifier from `options` dictionary.

        Returns image specifier.
        '''
        pages = None
        if 'pages' in options:
            pages = options.pop('pages')
        with_columns = None
        if 'with_columns' in options:
            with_columns = options.pop('with_columns')
        with_thumbnail = None
        if 'with_thumbnail' in options:
            with_thumbnail = options.pop('with_thumbnail')
        if all(_ is None for _ in (
            pages,
            with_columns,
            with_thumbnail,
            )):
            return None, options
        return cls(
            pages=pages,
            with_columns=with_columns,
            with_thumbnail=with_thumbnail,
            ), options

    ### PUBLIC PROPERTIES ###

    @property
    def pages(self):
        '''
        Gets page indices.

        Returns tuple of integers or none.
        '''
        return self._pages

    @property
    def with_columns(self):
        '''
        Gets column count for table layout.

        Return integer or none.
        '''
        return self._with_columns

    @property
    def with_thumbnail(self):
        '''
        Is true if image should have a thumbnail.

        Returns true or false.
        '''
        return self._with_thumbnail


class ImageRenderSpecifier(abjad.AbjadValueObject):
    '''
    An image render specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    __slots__ = (
        '_no_resize',
        '_no_stylesheet',
        '_no_trim',
        '_stylesheet',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        no_resize=None,
        no_stylesheet=None,
        no_trim=None,
        stylesheet=None,
        ):
        self._no_resize = bool(no_resize) or None
        self._no_stylesheet = bool(no_stylesheet) or None
        self._no_trim = bool(no_trim) or None
        self._stylesheet = stylesheet
        if self._no_stylesheet:
            self._stylesheet = None

    ### PUBLIC METHODS ###

    @classmethod
    def from_options(cls, **options):
        '''
        Creates image specifier from `options` dictionary.

        Returns image specifier.
        '''
        no_resize = None
        if 'no_resize' in options:
            no_resize = options.pop('no_resize')
        no_stylesheet = None
        if 'no_stylesheet' in options:
            no_stylesheet = options.pop('no_stylesheet')
        no_trim = None
        if 'no_trim' in options:
            no_trim = options.pop('no_trim')
        stylesheet = None
        if 'stylesheet' in options:
            stylesheet = options.pop('stylesheet')
        if all(_ is None for _ in (
            no_resize,
            no_stylesheet,
            no_trim,
            stylesheet,
            )):
            return None, options
        return cls(
            no_resize=no_resize,
            no_stylesheet=no_stylesheet,
            no_trim=no_trim,
            stylesheet=stylesheet,
            ), options

    ### PUBLIC PROPERTIES ###

    @property
    def no_resize(self):
        '''
        Is true if image should not be resized.

        Returns true or false.
        '''
        return self._no_resize

    @property
    def no_stylesheet(self):
        '''
        Is true if no stylesheet should be used with image at all.

        Returns true or false.
        '''
        return self._no_stylesheet

    @property
    def no_trim(self):
        '''
        Is true if image should not be trimmed of whitespace.

        Returns true or false.
        '''
        return self._no_trim

    @property
    def stylesheet(self):
        '''
        Gets stylesheet name to be used for image.

        Returns string or none.
        '''
        return self._stylesheet


__all__ = [
    'CodeBlockSpecifier',
    'ImageLayoutSpecifier',
    'ImageRenderSpecifier',
]
