from typing import List
import functools
import re

from .base_tokenizer import BaseTokenizer
from . import RESERVED_TOKENS


class ChineseCharTokenizer(BaseTokenizer):

    def __init__(self):
        reg_pattern = RESERVED_TOKENS + \
            ["[0-9]+\.[0-9]+"] + \
            ["[a-zA-Z]+"] + \
            ["[0-9]+"] + \
            ["\.\.\."]

        self.prog = re.compile(
            r"{}".format("|".join(reg_pattern)),
        )

    def lcut(
            self,
            sentence: str,
            **kwargs  # noqa
        ) -> List[str]:
        not_chinese_elements = self.prog.findall(sentence)
        pure_chinese_sentence = self.prog.sub("X", sentence)
        tokens = list(pure_chinese_sentence)
        index = 0
        for ti, token in enumerate(tokens):
            if token == "X":
                tokens[ti] = not_chinese_elements[index]
                index += 1
        return tokens

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
