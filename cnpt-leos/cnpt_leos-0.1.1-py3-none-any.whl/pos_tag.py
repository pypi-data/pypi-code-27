"""
Wrapper over nltk.pos_tag
Allows to use custom part of speech tags
"""
import nltk
from typing import List, Tuple

from .injector import Injector
from .rule import Rule


def pos_tag(text: str, rules: List[Rule], lang: str = 'rus') -> List[Tuple[str, str]]:
    """
    Parameters
        text: str
            input text
        rules: List[nltk_custom.rule.Rule]
            rules for custom tags
        lang: str
            language of the input text

    Return
        List[Tuple[str, str]]
            list of tagged words.
    """

    # forward preprocess
    for i, rule in enumerate(rules):
        text, matches = rule.extractor.extract(text)
        rules[i] = rule._replace(matches=matches)

    # split to tags
    tagged_text = _tag_preprocess(text, lang=lang)

    # backward preprocess
    for rule in rules:
        tagged_text = Injector.inject(tagged_text, rule.matches, rule.extractor.keyword.strip())

    return tagged_text


def _tag_preprocess(text: str, lang: str):
    """
    Parameters
        text: str
            input text
        lang: str
            language of the input text

    Return
        List[Tuple[str, str]]
            tagged words of the input text
    """
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent, lang=lang) for sent in sentences]
    return [y for x in sentences for y in x]
