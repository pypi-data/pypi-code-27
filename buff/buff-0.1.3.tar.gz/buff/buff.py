#!/usr/bin/env python
import struct
from collections import namedtuple
Datatype = namedtuple('Datatype', 'size typ')

# bitsize, typ
# typ is one of 'u', 's', 'f', 'S', 'P'
# u is unsigned
# s is signed
# f is float
# S is string
# P is pascal string

BIT = Datatype(1, 'u')
FLAG = Datatype(1, 'u')
NIBBLE = Datatype(4, 'u')
BYTE = Datatype(8, 'u')
SBYTE = Datatype(8, 's')
UBYTE = Datatype(8, 'u')
CHAR = Datatype(8, 'c')
WORD = Datatype(16, 'u')
SWORD = Datatype(16, 's')
UWORD = Datatype(16, 'u')
HALF = Datatype(16, 's')
UHALF = Datatype(16, 'u')
SHALF = Datatype(16, 's')
SHORT = Datatype(16, 's')
USHORT = Datatype(16, 'u')
SSHORT = Datatype(16, 's')
DWORD = Datatype(32, 'u')
UDWORD = Datatype(32, 'u')
SDWORD = Datatype(32, 's')
INT = Datatype(32, 's')
UINT = Datatype(32, 'u')
FLOAT = Datatype(32, 'f')
LONG = Datatype(32, 's')
ULONG = Datatype(32, 'u')
DOUBLE = Datatype(64, 'f')
QUAD = Datatype(64, 'u')
UQUAD = Datatype(64, 'u')
SQUAD = Datatype(64, 's')
LONGLONG = Datatype(64, 's')
SLONGLONG = Datatype(64, 's')
ULONGLONG = Datatype(64, 'u')
STRING = Datatype('v', 'S')
PSTRING = Datatype('v', 'P')

class Buffer(object):
    pass

class Union(object):

    def __init__(self, *args):
        ''' Create a Union type and add values to it, or initialize.
        A union is an ordered container of (name, datatype, mult).
        name is the identifier of the value. bitsize is its size in bits,
        and datatype is one of the types declared in buff.
        mult is how many.
        '''
        if args:
            self.set(*args)

    def set(self, *args):
        self._union = args
    
    def add(self, name, datatype=None, mult=1, bitsize=None, typ=None):
        ''' Add a data type to the union '''
        if datatype is not None:
            return self.add(
                name, 
                bitsize=bitsize or datatype.size,
                typ=typ or datatype.typ, 
                mult=mult
            )
            self._union += [(name, Datatype(bitsize, typ), mult)]
    
    def unpack_odd(self, packed, datatype, order='<'):
        if datatype.typ not in ('s', 'u'):
            raise ValueError('cant work with odd sized string')
        if datatype.size > 64:
            raise ValueError('cant work with values larger than 64')
        m = 8 - (datatype.size % 8)
        packed_fixed = ''
        for c in packed:
            packed_fixed += chr(ord(c) << m)
        packed_fixed = packed_fixed + ('\x00' * (8 - len(packed_fixed)))
        value = struct.unpack(order + 'Q', packed_fixed)[0]
        i = datatype.size - 1
        total = 0
        if datatype.typ == 's':
            signed = bool(value & 2**i)
            i -= 1
        else:
            signed = False
        while i >= 0:
            if bool(value & 2**i):
                total += 2**i 
            i -= 1
        if signed:
            return -1 * total
        else:
            return total

    def unpack_value(self, packed, datatype, order='<'):
        if datatyp.typ == 'S':
            return packed[:datatype.size / 8]
        elif datatyp.typ == 'P':
            return packed[1:ord(packed[0])]
        if datatype.size == 1:
            return packed & 1
        elif datatype.size in (4, 8):
            if datatype.typ == 's':
                fmt = 'b'
            elif datatyp.typ == 'u':
                fmt = 'B'
            elif datatype.typ == 'c':
                fmt = 'c'
            else:
                raise ValueError('unknown type for size (%s, %s)'
                    % datatype)
            return struct.unpack(order + fmt, packed[0])[0]
        elif datatype.size == 16:
            if datatype.typ == 's':
                fmt = 'h'
            elif datatype.typ == 'u':
                fmt = 'H'
            else:
                raise ValueError('unknown type for size (%s, %s)'
                    % datatype)
            return struct.unpack(order + fmt, packed[:2])[0]
        elif datatype.size == 32:
            if datatype.typ == 's':
                fmt = 'i'
            elif datatype.typ == 'u':
                fmt = 'I'
            elif datatype.typ == 'f':
                fmt = 'f'
            else:
                raise ValueError('unknown type for size (%s, %s)'
                    % datatype)
            return struct.unpack(order + fmt, packed[:4])[0]
        elif datatype.size == 64:
            if datatype.typ == 's':
                fmt = 'q'
            elif datatype.typ == 'u':
                fmt = 'Q'
            elif datatype.typ == 'f':
                fmt = 'd'
            else:
                raise ValueError('unknown type for size (%s, %s)'
                    % datatype)
            return struct.unpack(order + fmt, packed[:8])[0]
        elif datatype.size < 1:
            raise ValueError('unknown type for size (%s, %s)' % datatype)
        return self.unpack_value_odd(packed, datatype, order)

    def unpack(self, packed, order='<'):
        buff = Buffer()
        for name, datatype, mult in self._union:
            if mult > 1:
                vals = []
        return buf
