# Copyright 2018 by Teradata Corporation. All rights reserved.

import ctypes
import datetime
import json
import os
import platform
import struct
import threading

apilevel = "2.0" # Required by DBAPI 2.0

threadsafety = 1 # Threads may share the module, but not connections # Required by DBAPI 2.0

paramstyle = "qmark" # Required by DBAPI 2.0

class Warning(Exception): # Required by DBAPI 2.0
    pass

class Error(Exception): # Required by DBAPI 2.0
    pass

class InterfaceError(Error): # Required by DBAPI 2.0
    pass

class DatabaseError(Error): # Required by DBAPI 2.0
    pass

class DataError(DatabaseError): # Required by DBAPI 2.0
    pass

class OperationalError(DatabaseError): # Required by DBAPI 2.0
    pass

class IntegrityError(DatabaseError): # Required by DBAPI 2.0
    pass

class InternalError(DatabaseError): # Required by DBAPI 2.0
    pass

class ProgrammingError(DatabaseError): # Required by DBAPI 2.0
    pass

class NotSupportedError(DatabaseError): # Required by DBAPI 2.0
    pass

osType = platform.system()
lockInit = threading.Lock()
bInitDone = False
goside = None

def prototype(rtype, func, *args):
    func.restype = rtype
    func.argtypes = args

class TeradataConnection:

    def __init__ (self, sConnectParams, **kwargs):

        if not sConnectParams:
            sConnectParams = '{}'

        if kwargs:
            dictParams = json.loads (sConnectParams)
            dictParams.update (kwargs) # parameters specified as kwargs have higher priority than parameters specified in JSON
            sConnectParams = json.dumps (dictParams)

        global bInitDone, goside # assigned-to variables are local unless marked as global

        try:
            lockInit.acquire()
            if not bInitDone:
                bInitDone = True

                if osType == "Windows":
                    sExtension = "dll"
                elif osType == "Darwin":
                    sExtension = "dylib"
                else:
                    sExtension = "so"

                sLibPathName = os.path.join(os.path.dirname(__file__), "teradatasql." + sExtension)
                goside = ctypes.cdll.LoadLibrary(sLibPathName)

                prototype(None, goside.goInitDriver              , ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                prototype(None, goside.goCreateConnectionPool    , ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.c_uint64))
                prototype(None, goside.goCloseConnectionPool     , ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                prototype(None, goside.goCreateRows              , ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.c_uint64))
                prototype(None, goside.goResultMetaData          , ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                prototype(None, goside.goFetchRow                , ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                prototype(None, goside.goNextResult              , ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.c_char))
                prototype(None, goside.goCloseRows               , ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
                prototype(None, goside.goFreePointer             , ctypes.POINTER(ctypes.c_char))

                pcError = ctypes.POINTER(ctypes.c_char)()
                goside.goInitDriver(sConnectParams.encode('utf-8'), ctypes.byref(pcError))
                if pcError:
                    sErr = ctypes.string_at(pcError).decode('utf-8')
                    goside.goFreePointer(pcError)
                    raise OperationalError(sErr)
        finally:
            lockInit.release()

        pcError = ctypes.POINTER(ctypes.c_char)()
        uPoolHandle = ctypes.c_uint64()
        goside.goCreateConnectionPool(sConnectParams.encode('utf-8'), ctypes.byref(pcError), ctypes.byref(uPoolHandle))
        if pcError:
            sErr = ctypes.string_at(pcError).decode('utf-8')
            goside.goFreePointer(pcError)
            raise OperationalError(sErr)

        self.uPoolHandle = uPoolHandle.value

        # end __init__

    def close(self): # Required by DBAPI 2.0

        pcError = ctypes.POINTER(ctypes.c_char)()
        goside.goCloseConnectionPool(self.uPoolHandle, ctypes.byref(pcError))
        if pcError:
            sErr = ctypes.string_at(pcError).decode('utf-8')
            goside.goFreePointer(pcError)
            raise OperationalError(sErr)

        # end close

    def commit(self): # Required by DBAPI 2.0
        pass

    def rollback(self): # Required by DBAPI 2.0
        pass

    def cursor(self): # Required by DBAPI 2.0
        return TeradataCursor(self)

    def __enter__(self): # Implements with-statement context manager
        return self

    def __exit__(self, t, value, traceback): # Implements with-statement context manager
        self.close()

    def __repr__(self): # Equivalent to the toString method in Java or the String method in Go
        return("{} uPoolHandle={}".format(self.__class__.__name__, self.uPoolHandle))

class DBAPITypeObject:

    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        return other in self.values

connect = TeradataConnection # Required by DBAPI 2.0

Date = datetime.date # Required by DBAPI 2.0

Time = datetime.time # Required by DBAPI 2.0

Timestamp = datetime.datetime # Required by DBAPI 2.0

DateFromTicks = datetime.date.fromtimestamp # Required by DBAPI 2.0

def TimeFromTicks(x): # Required by DBAPI 2.0
    return datetime.datetime.fromtimestamp(x).time()

TimestampFromTicks = datetime.datetime.fromtimestamp # Required by DBAPI 2.0

Binary = bytearray # Required by DBAPI 2.0

STRING = str # Required by DBAPI 2.0

BINARY = bytearray # Required by DBAPI 2.0

NUMBER = DBAPITypeObject(int, float) # Required by DBAPI 2.0

DATETIME = datetime.datetime # Required by DBAPI 2.0

ROWID = None # Required by DBAPI 2.0

def _deserializeBool (pc, i, row):

    if pc [i] == b'T' or pc [i] == b'F': # T=true F=false

        if row is not None:
            row.append (pc [i] == b'T')
        return i + 1

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type T/F/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeBool

def _serializeBytes (aby):

    return b'B' + struct.pack (">Q", len (aby)) + aby

def _deserializeBytes (pc, i, row):

    if pc [i] == b'B': # B=bytes
        i += 1

        uByteCount = struct.unpack (">Q", pc [i : i + 8]) [0] # uint64
        i += 8

        abyValue = pc [i : i + uByteCount]
        i += uByteCount

        if row is not None:
            row.append (abyValue)
        return i

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type B/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeBytes

def _serializeDouble (d):

    return b'D' + struct.pack (">d", d)

def _deserializeDouble (pc, i, row):

    if pc [i] == b'D': # D=double
        i += 1

        dValue = struct.unpack (">d", pc [i : i + 8]) [0] # float64
        i += 8

        if row is not None:
            row.append (dValue)
        return i

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type D/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeDouble

def _serializeInt (n):

    return b'I' + struct.pack (">i", n)

def _deserializeInt (pc, i, row):

    if pc [i] == b'I': # I=integer
        i += 1

        nValue = struct.unpack (">i", pc [i : i + 4]) [0] # int32
        i += 4

        if row is not None:
            row.append (nValue)
        return i

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type I/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeInt

def _serializeLong (n):

    return b'L' + struct.pack (">q", n)

def _deserializeLong (pc, i, row):

    if pc [i] == b'L': # L=long
        i += 1

        nValue = struct.unpack (">q", pc [i : i + 8]) [0] # int64
        i += 8

        if row is not None:
            row.append (nValue)
        return i

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type L/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeLong

def _serializeNull ():

    return b'N'

def _deserializeNull (pc, i, row):

    if pc [i] == b'N': # N=null

        if row is not None:
            row.append (None)
        return i + 1

    else:
        raise OperationalError ('Expected column type N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeNull

def _serializeString (s):

    aby = s.encode ('utf-8')
    return b'S' + struct.pack (">Q", len (aby)) + aby

def _deserializeString (pc, i, row):

    if pc [i] == b'S': # S=string
        i += 1

        uByteCount = struct.unpack (">Q", pc[i : i + 8]) [0] # uint64
        i += 8

        sValue = pc [i : i + uByteCount].decode ('utf-8')
        i += uByteCount

        if row is not None:
            row.append (sValue)
        return i

    elif pc [i] == b'N': # N=null
        return _deserializeNull (pc, i, row)

    else:
        raise OperationalError ('Expected column type S/N but got {} at byte offset {}'.format (pc [i], i))

    # end _deserializeString

class TeradataCursor:

    def __init__(self, con):

        self.description = None # Required by DBAPI 2.0
        self.rowcount = -1 # Required by DBAPI 2.0
        self.arraysize = 1 # Required by DBAPI 2.0
        self.rownumber = None # Optional by DBAPI 2.0
        self.connection = con # Optional by DBAPI 2.0
        self.uRowsHandle = None

        # end __init__

    def callproc(self, sProcName, params=None): # Required by DBAPI 2.0

        sCall = "CALL {} (".format(sProcName)

        for i in range(0, len(params)):
            if i > 0:
                sCall += ", "
            sCall += "?"

        sCall += ")"

        self.execute(sCall, params)

        # end callproc

    def close(self): # Required by DBAPI 2.0

        if self.uRowsHandle:
            pcError = ctypes.POINTER(ctypes.c_char)()
            goside.goCloseRows(self.uRowsHandle, ctypes.byref(pcError))

            self.uRowsHandle = None

            if pcError:
                sErr = ctypes.string_at(pcError).decode('utf-8')
                goside.goFreePointer(pcError)
                raise OperationalError(sErr)

        # end close

    def execute (self, sOperation, params = None): # Required by DBAPI 2.0

        if params and type (params) not in [list, tuple]:
            raise TypeError ("params unexpected type {}".format (type (params)))

        if not params:
            self.executemany (sOperation, None)

        elif type (params [0]) in [list, tuple]:
            # Excerpt from PEP 249 DBAPI documentation:
            #  The parameters may also be specified as list of tuples to e.g. insert multiple rows in a single
            #  operation, but this kind of usage is deprecated: .executemany() should be used instead.
            self.executemany (sOperation, params)

        else:
            self.executemany (sOperation, [params, ])

        return self

        # end execute

    def _obtainResultMetaData (self):

        pcError = ctypes.POINTER (ctypes.c_char) ()
        pcColumnMetaData = ctypes.POINTER (ctypes.c_char) ()
        goside.goResultMetaData (self.uRowsHandle, ctypes.byref (pcError), ctypes.byref (pcColumnMetaData))

        if pcError:
            sErr = ctypes.string_at (pcError).decode ('utf-8')
            goside.goFreePointer (pcError)
            raise OperationalError (sErr)

        if pcColumnMetaData:
            self.description = []
            i = 0
            while pcColumnMetaData [i] != b'Z': # Z=terminator
                columnDesc = []

                # (1) Column name
                i = _deserializeString (pcColumnMetaData, i, columnDesc)

                i = _deserializeString (pcColumnMetaData, i, None) # discard Type name

                # (2) Type code
                i = _deserializeString (pcColumnMetaData, i, columnDesc)
                if columnDesc [-1] == 'b': # typeCode b=binary
                    columnDesc [-1] = BINARY
                elif columnDesc [-1] == 'd': # typeCode d=double
                    columnDesc [-1] = float
                elif columnDesc [-1] == 'i': # typeCode i=int (int32)
                    columnDesc [-1] = int
                elif columnDesc [-1] == 'l': # typeCode l=long (int64)
                    columnDesc [-1] = int
                elif columnDesc [-1] == 's': # typeCode s=string
                    columnDesc [-1] = STRING

                # (3) Display size
                columnDesc.append (None) # not provided

                # (4) Max byte count
                i = _deserializeLong (pcColumnMetaData, i, columnDesc)

                # (5) Precision
                i = _deserializeLong (pcColumnMetaData, i, columnDesc)

                # (6) Scale
                i = _deserializeLong (pcColumnMetaData, i, columnDesc)

                # (7) Nullable
                i = _deserializeBool (pcColumnMetaData, i, columnDesc)

                self.description.append (columnDesc)

                # end while

            goside.goFreePointer (pcColumnMetaData)

            # end if pcColumnMetaData

        # end _obtainResultMetaData

    def executemany (self, sOperation, seqOfParams): # Required by DBAPI 2.0

        if self.uRowsHandle:
            self.close ()

        abyBindValues = b''

        if seqOfParams:

            if type (seqOfParams) not in [list, tuple]:
                raise TypeError ("seqOfParams unexpected type {}".format (type (seqOfParams)))

            for i in range (0, len (seqOfParams)):

                if type (seqOfParams [i]) not in [list, tuple]:
                    raise TypeError ("seqOfParams[{}] unexpected type {}".format (i, type (seqOfParams [i])))

                if len (seqOfParams [i]) == 0:
                    raise ValueError ("seqOfParams[{}] is zero length".format (i))

                for j in range (0, len (seqOfParams [i])):
                    if seqOfParams [i][j] is None:
                        abyBindValues += _serializeNull ()
                    elif isinstance (seqOfParams [i][j], bytes):
                        abyBindValues += _serializeBytes (seqOfParams [i][j])
                    elif isinstance (seqOfParams [i][j], int):
                        abyBindValues += _serializeLong (seqOfParams [i][j])
                    elif isinstance (seqOfParams [i][j], float):
                        abyBindValues += _serializeDouble (seqOfParams [i][j])
                    elif isinstance (seqOfParams [i][j], str):
                        abyBindValues += _serializeString (seqOfParams [i][j])
                    else:
                        raise TypeError ("seqOfParams[{}][{}] unexpected type {}".format (i, j, type (seqOfParams [i][j])))
                    # end for j

                abyBindValues += b'Z' # end of row terminator

                # end for i
            # end if seqOfParams

        abyBindValues += b'Z' # end of all rows terminator

        pcError = ctypes.POINTER (ctypes.c_char) ()
        uRowsHandle = ctypes.c_uint64 ()
        goside.goCreateRows (self.connection.uPoolHandle, sOperation.encode ('utf-8'), len (abyBindValues), abyBindValues, ctypes.byref (pcError), ctypes.byref (uRowsHandle))
        if pcError:
            sErr = ctypes.string_at (pcError).decode ('utf-8')
            goside.goFreePointer (pcError)
            raise OperationalError (sErr)

        self.uRowsHandle = uRowsHandle.value

        self._obtainResultMetaData ()

        # end executemany

    def fetchone(self): # Required by DBAPI 2.0

        try:
            return next(self)

        except StopIteration:
            return None

        # end fetchone

    def fetchmany(self, nDesiredRowCount=None): # Required by DBAPI 2.0

        if nDesiredRowCount is None:
            nDesiredRowCount = self.arraysize

        rows = []
        nObservedRowCount = 0
        for row in self:
            rows.append(row)
            nObservedRowCount += 1
            if nObservedRowCount == nDesiredRowCount:
                break

        return rows

        # end fetchmany

    def fetchall(self): # Required by DBAPI 2.0

        rows = []
        for row in self:
            rows.append(row)

        return rows

        # end fetchall

    def nextset(self): # Optional by DBAPI 2.0

        if self.uRowsHandle:

            pcError = ctypes.POINTER(ctypes.c_char)()
            cAvail = ctypes.c_char()

            goside.goNextResult(self.uRowsHandle, ctypes.byref(pcError), ctypes.byref(cAvail))

            if pcError:
                sErr = ctypes.string_at(pcError).decode('utf-8')
                goside.goFreePointer(pcError)
                raise OperationalError(sErr)

            if cAvail.value == b'Y':
                self._obtainResultMetaData ()
            else:
                self.description = None

            return cAvail.value == b'Y'

        # end nextset

    def setinputsizes(self, sizes): # Required by DBAPI 2.0
        pass

    def setoutputsize(self, size, column=None): # Required by DBAPI 2.0
        pass

    def __iter__(self): # Implements iterable # Optional by DBAPI 2.0
        return self

    def __next__(self): # Implements Python 3 iterator

        if self.uRowsHandle:

            pcError = ctypes.POINTER(ctypes.c_char)()
            pcColumnValues = ctypes.POINTER(ctypes.c_char)()

            goside.goFetchRow(self.uRowsHandle, ctypes.byref(pcError), ctypes.byref(pcColumnValues))

            if pcError:
                sErr = ctypes.string_at (pcError).decode ('utf-8')
                goside.goFreePointer (pcError)
                raise OperationalError (sErr)

            if pcColumnValues:
                row = []
                i = 0
                while pcColumnValues [i] != b'Z': # Z=terminator

                    if pcColumnValues [i] == b'N': # N=null
                        i = _deserializeNull (pcColumnValues, i, row)

                    elif pcColumnValues [i] == b'B': # B=bytes
                        i = _deserializeBytes (pcColumnValues, i, row)

                    elif pcColumnValues [i] == b'D': # D=double
                        i = _deserializeDouble (pcColumnValues, i, row)

                    elif pcColumnValues [i] == b'I': # I=integer
                        i = _deserializeInt (pcColumnValues, i, row)

                    elif pcColumnValues [i] == b'L': # L=long
                        i = _deserializeLong (pcColumnValues, i, row)

                    elif pcColumnValues [i] == b'S': # S=string
                        i = _deserializeString (pcColumnValues, i, row)

                    else:
                        raise OperationalError ('Unrecognized column type {} at byte offset {}'.format (pcColumnValues [i], i))

                    # end while

                goside.goFreePointer (pcColumnValues)

                return row

                # end if pcColumnValues

            # end if self.uRowsHandle

        raise StopIteration ()

        # end __next__

    def next(self): # Implements Python 2 iterator # Optional by DBAPI 2.0
        return self.__next__()

    def __enter__(self): # Implements with-statement context manager
        return self

    def __exit__(self, t, value, traceback): # Implements with-statement context manager
        self.close()

    def __repr__(self): # Equivalent to the toString method in Java or the String method in Go
        return("{} uRowsHandle={}".format(self.__class__.__name__, self.uRowsHandle))
