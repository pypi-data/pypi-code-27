from typing import TypeVar

from amino import List, IO
from amino.case import Case

from ribosome.util.doc.data import DocLine, DocCompiler, DocCat, DocFragment, DocString, DocBlock

A = TypeVar('A')


class compile_fragment(Case[DocFragment[A], List[str]], alg=DocFragment):

    def cat(self, frag: DocCat[A]) -> List[str]:
        return frag.fragments.flat_map(self)

    def string(self, frag: DocString[A]) -> List[str]:
        return List(frag.text)


def compile_line(line: DocLine[A]) -> List[str]:
    return compile_fragment.match(line.data)


def compile_block(block: DocBlock[A]) -> List[str]:
    return block.lines.flat_map(compile_line)


def compile_markdown(blocks: List[DocBlock[A]]) -> IO[List[str]]:
    return IO.pure(blocks.flat_map(compile_block))


markdown_compiler = DocCompiler(compile_markdown)


__all__ = ('compile_markdown', 'markdown_compiler',)
