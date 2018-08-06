from typing import List
from .base_tokenizer import BaseTokenizer


class AddWords(object):

    def __init__(
            self,
            tokenizer: BaseTokenizer,
            extra_words: List[str] = None,
        ) -> None:
        if extra_words is None:
            extra_words = []
        self.extra_words = extra_words
        self.tokenizer = tokenizer

    def __enter__(self):
        if hasattr(self.tokenizer, "add_word_idempotent"):
            self.existed_tokens = {}
            for word in self.extra_words:
                self.existed_tokens.update(
                    self.tokenizer.add_word_idempotent(word=word),
                )
        return self.tokenizer

    def __exit__(self, type, value, traceback):
        if hasattr(self.tokenizer, "del_word_idempotent"):
            for word in self.extra_words:
                self.tokenizer.del_word_idempotent(
                    word=word,
                    existed_tokens=self.existed_tokens,
                )
