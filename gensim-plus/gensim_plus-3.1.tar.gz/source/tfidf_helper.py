#!/usr/bin/env python3
import os
import traceback
import pdb
import gensim
import gensim_plus_config
from gensim_plus_config import FLAGS
import jieba
import jieba.posseg
import re
import base_interface
from base_interface import TfIdfHelperInterface
import numpy as np

words2d = [
    ["富强","民主","文明","和谐","民主","文明","和谐"],
    ["自由","平等","公正","法治","法治"],
    ["爱国","敬业","明礼","诚信","敬业"]
]

words = ["富强民主文明和谐", "自由平等公正法治", "爱国敬业明礼诚信"]

class TfIdfHelper(TfIdfHelperInterface):
    def __init__(self):
        pass
        print("\n> 实例化一个新的 TfIdfHelper")

    def init_tfidf_model(self,dictionary,words2d):
        corpus = [dictionary.doc2bow(words) for words in words2d]
        print(corpus)
        tfidfModel = gensim.models.TfidfModel(corpus)
        for corpus_item in corpus:
            #print([dictionary[i[0]] for i in corpus_item])
            yield [(dictionary[i[0]], i[1]) for i in tfidfModel[corpus_item]]

    def filter_tfidf(self,lst,percent):
        tfidf_sum_lst = [wordtuple[1] for wordtuple in lst]
        level = int(percent*len(lst))
        level_num = sorted(tfidf_sum_lst)[level]
        res = []
        for wordtuple in lst:
            if wordtuple[1]>level_num:
                res.append(wordtuple[0])
        return res

    def test_init_tfidf_model(self):
        tfIdfHelperInstance = TfIdfHelper()
        dictionary = gensim.corpora.dictionary.Dictionary(words2d)
        gen = tfIdfHelperInstance.init_tfidf_model(dictionary,words2d)
        for i in range(len(words2d)):
            lst = gen.__next__()
            print(lst)
            res = tfIdfHelperInstance.filter_tfidf(lst,0.0)
            print(res)

if __name__ == "__main__":
    tfIdfHelperInstance = TfIdfHelper()
    tfIdfHelperInstance.test_init_tfidf_model()
