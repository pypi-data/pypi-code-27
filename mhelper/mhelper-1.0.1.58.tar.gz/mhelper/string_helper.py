"""
Functions for processing strings.

Some of the following functions explicitly denote `TStr` instead of `str`, where `TStr` is a `str`-like class. For a correctly implemented class the return value is then `TStr`.
This makes these functions applicable to arrays or special string instances such as `ansi_helper.AnsiStr`.
"""

import datetime
import re
import warnings
from collections import Counter, defaultdict
from typing import Callable, Iterable, Iterator, List, Optional, Union, cast, Tuple

from mhelper import array_helper
from mhelper.exception_helper import SwitchError
from mhelper.special_types import NOT_PROVIDED


TStr = str
__strip_lines_rx = re.compile( r"^[ ]+", re.MULTILINE )
__word_delimiter_rx = re.compile( r"([" + re.escape( "\t\n\x0b\x0c\r " ) + r"]+)" )
__author__ = "Martin Rusilowicz"


def first_words( t: str, min_length = 1 ) -> str:
    """
    Returns a string made up of the first and last words (optionally allows a min_length of first words)
    """
    result = ""
    last_iter = ""
    for match in re.finditer( r"[\w]+", t ):
        if len( match.group( 0 ) ) <= 1:
            continue
        
        last_iter = match.group( 0 )
        
        if len( result ) < min_length:
            if result:
                result += " "
            result += last_iter
            last_iter = None
    if result:
        if last_iter:
            return result + " " + last_iter
        else:
            return result
    else:
        return t


def first_word( t: str ) -> str:
    """
    Returns the first word from the string
    """
    match = re.match( r"[\w]+", t )
    
    if not match:
        return t
    
    return match.group( 0 )


def time_to_string( time: float ) -> str:
    """
    Given a time in seconds, returns an approximate string representation like "5 seconds", "4 minutes", etc.
    """
    if time <= 1.5:
        return str( round( time * 1000 ) ) + " milliseconds"
    
    if time < 60:
        return str( round( time ) ) + " seconds"
    
    time /= 60
    
    if time < (60 * 2):
        return str( round( time ) ) + " minutes"
    
    time /= 60
    
    return str( round( time ) ) + " hours"


def time_to_string_short( time: float, delimiter: str = ":" ) -> str:
    """
    Given a time in seconds, returns a formatted string like "00:05", or "02:01:05".
    """
    SECONDS_IN_ONE_HOUR = 60 * 60
    SECONDS_IN_ONE_MINUTE = 60
    
    hours = time // SECONDS_IN_ONE_HOUR
    time -= hours * SECONDS_IN_ONE_HOUR
    
    minutes = time // SECONDS_IN_ONE_MINUTE
    time -= minutes * SECONDS_IN_ONE_MINUTE
    
    seconds = time
    
    h_text = ""
    
    if hours:
        h_text = str( int( hours ) ) + delimiter
    
    m_text = str( int( minutes ) ).rjust( 2, "0" ) + delimiter
    
    s_text = str( int( seconds ) ).rjust( 2, "0" )
    
    return h_text + m_text + s_text


def highlight_words( text: str, words, colour, normal ):
    text = normal + text
    
    for x in words:
        text = highlight_regex( text, "/\b($" + x + ")\b/i", colour, normal )
    
    return text


def regex_extract( regex, text, group = 1 ):
    m = re.search( regex, text )
    
    if m is None:
        return ""
    
    return m.group( group )


def highlight_regex( text, regex, colour, normal, group = 1 ):
    l = len( colour ) + len( normal )
    
    for i, m in enumerate( re.finditer( regex, text, re.IGNORECASE ) ):
        if group > m.lastindex:
            continue
        
        s = m.start( group ) + l * i
        e = m.end( group ) + l * i
        
        text = text[:s] + colour + text[s:e] + normal + text[e:]
    
    return text


def highlight_quotes( text, start, end, colour, normal ):
    find = start + "([^" + start + end + "]+)" + end
    replace = colour + "\\1" + normal
    return re.sub( find, replace, text )


def curtail( text: str, start: Optional[str] = None, end: Optional[str] = None, error = False ):
    """
    Removes text from the start of end of a string
    """
    if start:
        if text.startswith( start ):
            text = text[len( start ):]
        elif error:
            raise KeyError( "Trying to remove the substring «{0}» from the string «{1}» but the string does not start with the substring.".format( start, text ) )
    
    if end:
        if text.endswith( end ):
            text = text[:len( text ) - len( end )]
        elif error:
            raise KeyError( "Trying to remove the substring «{0}» from the string «{1}» but the string does not end with the substring.".format( end, text ) )
    
    return text


def time_now() -> str:
    t = datetime.datetime.now()
    return t.strftime( '%Y-%m-%d %H:%M:%S' )


def percent( n: float = None, d: float = None, q = None, t = 0, dp: int = 0 ):
    """
    Formats a value percentage from either the quotient (Q), the numerator (N) and/or the denominator (D).

    ```
    percent( quotient )                         # N and D unknown, defaults to `t = 1`
    percent( numerator, denominator, quotient ) # D, D, Q specified explicitly, defaults to `t = 3`
    percent( numerator, denominator )           # Q calculated automatically, defaults to `t = 2` 
    percent( numerator, q = quotient )          # D calculated automatically, defaults to `t = 2`
    percent( q = quotient, d = denominator )    # N calculated automatically, defaults to `t = 2`
    ```
    
    "q.q%" if `t` is 1.
    
    ```
    percent( 0.5 )                      # 50%
    percent( 5, 10, t = 1 )             # 50%
    ```
    
    "n (q.q%)" if `t` if 2 (requires N and D, otherwise uses `t` = 1).

    ```
    percent( 5, 10 )                    # 5 (50%)
    ```
    
    "n/d (q.q%)" if `t` is 3 (requires N and D, otherwise uses `t` = 1).
    
    ```
    percent( 5, 10, t = 3 )             # 5/10 (50%)
    ```
    
    This is a function for display, hence there are no "division by zero" errors and 0% is
    displayed if both numerator and denominator are zero (if the denominator alone is zero,
    then `"inf%"` is still used).

    :param n:   Specifies the quotient, unless either of `q` or `d` are specified, in which case this parameter specifies the numerator. 
    :param d:   Denominator.
    :param q:   Quotient.
    :param t:   Number of terms to display (1, 2 or 3), if 0 assumes the default for the number of terms provided.
    :param dp:  Decimal places to display for Q.
    
    :exception ValueError:  Q missing or cannot be calculated.
    :exception ValueError:  `t` specified when only Q is known.
    :exception SwitchError: `t` is not 1, 2 or 3.
    """
    fmt = "{{:.{}%}}".format( dp )
    
    if d is None and ((q is None) != (n is None)):
        # "D" and "Q" missing
        # "N" is actually "Q"
        if q is None:
            q = n
        
        if (t or 1) != 1:
            raise ValueError( "Cannot specify t = {} when only `q` is provided.".format( t ) )
        
        return fmt.format( q )
    
    if d is None:
        # "D" missing
        if n is None or q is None:
            raise ValueError( "Must specify at least two of n/d/q." )
        
        t = t or 2
        ns = str( n )
        ds = "inf" if q == 0 else str( n / q )
        qs = fmt.format( q )
    elif n is None:
        # "N" missing
        if q is None:
            raise ValueError( "Must specify at least two of n/d/q." )
        
        t = t or 2
        ns = "{0:g}".format( q * d )
        ds = str( d )
        qs = fmt.format( q )
    elif q is None:
        # "Q" missing
        t = t or 2
        ns = str( n )
        ds = str( d )
        qs = fmt.format( n / d ) if d != 0 else "0%" if n == 0 else "inf%"
    else:
        # All provided
        t = t or 3
        ns = str( n )
        ds = str( d )
        qs = fmt.format( q )
    
    if t == 1:
        return "{}".format( qs )
    elif t == 2:
        return "{} ({})".format( ns, qs )
    elif t == 3:
        return "{}/{} ({})".format( ns, ds, qs )
    else:
        raise SwitchError( "t (terms)", t )


def timedelta_to_string( delta ) -> str:
    s = delta.seconds
    hours = s // 3600
    s -= hours * 3600
    minutes = s // 60
    seconds = s - (minutes * 60)
    
    if hours:
        return '%d:%02d:%02d' % (hours, minutes, seconds)
    else:
        return '%02d:%02d' % (minutes, seconds)


def fix_width( text: TStr, width: int = 20, char: TStr = " ", justify = None ) -> TStr:
    if justify is None or justify < 0:
        justify_fn = ljust
    elif justify == 0:
        justify_fn = cjust
    elif justify > 0:
        justify_fn = rjust
    else:
        raise SwitchError( "justify", justify )
    
    return justify_fn( max_width( text, width ), width, char )


def max_width( text: TStr, width: int = 20 ) -> TStr:
    if width <= 1:
        warnings.warn( "Did you really mean to pass <width = {}> to max_width?".format( width ) )
    
    text = text.strip()
    
    if "\n" in text:
        text = text[:text.index( "\n" )]
    
    if len( text ) > width:
        text = text[:(width - 1)] + "…"
    
    assert len( text ) <= width
    return text


def size_to_string( size: int ):
    """
    Returns a `size`, specified in bytes, as a human-readable string, similar to `ls -h` in bash.
    """
    if size == -1:
        return "?"
    
    if size < 1024:
        return "{0:.1f}b".format( size )
    
    size /= 1024
    
    if size < 1024:
        return "{0:.1f}kb".format( size )
    
    size /= 1024
    
    if size < 1024:
        return "{0:.1f}Mb".format( size )
    
    size /= 1024
    
    return "{0:.1f}Gb".format( size )


def summarised_join( source: Counter, delimiter ):
    r = []
    
    for k, v in sorted( source.items(), key = lambda x: -x[1] ):
        r.append( "{1} × {0}".format( k, v ) )
    
    return delimiter.join( r )


def is_int( x ) -> bool:
    if not x:
        return False
    
    try:
        _ = int( x )
        return True
    except:
        return False


def to_int( x ) -> Optional[int]:
    if not x:
        return None
    
    try:
        return int( x )
    except:
        return None


def bulk_replace( text, format = "<*>", **kwargs ):
    for k, v in kwargs.items():
        text = text.replace( format.replace( "*", k ), v )
    
    return text


__make_name_regex = re.compile( "[^0-9a-zA-Z.]" )


def make_name( name ):
    return __make_name_regex.sub( "_", name )


def strip_lines( text ):
    return __strip_lines_rx.sub( "", text )


def prefix_lines( text, prefix, suffix = "" ):
    return prefix + text.replace( "\n", suffix + "\n" + prefix ) + suffix


def remove_prefix( text, prefix ) -> str:
    if not text.startswith( prefix ):
        raise ValueError( "I've been asked to remove a prefix «{0}» from a string «{1}», but the string doesn't start with that prefix.".format( prefix, text ) )
    
    return text[len( prefix ):]


def type_name( value ):
    return type( value ).__name__


def undo_camel_case( text: str, sep = " " ):
    result = []
    
    for i, c in enumerate( text ):
        if i and c.isupper():
            result.append( sep )
        
        result.append( c )
    
    return "".join( result )


def name_index( names: List[str], name: str ) -> int:
    """
    Given a `name`, finds its index in `names`. `name` can be a `str`, an `int` or an int as a str.
    :param names: List of names 
    :param name:  Name or index to find 
    :return: Index
    :exception ValueError: Not found
    """
    if isinstance( name, int ):
        index = name
    elif not isinstance( name, str ):
        raise TypeError( "`name` should be an `int` or a `str`, but it is «{0}» which is a {1}.".format( name, type_name( name ) ) )
    elif all( str.isdigit( x ) for x in name ):
        return int( name )
    else:
        index = None
    
    if index is not None:
        if names is not None:
            if not 0 <= index < len( names ):
                raise ValueError( "Trying to find the column with index «{0}» but that is out of range. The columns are: {1}".format( index, names ) )
        
        return index
    
    if names is None:
        raise ValueError( "Cannot get columns by name «{0}» when there are no headers.".format( name ) )
    
    if name in names:
        return names.index( name )
    
    raise ValueError( "Trying to find the column with header «{0}» but that column doesn't exist. The columns are: {1}".format( name, names ) )


def current_time():
    import time
    return time.strftime( "%Y-%m-%d %H:%M:%S %z" )


def ordinal( i: object ):
    """
    Returns "1st", "2nd", "3rd", etc. from 1, 2, 3, etc.
    `i` can be anything coercible to a string that looks like a number.
    """
    i = str( i )
    l = i[-1]
    
    if l == "1":
        return i + "st"
    elif l == "2":
        return i + "nd"
    elif l == "3":
        return i + "rd"
    else:
        return i + "th"


def get_indent( line ):
    num_spaces = 0
    for x in line:
        if x == " ":
            num_spaces += 1
        else:
            return num_spaces
    
    return num_spaces


def remove_indent( current_indent, line: str ):
    i = 0
    
    for i, x in enumerate( line ):
        if x != " ":
            break
    
    i = min( i, current_indent )
    
    return line[i:]


def capitalise_first_and_fix( text: str, swap = "_-" ) -> str:
    text = capitalise_first( text )
    
    for x in swap:
        text = text.replace( x, " " )
    
    return text


def capitalise_first( text: str ) -> str:
    if text is None:
        return ""
    
    if not text:
        return text
    
    if len( text ) == 1:
        return text[0].upper()
    
    return text[0].upper() + text[1:]


def special_to_symbol( value ):
    return value.replace( "\n", "␊" ).replace( "\r", "␍" ).replace( "\t", "␉" )


def unescape( v ):
    try:
        return v.encode().decode( "unicode_escape" )
    except Exception as ex:
        raise ValueError( "Unescape «{}» failed.".format( v ) ) from ex


def to_bool( x ):
    try:
        y = float( x )
        return y != 0
    except:
        x = x.lower()
        if x in ("true", "yes", "t", "y", "1", "on"):
            return True
        elif x in ("false", "no", "f", "n", "0", "off"):
            return False
        else:
            raise ValueError( "Cannot convert «{}» to boolean.".format( x ) )


DPrint = Callable[[object], None]


class FindError( Exception ):
    pass


def find( *,
          source: Iterable[object],
          search: str,
          namer: Optional[Union[Callable[[object], str], Callable[[object], List[str]]]] = None,
          detail: Optional[str] = None,
          fuzzy: Optional[bool] = True,
          default = NOT_PROVIDED ):
    """
    Finds the command or plugin with the closest name to "text".
    
    :param source:  Source list 
    :param search:  Text to find 
    :param namer:   How to translate items in the source list, each item can translate to a `str`, or a `list` or `tuple` of `str` 
    :param detail:  What to call the collection in error messages.
    :param fuzzy:   Permit partial (start-of-word) matches
    :param default: Default to use. If `NOT_PROVIDED` raises an error.
    :return:        The matching item in `source`
    :except FindError: The text was not matched 
    """
    
    #
    # Arguments
    #
    if not isinstance( source, list ) and not isinstance( source, tuple ):
        source = list( source )
    
    if not isinstance( search, str ):
        raise TypeError( "string_helper.find() takes a `str` and not a {} (`{}`).".format( type( search ).__name__, search ) )
    
    if namer is None:
        namer = cast( Callable[[object], str], str )
    
    
    def __get_names( item ):
        r = namer( item )
        
        if isinstance( r, str ):
            return [r]
        elif isinstance( r, list ) or isinstance( r, tuple ):
            return r
        else:
            raise TypeError( "Return value of namer «{}».".format( namer ) )
    
    
    #
    # Exact match
    #
    for item in source:
        for name in __get_names( item ):
            if search == name:
                return item
    
    #
    # Start-of-word match
    #
    if fuzzy:
        match_items = set()
        match_names = set()
        
        for item in source:
            for name in __get_names( item ):
                if name.startswith( search ):
                    match_items.add( item )
                    match_names.add( name )
        
        if len( match_items ) == 1:
            return array_helper.first_or_none( match_items )
    else:
        match_items = set()
    
    #
    # Failure
    #
    if default is not NOT_PROVIDED:
        return default
    
    if detail is None:
        detail = "item"
    
    if not match_items:
        ss = []
        ss.append( "No such {}: «{}»".format( detail, search ) )
        available = []
        
        for item in source:
            for name in __get_names( item ):
                if name:
                    available.append( name )
        
        if len( available ) < 10:
            ss.append( "Options: " + ", ".join( "«{}»".format( x ) for x in available ) )
        else:
            ss.append( "Options: «{}» items including {}, ...".format( len( available ), ", ".join( "«{}»".format( x ) for x in available[:10] ) ) )
        
        raise FindError( "\n".join( ss ) )
    
    ss = []
    ss.append( "Ambiguous {} name: «{}»".format( detail, search ) )
    ss.append( "    ...did you mean..." )
    for item in match_items:
        for name in __get_names( item ):
            if search in name:
                ss.append( "    ...... " + name.replace( search, "«" + search + "»" ) )
    
    raise FindError( "\n".join( ss ) )


def no_emoji( x ):
    return x + "\uFE0E"


def fix_indents( text: str ) -> str:
    text = str( text )
    lines = text.split( "\n" )
    lines[0] = lines[0].lstrip()
    
    if len( lines ) == 1:
        return lines[0]
    
    min_leading = 9999
    
    for line in lines[1:]:
        stripped = line.lstrip()
        
        if stripped:
            leading = len( line ) - len( stripped )
            min_leading = min( leading, min_leading )
    
    if min_leading == 9999:
        return text.strip()
    
    for i in range( 1, len( lines ) ):
        lines[i] = lines[i][min_leading:]
    
    return "\n".join( lines )


def assert_unicode():
    """
    UTF-8 check. Probably Windows Console Services is badly configured.
    """
    UNICODE_ERROR_MESSAGE = \
        """


        +-------------------------------------------------------------------------------------------------------+--------+
        | UNICODE ENCODE ERROR                                                                                  |        |
        +-------------------------------------------------------------------------------------------------------+  X  X  +
        | It looks like your console doesn't support Unicode.                                                   |        |
        |                                                                                                       |  _--_  |
        | intermake needs Unicode to display its UI.                                                             |        |
        | Python doesn't seem to know your terminal doesn't support UTF8 and just crashes :(                    +--------|
        | This problem usually occurs when using cmd.exe on Windows.                                                     |
        |                                                                                                                |
        | On Windows, you could `set PYTHONIOENCODING=ascii:replace` as a quick fix, but it might be better in the long  |
        | run to setup your console and font to support UTF8: https://stackoverflow.com/questions/379240                 |
        |                                                                                                                |
        | On Unix, the quick fix is `export PYTHONIOENCODING=ascii:replace`                                              |
        +----------------------------------------------------------------------------------------------------------------+


        """
    try:
        print( "😁\r \r", end = "" )
    except UnicodeEncodeError as ex:
        # On the plus side, Window's Console has a horizontal scroll bar, so we can display an over-sized error message without it breaking...
        raise ValueError( UNICODE_ERROR_MESSAGE ) from ex


def centre_align( text, width, char = " ", prefix = None, suffix = None ):
    """
    Centre aligns text.
    :param suffix:  Prefix to use in output. e.g. colour codes that shouldn't be considered as part of the length.
    :param prefix:  Suffix to use in output. e.g. colour codes that shouldn't be considered as part of the length.
    :param text:    Text to align 
    :param width:   Width to align into 
    :param char:    Padding character
    :return:        Aligned text. 
    """
    
    use = text
    
    if prefix:
        use = prefix + use
    
    if suffix:
        use += suffix
    
    length = len( text )
    
    pad_len = (width - length) // 2 - 1
    pad = char * pad_len
    
    if (length % 2) != 0 and (length + pad_len * 2) < width:
        return pad + use + pad + char
    else:
        return pad + use + pad


def as_delta( value ):
    """
    Returns +x or -x 
    """
    if value > 0:
        return "+{}".format( value )
    elif value < 0:
        return "{}".format( value )
    else:
        return "±{}".format( value )


def wrap( text: str, width: int = 70, pad: bool = False ) -> Iterator[str]:
    """
    Iterates over the lines in `text`, word-wrapping to the specified `width`.
     
    :param text:        Text to wrap.
                        This can be a `str` or a `str`-like object such as `AnsiStr`.
                        Only `n = len(text)` and `text[i]` for `i in 0:n` are used, with each `text[i]` always being assumed to have a width of 1.
                        Only `text[i]`'s equality with `" "` and `"\n"` is used to determine spaces and newlines.
    :param width:       Maximum line width 
    :param pad:         When set, all lines are padded to the specified `width` with spaces.
    :return:            An iterator over the lines.
                        A trailing empty line, if present, will not be returned.
    """
    if pad:
        pad_fn = lambda x: x.ljust( width )
    else:
        pad_fn = lambda x: x
    
    if width <= 0:
        for line in str( text ).split( "\n" ):
            yield line
        
        return
    
    text_length = len( text )
    i = 0
    start_line = 0
    last_space = -1
    loop_detector = 0
    max_iter = len( text ) * 10
    
    while i < text_length:
        loop_detector += 1
        
        if loop_detector > max_iter:
            raise ValueError( "Infinite loop when trying to parse text. Loops = {}, text length = «{}», width = «{}», padding = «{}».".format( loop_detector, len( text ), width, pad ) )
        
        c = text[i]
        
        if c == " " or c == "\n":
            if (i - start_line) < width:
                if c == " ":
                    # Still enough space, continue adding
                    last_space = i
                else:  # c == "\n"
                    # Still enough space, print newline now
                    yield pad_fn( text[start_line:i] )
                    start_line = i + 1
                    last_space = start_line
                    
                    # No more room
        if (i - start_line) >= width:
            if start_line != last_space + 1:
                # Backtrack to last space
                i = last_space
                yield pad_fn( text[start_line:i] )
                start_line = i + 1  # skip over space
            else:
                # Cannot backtrack to last space, just take as much as possible
                i = start_line + width
                yield pad_fn( text[start_line:i] )
                start_line = i
                last_space = start_line
        
        i += 1
    
    if i != start_line:
        final = text[start_line:i]
        
        if final.strip():
            yield pad_fn( final )


def ljust( text: TStr, width: int, char: TStr ) -> TStr:
    needed = width - len( text )
    
    if needed <= 0:
        return text
    
    return text + char * needed


def rjust( text: TStr, width: int, char: TStr ) -> TStr:
    needed = width - len( text )
    
    if needed <= 0:
        return text
    
    return char * needed + text


def cjust( text: str, width: int, char: str ) -> str:
    needed = width - len( text )
    
    if needed <= 0:
        return text
    
    text = (char * (needed // 2)) + text
    text = ljust( text, width, char )
    return text


def join_ex( sequence: Iterable[object], delimiter = ", ", last_delimiter = None, formatter = None ) -> str:
    """
    Join, with more functionality.
    
    :param sequence:            Sequence to join, can be any type. 
    :param delimiter:           Delimiter 
    :param last_delimiter:      Delimiter before the final item (e.g. `" and "` or `" or "`). `None` is the same as `delimiter. 
    :param formatter:           Formatter function, such as `str`, or a format string, such as `"{}"`. `None` defaults to `str`.
    :return:                    Joined string. 
    """
    r = []
    
    if last_delimiter is None:
        last_delimiter = delimiter
    
    if formatter is None:
        formatter = str
    elif isinstance( formatter, str ):
        formatter = (lambda f: lambda x: f.format( x ))( formatter )
    
    for i, (x, l) in array_helper.when_last( sequence ):
        if i != 0:
            if l:
                r.append( last_delimiter )
            else:
                r.append( delimiter )
        
        r.append( formatter( x ) )
    
    return "".join( r )


def format_array( array: Iterable,
                  join: str = ", ",
                  final: str = None,
                  sort: bool = False,
                  format: Callable[[object], str] = str,
                  limit: int = -1,
                  limit_symbol: str = "...",
                  empty: str = "∅",
                  autorange: bool = False ) -> str:
    """
    Formats an array
    
    :param autorange:    Create ranges from text.
    :param array:        The array (any iterable) 
    :param join:         How to join 
    :param final:        How to join the final element 
    :param sort:         Whether to sort 
    :param format:       How to format the text, e.g. `my_function` or `"blah{}blah".format` 
    :param limit:        Limit to this many items.
    :param limit_symbol: Display further items with this symbol
    :param empty:        Returned for empty array
    :return:             String representation of the array 
    """
    if array is None:
        return empty
    
    if autorange:
        copy = list( array )
        array = []
        prefix_to_numbers = defaultdict( list )
        
        i = len( copy ) - 1
        
        while i >= 0:
            item = copy[i]
            item_str = format( item )
            elements = re.split( "([0-9]+)", item_str, 1 )
            
            if len( elements ) == 3:
                prefix_to_numbers[(elements[0], elements[2])].append( int( elements[1] ) )
            else:
                array.append( item_str )
            
            i -= 1
        
        for (prefix, suffix), numbers in prefix_to_numbers.items():
            for start, end in array_helper.get_ranges( numbers ):
                if start == end:
                    array.append( prefix + str( start ) + suffix )
                else:
                    array.append( prefix + str( start ) + "-" + str( end ) + suffix )
        
        format = str
    
    if sort:
        array = sorted( array, key = format )
    
    if final is None and limit == -1 and not empty:
        return join.join( format( x ) for x in array )
    else:
        if final is None:
            final = join
        
        r = []
        
        for index, (item, is_first, is_last) in enumerate( array_helper.when_first_or_last( array ) ):
            if index == limit:
                r.append( limit_symbol )
                break
            
            if not is_first:
                if is_last or index == limit - 1:
                    r.append( final )
                else:
                    r.append( join )
            
            r.append( format( item ) )
        
        if len( r ) == 0:
            return empty
        
        return "".join( r )


def dump_data( entity: object ):
    r = []
    ml = max( len( str( x ) ) for x in entity.__dict__ )
    
    for key, value in entity.__dict__.items():
        from mhelper import reflection_helper
        if reflection_helper.is_list_like( value ):
            value = format_array( value )
        
        r.append( str( key ).ljust( ml ) + " = " + str( value ) )
    
    return "\n".join( r )


def bracketed_split( text: str, split: str, start: str, end: str ) -> List[str]:
    inside = False
    r = []
    cur = []
    no_more = False
    no_br = False
    ebr = 0
    
    for c in text:
        if inside:
            if c in end:
                ebr -= 1
                
                if ebr >= 0:
                    cur.append( c )
                else:
                    inside = False
                    no_more = True
            elif c in start:
                ebr += 1
                cur.append( c )
            else:
                cur.append( c )
        else:
            if c in start and not no_br:
                inside = True
            elif c in split:
                no_br = False
                no_more = False
                ebr = 0
                r.append( "".join( cur ) )
                cur.clear()
            elif c.isspace():
                if no_more:
                    continue
                elif no_br:
                    cur.append( c )
            else:
                if no_more:
                    raise ValueError( "Malformed string: {}".format( repr( text ) ) )
                
                cur.append( c )
                no_br = True
    
    r.append( "".join( cur ) )
    
    return r
