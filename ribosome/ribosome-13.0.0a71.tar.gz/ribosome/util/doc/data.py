from typing import Generic, TypeVar, Callable

from amino import do, Do, IO, List, Dat, Lists, ADT

from ribosome.config.setting import StrictSetting

A = TypeVar('A')


class DocMeta(Generic[A], ADT['DocMeta[A]']):
    pass


class NoMeta(DocMeta[A]):
    pass


class Headline(DocMeta[A]):

    def __init__(self, level: int) -> None:
        self.level = level


class Code(DocMeta[A]):

    def __init__(self, lang: str) -> None:
        self.lang = lang


class CustomDocMeta(DocMeta[A]):

    def __init__(self, extra: A) -> None:
        self.extra = extra


class LinkType(ADT['LinkType']):
    pass


class WebLinkType(LinkType):
    pass


class DocLinkType(LinkType):
    pass


class Link(Generic[A], DocMeta[A]):

    def __init__(self, target: str, tpe: LinkType) -> None:
        self.target = target
        self.tpe = tpe


class DocFragment(Generic[A], ADT['DocFragment[A]']):
    pass


class DocCat(DocFragment[A]):

    def __init__(self, fragments: List[DocFragment]) -> None:
        self.fragments = fragments


class DocString(DocFragment[A]):

    @staticmethod
    def none(text: str) -> 'DocString[None]':
        return DocString(text, NoMeta())

    def __init__(self, text: str, meta: DocMeta[A]) -> None:
        self.text = text
        self.meta = meta


class DocLine(Generic[A], Dat['DocLine[A]']):

    @staticmethod
    def string(
            text: str,
    ) -> 'DocLine[None]':
        return DocLine(
            DocString.none(text),
        )

    def __init__(self, data: DocFragment) -> None:
        self.data = data


class DocBlock(Generic[A], Dat['DocBlock[A]']):

    @staticmethod
    def none(lines: List[DocLine[A]]) -> 'DocBlock[A]':
        return DocBlock(lines, NoMeta())

    def __init__(self, lines: List[DocLine[A]], meta: DocMeta[A]) -> None:
        self.lines = lines
        self.meta = meta


def setting_doc(setting: StrictSetting) -> IO[DocBlock[None]]:
    info = List(setting.desc, setting.help).map(DocLine.string)
    block: DocBlock[None] = DocBlock.none(List(DocLine(DocString(setting.name, Headline(2)))) + info)
    return IO.pure(block)


def settings_doc(settings: List[StrictSetting]) -> IO[List[DocLine]]:
    return settings.traverse(setting_doc, IO)


class DocCompiler(Generic[A], Dat['DocCompiler[A]']):

    def __init__(self, compile: Callable[[List[DocLine[A]]], List[str]]) -> None:
        self.compile = compile


@do(IO[List[str]])
def generate_doc(settings: List[StrictSetting], compiler: DocCompiler[A]) -> Do:
    lines = yield settings_doc(settings)
    yield compiler.compile(lines)


__all__ = ('generate_doc',)
