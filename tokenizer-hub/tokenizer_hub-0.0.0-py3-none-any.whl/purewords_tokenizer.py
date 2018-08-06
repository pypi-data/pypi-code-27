import re
from typing import List

import purewords

from .base_tokenizer import BaseTokenizer
from .parallel_jieba_tokenizer import ParallelJiebaTokenizer


class PureWordsTokenizer(BaseTokenizer):

    def __init__(
            self,
            dict_path: str = None,
            freq_words: List[str] = None,
        ):
        self.tokenizer = ParallelJiebaTokenizer()
        if dict_path is not None:
            self.tokenizer.load_userdict(dict_path)
        if freq_words is not None:
            self._add_words(words=freq_words)
        self.specific_tokens = [
            '_url_',
            '_num_',
            '_phone_',
            '_time_',
        ]
        self._add_words(
            words=self.specific_tokens,
        )
        self.purewords_tokenizer = purewords.PureWords(
            tokenizer=self.tokenizer,
        )
        self.sub_prog_1 = re.compile(r"(?<=\s)_(\s)")
        self.sub_prog_2 = re.compile(r"\s+")

    def _add_words(
            self,
            words: List[str],
            freq: int = None,
            tag: str = None,
        ):
        for word in words:
            self.tokenizer.add_word(word=word, freq=freq, tag=tag)
            self.tokenizer.suggest_freq(segment=word, tune=True)

    def lcut(
            self,
            sentence: str,
            **kwargs  # noqa
        ) -> List[str]:
        clean_sentence = self.purewords_tokenizer.clean_sentence(sentence)
        clean_sentence = ' ' + clean_sentence + ' '
        clean_sentence = self.sub_prog_1.sub(" ", clean_sentence)
        clean_sentence = self.sub_prog_2.sub(" ", clean_sentence)
        clean_sentence = clean_sentence.strip()
        if clean_sentence == '':
            return []
        else:
            tokens = clean_sentence.split(' ')
            return tokens

    def lcut_sentences(
            self,
            sentences: List[str],
            num_jobs: int = 8,
        ) -> List[List[str]]:
        from multiprocessing import cpu_count, Pool
        if num_jobs is None:
            num_jobs = cpu_count()
        with Pool(num_jobs) as pool:
            tokenized_sentences = pool.map(self.lcut, sentences)
        return tokenized_sentences
