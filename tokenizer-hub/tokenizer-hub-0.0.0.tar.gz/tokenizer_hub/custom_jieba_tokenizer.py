from typing import Dict, List

from .parallel_jieba_tokenizer import ParallelJiebaTokenizer, strdecode
from .base_tokenizer import BaseTokenizer
import functools


class CustomJiebaTokenizer(ParallelJiebaTokenizer, BaseTokenizer):

    def __init__(
            self,
            cut_all: bool = None,
            HMM: bool = None,
            userdict_path: str = None,
        ):
        super(CustomJiebaTokenizer, self).__init__()
        self.cut_all = cut_all
        self.HMM = HMM
        if userdict_path is not None:
            super(CustomJiebaTokenizer, self).load_userdict(userdict_path)

    def add_word_idempotent(
            self,
            word: str,
        ) -> Dict[str, int]:
        word = strdecode(word)
        freq = 1
        self.FREQ[word] = freq
        self.total += freq

        existed_token = {}
        for ch in range(len(word)):
            wfrag = word[:ch + 1]
            if wfrag not in self.FREQ:
                self.FREQ[wfrag] = 0
            else:
                existed_token[wfrag] = self.FREQ[wfrag]
        return existed_token

    def del_word_idempotent(
            self,
            word: str,
            existed_tokens: Dict[str, int],
        ) -> None:
        word = strdecode(word)
        self.total -= self.FREQ[word]
        del self.FREQ[word]

        for ch in range(len(word)):
            wfrag = word[:ch + 1]
            if wfrag not in existed_tokens and self.FREQ[wfrag] == 0:
                del self.FREQ[wfrag]

    def lcut(
            self,
            sentence: str,
            cut_all: bool = None,
            HMM: bool = None,
            **kwargs  # noqa
        ) -> List[str]:
        if cut_all is not None:
            self.cut_all = cut_all
        if HMM is not None:
            self.HMM = HMM
        return super().lcut(
            sentence,
            cut_all=self.cut_all,
            HMM=self.HMM,
        )

    def lcut_sentences(
            self,
            sentences: List[str],
            num_jobs: int = None,
            extra_words: List[str] = None,
            HMM: bool = True,
            cut_all: bool = False,
        )-> List[List[str]]:
        from multiprocessing import cpu_count, Pool
        if num_jobs is None:
            num_jobs = cpu_count()
        if self.cut_all is not None:
            cut_all = self.cut_all
        if self.HMM is not None:
            HMM = self.HMM
        with Pool(num_jobs) as pool:
            results = pool.map(
                functools.partial(
                    self.lcut,
                    extra_words=extra_words,
                    cut_all=cut_all,
                    HMM=HMM,
                ),
                sentences,
            )
        return results
