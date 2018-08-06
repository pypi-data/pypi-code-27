from typing import List
import nltk
nltk.download('punkt')  # noqa
import functools
from nltk.tokenize import WordPunctTokenizer, word_tokenize

from .base_tokenizer import BaseTokenizer


class NltkTokenizer(BaseTokenizer):

    def __init__(
            self,
            punct: bool = None,
        ):
        self.WPtokenizer = WordPunctTokenizer()
        self.punct = punct

    def lcut(
            self,
            sentence,
            punct: bool = None,
            **kwargs  # noqa
        ):
        if punct is not None:
            self.punct = punct
        if self.punct is True:
            return(self.WPtokenizer.tokenize(sentence))
        else:
            return(word_tokenize(sentence))

    def lcut_sentences(
            self,
            sentences: List[str],
            num_jobs: int = 8,
            punct: bool = True,
        ) -> List[List[str]]:
        from multiprocessing import cpu_count, Pool
        if num_jobs is None:
            num_jobs = cpu_count()
        if self.punct is not None:
            punct = self.punct
        with Pool(num_jobs) as pool:
            results = pool.map(
                functools.partial(
                    self.lcut,
                    punct=punct,
                ),
                sentences,
            )
        return results
