"""Left pad a string.

>>> left_pad("foo", 5)
'  foo'

>>> left_pad("foobar", 6)
'foobar'

>>> left_pad(1, 2, '0')
'01'

>>> left_pad(17, 5, 0)
'00017'
"""

def left_pad(string, length, character=" "):
    """Left pad a `string` to `length` characters with `character`."""
    if not isinstance(string, str):
        string = str(string)
    if not isinstance(character, str):
        character = str(character)
    return string.rjust(length, character)
