import re
import time
from textwrap import wrap
from typing import Union

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
    o = "{:{}<{}}".format(text, char, width)
    return o

def center_on(value:str, text:str) -> str:
    return u"{:^{}}".format(value, len(text))

def wall_text(text:str, width:int=80, wall:str= "|", text_alignment="<", h_padding=2) -> str:
    pad = _get_padding(h_padding)
    text_alignment = _get_alignment(text_alignment)
    result, adjusted = "", width - len(wall) * 2 - h_padding * 2
    executed = False
    for line in wrap(text, width=adjusted):
        executed = True
        if line == "":
            line = " "
        result += "{}{}{:{}{}}{}{}\n".format(wall, pad, line, text_alignment, adjusted, pad, wall)
    if not executed:
        result = "{}{}{:{}{}}{}{}\n".format(wall, pad, " ", text_alignment, adjusted, pad, wall)
    return result[:-1]

def box_text(text:str, width:int=80, roof:str= "-", wall:str= "|") -> str:
    line = create_line(char=roof, width=width)
    walled = wall_text(text, wall=wall)
    return f"{line}\n{walled}\n{line}"


def regex(expr:str, text:str, only_first:bool=False, suppress:bool=False) -> str:
    if only_first:
        if suppress:
            try:
                return re.search(expr, text).group(0)
            except:
                pass
        else:
            return re.search(expr, text).group(0)
    else:
        yield from (x for x in re.findall(expr, text))

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