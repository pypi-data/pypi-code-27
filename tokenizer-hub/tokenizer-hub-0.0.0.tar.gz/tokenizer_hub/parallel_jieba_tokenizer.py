from jieba import Tokenizer, strdecode
from typing import List
import threading


class ParallelJiebaTokenizer(Tokenizer):

    def __init__(self, dictionary=None):
        super().__init__(dictionary=dictionary)
        super().initialize(dictionary=dictionary)

    def strdecode(self, sentence):
        return strdecode(sentence)

    def lcut(
            self,
            sentence: str,
            cut_all: bool = False,
            HMM: bool = True,
        ) -> List[str]:
        return super().lcut(sentence, cut_all=cut_all, HMM=HMM)

    def __getstate__(self):
        d = super().__dict__.copy()
        if 'lock' in d:
            del d['lock']
        return d

    def __setstate__(self, d):
        self.lock = threading.RLock()
        self.__dict__.update(d)
