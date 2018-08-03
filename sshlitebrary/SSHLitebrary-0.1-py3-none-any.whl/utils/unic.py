from pprint import PrettyPrinter
from .robottypes import is_bytes, is_unicode


def unic(item):
    if isinstance(item, str):
        return item
    if isinstance(item, (bytes, bytearray)):
        try:
            return item.decode('ASCII')
        except UnicodeError:
            return ''.join(chr(b) if b < 128 else '\\x%x' % b
                            for b in item)
    try:
        return str(item)
    except:
        return _unrepresentable_object(item)


from unicodedata import normalize
_unic = unic

def unic(item):
    return normalize('NFC', _unic(item))


def prepr(item, width=400):
    return unic(PrettyRepr(width=width).pformat(item))


class PrettyRepr(PrettyPrinter):

    def format(self, object, context, maxlevels, level):
        try:
            if is_unicode(object):
                return repr(object).lstrip('u'), True, False
            if is_bytes(object):
                return 'b' + repr(object).lstrip('b'), True, False
            return PrettyPrinter.format(self, object, context, maxlevels, level)
        except:
            return _unrepresentable_object(object), True, False


def _unrepresentable_object(item):
    from .error import get_error_message
    return u"<Unrepresentable object %s. Error: %s>" \
           % (item.__class__.__name__, get_error_message())
