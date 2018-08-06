from typing import List


class BaseTokenizer(object):

    def lcut(
            self,
            sentence: str,
        ) -> List[str]:
        """Tokenize a single sentence
        Args:
          sentence: single string representing a sentence
        Returns:
          tokenized_sentence: a list of tokens
        """
        raise NotImplementedError

    def lcut_sentences(
            self,
            sentences: List[str],
            num_jobs: int,
        ) -> List[List[str]]:
        """Tokenizing sentences in a parallel way.
        Args:
          sentences: list of sentence to be tokenized
          num_jobs: parallel processors
        Returns:
          tokenized_sentences: List[List[tokens]]
        """
        raise NotImplementedError
