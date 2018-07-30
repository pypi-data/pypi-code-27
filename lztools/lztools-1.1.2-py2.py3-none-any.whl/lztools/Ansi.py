import re

_c_ = {
    "Red": "\033[31m",
    "Cyan": "\033[96m",
    "Yellow": "\033[33m",
    "Bold": "\033[1m",
    "Reverse": "\033[7m",
    "Reset": "\033[0m"
}

__extra_symbols = [
    "\x1b",
    "\x00",
    "\x01",
    "\x02",
    "\x03",
    "\x04",
    "\x05",
    "\x06",
    "\x07",
    "\x08",
    "\x09",
    "\x10"
]

def true_length(string):
    for astr in _c_.values():
        string = string.replace(astr, "")
    return len(string)

def cyan(string):
    return "{}{}{}".format(_c_['Cyan'], string, _c_['Reset'])

def red(string):
    return "{}{}{}".format(_c_['Red'], string, _c_['Reset'])

def yellow(string):
    return "{}{}{}".format(_c_['Yellow'], string, _c_['Reset'])

def bold(string):
    return "{}{}{}".format(_c_['Bold'], string, _c_['Reset'])

def reverse(string):
    return "{}{}{}".format(_c_['Reverse'], string, _c_['Reset'])

def strip(text):
    for c in _c_.values():
        text = text.replace(c, "")
    for s in __extra_symbols:
        text = text.replace(s, "")
    return text

def strip_reg(text):
    text = text.encode('string-escape')
    text = re.sub(r"\\x1b", '', text)
    text = re.sub(r"\\x[0-9][0-9]", '', text)
    return text.decode('string-escape')

def ansi_length(string, count_close=True):
    rst = _c_["Reset"]
    lis = _c_.values()
    if not count_close:
        lis.remove(rst)
    for astr in lis:
        string = string.replace(astr, " ")
    string = string.replace(rst, "")
    return len(string)

# def ansi_length(string):
#     for astr in _c_.values():
#         string = string.replace(astr, " ")
#     return len(string)
