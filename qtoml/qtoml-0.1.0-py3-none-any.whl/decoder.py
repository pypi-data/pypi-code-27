#!python3

import re, datetime

def load(fo):
    """Load TOML data from a file-like object fo, and return it as a dict.

    """
    s = fo.read()
    return loads(s)

class ParseState:
    """A parser state. Holds the entire input string, advances through it as
    requested. Also tracks line and column for error reporting.

    """
    def __init__(self, string, line=1, col=0):
        self._string = string
        self._index = 0
        self.line = line
        self.col = col

    def at_string(self, s):
        return self._string[self._index:self._index + len(s)] == s

    def at_end(self):
        return self._index >= len(self._string)

    def len(self):
        return len(self._string) - self._index

    def get(self, n):
        return self._string[self._index:self._index + n]

    def advance_through_class(self, cls):
        i = self._index
        while True:
            if i < len(self._string) and self._string[i] in cls:
                i += 1
            else:
                break
        return self.advance(i - self._index)

    def advance_until(self, s):
        i = self._string.find(s, self._index)
        if i == -1:
            i = len(self._string)
        else:
            i += len(s)
        return self.advance(i - self._index)

    def advance(self, n):
        d = self._string[self._index:self._index + n]
        lc = d.count('\n')
        cc = len(d.rpartition("\n")[2])
        self.line += lc
        if lc > 0:
            self.col = cc
        else:
            self.col += cc
        self._index += n
        return d

    def __repr__(self):
        return ("ParseState({}, line={}, col={})".
                format(repr(self._string), self.line, self.col))

class TOMLDecodeError(Exception):
    def __init__(self, msg, parse, *args, **kwargs):
        super().__init__("{} (line {}, column {})".
                         format(msg, parse.line, parse.col))

def parse_throwaway(p):
    s = ""
    while True:
        s += p.advance_through_class(" \t\r\n")
        if p.at_string("#"):
            s += p.advance_until("\n")
        else:
            break
    lines = s.count("\n")
    return lines, p

def class_partition(cls, string):
    """Given a set of characters and a string, take the longest prefix made up of
    the characters in the set, and return a tuple of (prefix, remainder).

    """
    ns = string.lstrip(cls)
    lc = len(string) - len(ns)
    return (string[:lc], string[lc:])

def class_rpartition(cls, string):
    """As class_partition, but for rpartition/rstrip"""
    ns = string.rstrip(cls)
    lc = len(string) - len(ns)
    if lc == 0:
        return (string, '')
    return (string[:-lc], string[-lc:])

escape_vals = { 'b': "\b", 't': "\t", 'n': "\n", 'f': "\f", 'r': "\r",
                '"': '"', '\\': '\\' }
def parse_string(p, delim='"', allow_escapes=True, allow_newlines=False,
                 whitespace_escape=False):
    if not p.at_string(delim):
        raise TOMLDecodeError(f"string doesn't begin with delimiter '{delim}'",
                              p)
    p.advance(len(delim))
    sv = ""
    while True:
        # endquote = string.find(delim, endquote + len(delim))
        sv += p.advance_until(delim)
        if p.at_end() and not sv.endswith(delim):  # closing quote not found
            raise TOMLDecodeError("end of file inside string", p)
        # get all backslashes before the quote
        if allow_escapes:
            # a, b = class_rpartition("\\", string[:endquote])
            a, b = class_rpartition("\\", sv[:-len(delim)])
            if len(b) % 2 == 0:  # if backslash count is even, it's not escaped
                break
        else:
            break
        if p.at_end():
            raise TOMLDecodeError("end of file after escaped delimiter", p)
    sv = sv[:-len(delim)]
    if "\n" in sv and not allow_newlines:
        raise TOMLDecodeError("newline in basic string", p)
    if allow_newlines and sv.startswith("\n"):
        sv = sv[1:]
    bs = 0
    last_subst = ''
    while allow_escapes:
        bs = sv.find("\\", bs + len(last_subst))
        if bs == -1:
            break
        escape_end = bs + 2
        ev = sv[bs + 1]
        if ev in escape_vals:
            subst = escape_vals[ev]
        elif ev == 'u':
            hexval = sv[bs + 2:bs + 6]
            if len(hexval) != 4:
                raise TOMLDecodeError("hexval cutoff in \\u", p)
            try:
                subst = chr(int(hexval, base=16))
            except ValueError as e:
                raise TOMLDecodeError(f"bad hex escape '\\u{hexval}'", p) from e
            escape_end += 4
        elif ev == 'U':
            hexval = sv[bs + 2:bs + 10]
            if len(hexval) != 8:
                raise TOMLDecodeError("hexval cutoff in \\U", p)
            try:
                subst = chr(int(hexval, base=16))
            except ValueError as e:
                raise TOMLDecodeError(f"bad hex escape '\\U{hexval}'", p) from e
            escape_end += 8
        elif whitespace_escape and ev == '\n':
            a, b = class_partition(" \t\n", sv[bs + 2:])
            escape_end += len(a)
            subst = ''
        else:
            raise TOMLDecodeError(f"\\{ev} not a valid escape", p)
        sv = sv[:bs] + subst + sv[escape_end:]
        last_subst = subst
    return sv, p  # .advance(adv_len)

num_re = re.compile(r"[+-]?([0-9]|[1-9][0-9_]*[0-9])" +
                    r"(?P<frac>\.([0-9]|[0-9][0-9_]*[0-9]))?" +
                    r"(?P<exp>[eE][+-]?([0-9]|[1-9][0-9_]*[0-9]))?" +
                    r"(?=([\s,\]]|$))")
def parse_num(p):
    string = p.advance_through_class("+-0123456789_.eE")
    o = num_re.match(string)
    if o is None:
        raise TOMLDecodeError("tried to parse_num non-num", p)
    mv = o.group(0)
    if '__' in mv:
        raise TOMLDecodeError("double underscore in number", p)
    sv = mv.replace('_', '')
    if o.group('frac') or o.group('exp'):
        rv = float(sv)
    else:
        rv = int(sv)
    return rv, p

def parse_array(p):
    rv = []
    atype = None
    if not p.at_string('['):
        raise TOMLDecodeError("tried to parse_array non-array", p)
    p.advance(1)
    n, p = parse_throwaway(p)
    while True:
        if p.at_string(']'):
            p.advance(1)
            break
        v, p = parse_value(p)
        if atype is not None:
            if type(v) != atype:
                raise TOMLDecodeError("array of mixed type", p)
        else:
            atype = type(v)
        rv.append(v)
        n, p = parse_throwaway(p)
        if p.at_string(','):
            p.advance(1)
            n, p = parse_throwaway(p)
            continue
        if p.at_string(']'):
            p.advance(1)
            break
        else:
            raise TOMLDecodeError(f"bad next char {p.get(0)} in array", p)
    return rv, p

dt_re = re.compile(r"(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)T" +
                   r"(?P<hr>\d\d):(?P<min>\d\d):(?P<sec>\d\d)" +
                   r"(\.(?P<msec>\d{6}))?(?P<tz>(Z|[+-]\d\d:\d\d))")
def parse_dt_string(s):
    o = dt_re.match(s)
    if o is None:
        return None
    year, month, day, hour, minute, sec = [
        int(o.group(i)) for i in ['year', 'month', 'day', 'hr', 'min', 'sec']]
    msec = int(o.group('msec')) if o.group('msec') else 0
    tz = o.group('tz')
    if tz == 'Z':
        tzi = datetime.timezone.utc
    else:
        td = datetime.timedelta(hours=int(tz[1:3]), minutes=int(tz[4:6]))
        if tz[0] == '-':
            td = -td
        tzi = datetime.timezone(td)
    rv = datetime.datetime(year, month, day, hour, minute, sec, msec, tzi)
    return rv

def parse_datetime(p):
    string = p.advance_through_class("0123456789-T:+Z")
    rv = parse_dt_string(string)
    if rv is None:
        raise TOMLDecodeError("tried to parse_datetime non-dt", p)
    return rv, p

def parse_inline_table(p):
    if not p.at_string('{'):
        raise TOMLDecodeError("tried to parse_inline_table non-table", p)
    rv = {}
    p.advance(1)
    p.advance_through_class(" \t")
    while True:
        if p.at_string('}'):
            break
        k, p = parse_key(p)
        p.advance_through_class(" \t")
        if not p.at_string('='):
            raise TOMLDecodeError(f"no = after key {k} in inline", p)
        p.advance(1)
        p.advance_through_class(" \t")
        v, p = parse_value(p)
        p.advance_through_class(" \t")
        if k in rv:
            raise TOMLDecodeError(f"duplicated key '{k}' in inline", p)
        rv[k] = v
        if p.at_string(','):
            p.advance(1)
            p.advance_through_class(" \t")
            continue
        if p.at_string('}'):
            p.advance(1)
            break
        else:
            raise TOMLDecodeError(f"bad next char {repr(p.get(1))}" +
                                  " in inline table", p)
    return rv, p

def parse_dispatch_string(p, multiline_allowed=True):
    if p.at_string('"""'):
        if not multiline_allowed:
            raise TOMLDecodeError("multiline string where not allowed", p)
        val, p = parse_string(p, delim='"""', allow_escapes=True,
                              allow_newlines=True, whitespace_escape=True)
    elif p.at_string('"'):
        val, p = parse_string(p, delim='"', allow_escapes=True,
                              allow_newlines=False, whitespace_escape=False)
    elif p.at_string("'''"):
        if not multiline_allowed:
            raise TOMLDecodeError("multiline string where not allowed", p)
        val, p = parse_string(p, delim="'''", allow_escapes=False,
                              allow_newlines=True, whitespace_escape=False)
    elif p.at_string("'"):
        val, p = parse_string(p, delim="'", allow_escapes=False,
                              allow_newlines=False, whitespace_escape=False)
    return val, p

def parse_value(p):
    if p.get(1) in ["'", '"']:
        val, p = parse_dispatch_string(p)
    elif p.at_string('['):
        val, p = parse_array(p)
    elif p.at_string('{'):
        val, p = parse_inline_table(p)
    elif p.at_string('true'):
        val = True
        p.advance(4)
    elif p.at_string('false'):
        val = False
        p.advance(5)
    elif num_re.match(p.get(p.len())):
        val, p = parse_num(p)
    elif dt_re.match(p.get(25)):
        val, p = parse_datetime(p)
    else:
        raise TOMLDecodeError("can't parse type", p)
    return val, p

# characters allowed in unquoted keys
key_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
def parse_key(p):
    ic = p.get(1)
    if ic in ['"', "'"]:
        k, p = parse_dispatch_string(p, multiline_allowed=False)
    elif ic in key_chars:
        k = p.advance_through_class(key_chars)
    else:
        raise TOMLDecodeError(f"'{p.get(1)}' cannot begin key", p)
    return k, p

def parse_pair(p):
    if p.at_end():
        return (None, None), p
    k, p = parse_key(p)
    p.advance_through_class(" \t")
    if not p.at_string('='):
        raise TOMLDecodeError(f"no = following key '\"{k}\"'", p)
    p.advance(1)
    p.advance_through_class(" \t")
    v, p = parse_value(p)
    return (k, v), p

def parse_tablespec(p):
    if not p.at_string('['):
        raise TOMLDecodeError("tried parse_tablespec on non-tablespec", p)
    p.advance(1)
    tarray = False
    if p.at_string('['):
        p.advance(1)
        tarray = True
    p.advance_through_class(" \t")
    rv = []
    while True:
        k, p = parse_key(p)
        p.advance_through_class(" \t")
        rv.append(k)
        if p.at_string('.'):
            p.advance(1)
            p.advance_through_class(" \t")
        elif p.at_string(']'):
            p.advance(1)
            break
        else:
            raise TOMLDecodeError(f"Bad char {repr(p.get(1))} in tablespec",
                                  p)
    if tarray:
        if not p.at_string(']'):
            raise TOMLDecodeError(f"Didn't close tarray properly", p)
        p.advance(1)
    return rv, p

def proc_kl(rv, kl, tarray, p):
    """Handle a table spec keylist, modifying rv in place; returns target"""
    c = rv
    # all entries except last must be dicts
    for i in kl[:-1]:
        if i in c:
            if type(c[i]) not in [dict, list]:
                raise TOMLDecodeError(f"repeated key in keylist {repr(kl)}", p)
        else:
            c[i] = {}
        c = c[i] if type(c[i]) == dict else c[i][-1]
    fk = kl[-1]
    if tarray:
        if fk in c:
            if type(c[fk]) != list:
                raise TOMLDecodeError(f"repeated key in keylist {repr(kl)}", p)
        else:
            c[fk] = []
        c[fk].append({})
        return c[fk][-1]
    else:
        if fk in c:
            if type(c[fk]) != dict:
                raise TOMLDecodeError(f"repeated key in keylist {repr(kl)}", p)
        else:
            c[fk] = {}
        return c[fk]

def loads(string):
    """Load TOML data from the string passed in, and return it as a dict."""
    rv = {}
    cur_target = rv
    p = ParseState(string)
    first = True
    n = 0
    # this tracks tables we've already seen just so we can error out on
    # duplicates as spec requires
    toplevel_targets = set()
    while not p.at_end():
        n2, p = parse_throwaway(p)
        n += n2
        if not first:
            if n == 0:
                raise TOMLDecodeError("Didn't find expected newline", p)
        else:
            first = False
        if p.at_string('['):
            tarray = p.get(2) == '[['
            kl, p = parse_tablespec(p)
            cur_target = proc_kl(rv, kl, tarray, p)
            if id(cur_target) in toplevel_targets:
                raise TOMLDecodeError(f"duplicated table {kl}", p)
            toplevel_targets.add(id(cur_target))
        else:
            (k, v), p = parse_pair(p)
            if k in cur_target:
                raise TOMLDecodeError(f"Key '{k}' is repeated", p)
            cur_target[k] = v
        n, p = parse_throwaway(p)
    return rv
