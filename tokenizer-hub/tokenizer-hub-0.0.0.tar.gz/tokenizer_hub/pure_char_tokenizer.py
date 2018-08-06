from typing import List
import functools
import re

import purewords
import string

from .base_tokenizer import BaseTokenizer


class CharTokenizerForPureWords(BaseTokenizer):

    def __init__(self):
        self.prog = re.compile(
            "[{}]+".format(re.escape(string.printable)),
        )

    def lcut(
            self,
            sentence: str,
            **kwargs  # noqa
        ):
        not_chinese_elements = self.prog.findall(sentence)
        pure_chinese_sentence = self.prog.sub("X", sentence)
        tokens = list(pure_chinese_sentence)
        index = 0
        for ti, token in enumerate(tokens):
            if token == 'X':
                tokens[ti] = not_chinese_elements[index]
                index += 1
        return tokens

    def cut(
            self,
            sentence: str,
        ) -> str:
        result = self.lcut(sentence)
        for char in result:
            yield char

    def lcut_sentences(
            self,
            sentences: List[str],
            num_jobs: int = None,
        ) -> List[List[str]]:
        from multiprocessing import cpu_count, Pool
        if num_jobs is None:
            num_jobs = cpu_count()
        with Pool(num_jobs) as pool:
            results = pool.map(
                functools.partial(
                    self.lcut,
                ),
                sentences,
            )
        return results


class PureChineseCharTokenizer(BaseTokenizer):

    def __init__(self):
        self.purechartokenizer = purewords.PureWords(
            tokenizer=CharTokenizerForPureWords(),
        )

    def lcut(
            self,
            sentence: str,
        ) -> List[str]:
        return self.purechartokenizer.clean_sentence(sentence).split(" ")

    def cut(
            self,
            sentence: str,
        ) -> str:
        result = self.lcut(sentence=sentence)
        for char in result:
            yield char
