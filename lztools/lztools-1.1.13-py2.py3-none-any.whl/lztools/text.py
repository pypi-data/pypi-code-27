import random
import re
import time
from typing import Union
from ansiwrap import wrap

from lztools import Ansi

_words = None

def words():
    from lztools.Bash import command_result
    global _words
    if _words is None:
        _words = command_result("cat", "/usr/share/dict/words")
    return _words

def _get_alignment(alignment:str) -> str:
    if alignment in ["<", "l", "left"]:
        return "<"
    elif alignment in [">", "r", "right"]:
        return ">"
    elif alignment in ["^", "c", "center"]:
        return "^"
    else:
        raise ValueError("Alignment argument not understood")
def _get_padding(padding:int, char:str=" ") -> str:
    result = ""
    for _ in range(0, padding, len(char)):
        result += char
    return result

def create_line(char:str= "-", width:int=200, text:str= "") -> str:
    o = pad_length(text, width, text_alignment="<", pad_char=char)
    return o

def center_on(value:str, text:str) -> str:
    return u"{:^{}}".format(value, len(text))

def pad_length(text:str, width:int, text_alignment:str, pad_char=" ") -> str:
    alignment = _get_alignment(text_alignment)
    if alignment == "^":
        while Ansi.true_length(text) < width:
            text += pad_char
            if Ansi.true_length(text) < width:
                text = pad_char + text
    elif alignment == "<":
        while Ansi.true_length(text) < width:
            text += pad_char
    elif alignment == ">":
        while Ansi.true_length(text) < width:
            text = pad_char + text
    return text

def wall_text(text:str, width:int=80, wall:str= "|", text_alignment="<", h_padding=2, colorizer=None) -> str:
    pad = _get_padding(h_padding)
    text_alignment = _get_alignment(text_alignment)

    result, adjusted = "", width - len(wall) * 2 - h_padding * 2
    executed = False
    for lt in text.splitlines():
        for line in wrap(lt, width=adjusted):
            if colorizer:
                line = colorizer(line)
            executed = True
            line = pad_length(line, adjusted, text_alignment)
            if line == "":
                line = " "
            result += "{}{}{:{}{}}{}{}\n".format(wall, pad, line, text_alignment, adjusted, pad, wall)
    if not executed:
        result = "{}{}{:{}{}}{}{}\n".format(wall, pad, " ", text_alignment, adjusted, pad, wall)
    return result[:-1]

def box_text(text:str, width:int=80, roof:str= "-", wall:str= "|", text_alignment="<") -> str:
    line = pad_length("", width=width, text_alignment=text_alignment, pad_char=roof)
    walled = wall_text(text, wall=wall, text_alignment=text_alignment)
    return f"{line}\n{walled}\n{line}"


def regex(expr:str, text:str, only_first:bool=False, suppress:bool=False) -> str:
    if not only_first:
        return _regex(expr, text, only_first, suppress)
    else:
        try:
            return _regex(expr, text, only_first, suppress).__next__()
        except Exception as e:
            if not suppress:
                raise

def _regex(expr:str, text:str, only_first:bool=False, suppress:bool=False) -> str:
    gen = (x for x in re.findall(expr, text))
    if only_first:
        if suppress:
            try:
                yield gen.__next__()
            except:
                pass
        else:
            yield gen.__next__()
    else:
        yield from gen

def wrap_lines(text: str, width: int = 80) -> str:
    for line in text.splitlines():
        yield from (line[i:i + width] for i in range(0, len(line), width))


def insert_spaces(name:str, underscore:str="") -> str:
    s, n = u"", name[:-4]
    s = s.replace(u"_", underscore)[:-1]
    n = re.sub(r"(?<=\w)([A-Z])", r" \1", str(n))
    return u"{}{}".format(s, n)

def trim_end(remove:str, the_text:str) -> str:
    while the_text.endswith(remove):
        the_text = the_text[:-len(remove)]
    return the_text

def format_seconds(sec:Union[int, float, str]) -> str:
    return time.strftime('%H:%M:%S', time.gmtime(sec))

def search_words(term, strict=False):
    for word in words():
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
    return random.choice(list(words()))