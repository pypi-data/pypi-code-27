from itertools import permutations


int_with_digits = ["_{}int_".format(num) for num in range(1, 13)]
float_with_digits = [
    "_{}float{}_".format(pair[0], pair[1]) for pair in list(
        permutations(list(range(1, 13)), 2)
    ) if pair[1] < 5
]

RESERVED_TOKENS = [
    "_int_",
    "_float_",
    "_num_",
] + int_with_digits + float_with_digits


from .purewords_tokenizer import PureWordsTokenizer  # noqa
from .parallel_jieba_tokenizer import ParallelJiebaTokenizer  # noqa
from .chinese_char_tokenizer import ChineseCharTokenizer  # noqa
from .pure_char_tokenizer import PureChineseCharTokenizer  # noqa
from .custom_jieba_tokenizer import CustomJiebaTokenizer  # noqa
from .nltk_tokenizer import NltkTokenizer  # noqa
from .nltk_custom_jieba_tokenizer import NltkCustomJiebaTokenizer  # noqa
from .add_words import AddWords  # noqa
