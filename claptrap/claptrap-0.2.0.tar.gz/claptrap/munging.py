import collections
import contextlib
import itertools
import json

# import lzma
import re
import random
import struct


# whole words and some punctuation
ELEMENT_MATCHER = r"((Dr|Mr|Mrs|Prof).|\b[a-zA-Z\']+\b|;|:|,|\.|\?|!)"

QUOTE_TRANS = str.maketrans(
    {
        # "\N{LEFT SINGLE QUOTATION MARK}": "'",
        # "\N{RIGHT SINGLE QUOTATION MARK}": "'",
        # "\N{LEFT DOUBLE QUOTATION MARK}": '"',
        # "\N{RIGHT DOUBLE QUOTATION MARK}": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u201C": '"',
        "\u201D": '"',
    }
)


def gen_words(*, filename=None, text=None, harmonize_caps=True):
    if filename:
        with open(filename, encoding="utf-8") as f:
            lines = [line for line in f if not line.isupper()]
    else:
        lines = text.splitlines()

    if harmonize_caps:
        translator = most_common_capitalization(
            gen_words(filename=filename, text=text, harmonize_caps=False)
        )
    else:
        translator = {}

    for line in lines:
        line = line.translate(QUOTE_TRANS)
        for word in re.findall(ELEMENT_MATCHER, line):
            word = word[0]
            yield translator.get(word, word)


def most_common_capitalization(words):
    case_sensitive = collections.Counter(words)
    case_insensitive = collections.defaultdict(dict)
    for word, count in case_sensitive.items():
        case_insensitive[word.lower()][word] = count

    translator = {}
    for lower, counts in case_insensitive.items():
        if len(counts) < 2:
            continue
        winner = max(counts.items(), key=lambda x: x[1])[0]

        for variant in counts:
            translator[variant] = winner

    return translator


def word_gen(words, smat):
    try:
        state = words.index(".")
    except ValueError:
        state = random.randrange(len(smat))
    while True:
        try:
            indexes, weights = smat[state]
            state = indexes[
                random.choices(list(range(len(indexes))), weights=weights)[0]
            ]
        except IndexError:  # dead-end states
            state = random.randrange(len(smat))
        yield words[state]


PUNCTUATION = set(",.;:?!")
TERMINAL_PUNCT = set(".?!")


def title(word):
    '''Because "it's".title() == "It'S"'''
    return word[0].upper() + word[1:]


def phrase(word_gen, length=100):
    """Generate some random "words" with some specified total char length"""
    try:
        min_length, max_length = length
    except TypeError:
        min_length = max_length = length

    rule = title(next(w for w in word_gen if w.isalpha()))
    for word in word_gen:
        if word in PUNCTUATION:
            if rule[-1] in PUNCTUATION:
                continue
            rule += word
        elif rule[-1] in TERMINAL_PUNCT:
            rule += " " + title(word)
        else:
            rule += " " + word
        if len(rule) >= min_length:
            break
    rule = rule[:max_length]
    if rule[-1] == " ":
        if rule[-2] in PUNCTUATION:
            return rule[:-2] + "s" + random.choice(list(TERMINAL_PUNCT))
        return rule[:-1] + "s"
    if rule[-1] in PUNCTUATION:
        return rule[:-1] + random.choice(list(TERMINAL_PUNCT))
    return rule
