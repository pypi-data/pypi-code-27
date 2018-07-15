"""
Little module offering functions to destroy text by repeated Google
translations.

.. moduleauthor:: Signaltonsalat
"""
import logging as log
import random

import click
import googletrans

from fuzzywuzzy import fuzz


def validate_path(path):
    """
    Takes a comma-separated list of languages and validates that each language
    is contained in :py:data:`googletrans.LANGUAGES`

    Args:
        path (str): Comma-separated list of languages as a string.

    Returns:
        The validated list of each language as a list.

    Raises:
        ValueError: If the path string contains invalid languages.

    Examples:
        Validate a translation from English, to Japanese, to English:

        .. code-block:: python

            path = validate_path('en,ja,en')

    """
    path = [step.lower().strip() for step in path.split(',')]
    if len(path) < 2:
        raise ValueError('Path needs to be at least two languages long.')
    for step in path:
        if step not in googletrans.LANGUAGES:
            raise ValueError('Language not known: {}'.format(step))
    return path


def path_schwurbel(path, text):
    """
    Feeds the given text through the given path of languages. The resulting
    translation is returned.

    Args:
        path (list): List of languages to translate through.
        text (str): The text to translate.

    Returns:
        The resulting translated text as a string.

    Examples:
        Translate "My hovercraft is full of eels." from English to Japanese and
        back to English:

        .. code-block:: python

            path = 'en,ja,en'
            text = 'My hovercraft is full of eels.'
            translated = path_schwurbel(path, text)

    """
    trans = googletrans.Translator()

    translated = text
    for src, dest in zip(path, path[1:]):
        translated = trans.translate(translated, src=src, dest=dest)
        assert translated.src == src
        assert translated.dest == dest
        translated = translated.text

    return translated


def set_ratio_schwurbel(text, lang,
                        langs=','.join(googletrans.LANGUAGES.keys()),
                        target_ratio=50):
    """
    Translates the given text through random languages until it only resembles
    the original text by the given ratio. The comparison metric used is a token
    set ratio.

    Args:
        text (str): The text to schwurbel.
        lang (str): The language the text is in.
        langs (str): Comma-separated list of available languages to chose from.
        target_ratio (int): The target ratio to achieve before returning.

    Returns:
        The text re-translated to the given target ratio.

    Raises:
        ValueError: If the given languages are invalid.
    """
    log.debug('Performing set ratio schwurbel going for a ratio of: %s', ratio)
    validate_path(langs)
    validate_path(lang)
    trans = googletrans.Translator()
    langs = {l for l in langs.split(',')}
    stack = [text]
    last_ratio = 100
    while last_ratio > target_ratio:
        cur_text = stack[-1]
        nxt_lang = random.sample(langs, 1)[0]
        nxt_text = trans.translate(cur_text, src=lang, dest=nxt_lang)
        nxt_text = nxt_text.text
        nat_text = trans.translate(nxt_text, src=nxt_lang, dest=lang)
        nat_text = nat_text.text
        current_ratio = fuzz.token_set_ratio(text, nat_text)
        if current_ratio < last_ratio:
            last_ratio = current_ratio
            stack.append(nat_text)
            log.debug('Got schwurbel with %s <? %s ratio: %s', last_ratio,
                      target_ratio, nat_text)
    return nat_text


@click.group()
def cli():
    """
    Click group bundling together available commands.
    """
    pass


@cli.command()
@click.option('--path', default='en,ja,de,en')
@click.argument('text')
def fixed(path, text):
    """
    Click command to perform a path schwurbel with the given parameters.
    """
    print('Doing fixed schwurbel: ', text)
    path = validate_path(path)
    translated = path_schwurbel(path, text)
    print()
    print('Result: ', translated)


@cli.command()
@click.option('--lang', default='en')
@click.option('--langs', default=','.join(googletrans.LANGUAGES.keys()))
@click.option('--target_ratio', default=50)
@click.argument('text')
def ratio(lang, langs, target_ratio, text):
    """
    Click command to perform a set ratio schwurbel with the given parameters.
    """
    print('Doing ratio schwurbel: ', text)
    schwurbel = set_ratio_schwurbel(text, lang, langs, target_ratio)
    print()
    print('Result: ', schwurbel)


if __name__ == '__main__':
    cli()
