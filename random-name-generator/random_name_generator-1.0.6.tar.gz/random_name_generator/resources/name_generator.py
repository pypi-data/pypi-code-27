from .nouns import (
    add_prefix, add_postfix, concatenate_words
)


def generate_name(**kwargs):
    prefix = kwargs.get('prefix', None)
    postfix = kwargs.get('postfix', None)
    number_of_word = kwargs.get('number_of_word', 1)
    separate_char = kwargs.get('separate_char', '_')
    return add_postfix(add_prefix(prefix, concatenate_words(number_of_word, separate_char), ''), separate_char, postfix)
