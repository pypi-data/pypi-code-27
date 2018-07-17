import random
import re

from lztools.DataTypes.LazyVariable import super_property
from lztools.IO import read_words_from_disk

def regex(expr, text, only_first=False, suppress=False):
    if only_first:
        if suppress:
            try:
                return re.search(expr, text).group(0)
            except:
                pass
        else:
            return re.search(expr, text).group(0)
    else:
        return (x for x in re.findall(expr, text))

words = super_property(read_words_from_disk)

def search_words(term, strict=False):
    for word in words:
        if strict:
            if term in word:
                yield word
        else:
            pas = True
            for l in set(term):
                if l not in word:
                    pas = False
            if pas:
                yield word

def get_random_word():
    return random.choice(list(words))