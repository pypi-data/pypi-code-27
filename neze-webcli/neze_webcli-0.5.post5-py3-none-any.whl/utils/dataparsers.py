try:
    from yaml.cyaml import CSafeLoader as yLoader, CSafeDumper as yDumper
except ImportError:
    from yaml import SafeLoader as yLoader, SafeDumper as yDumper
from yaml import load as _yload,dump as _ydump

__all__=['yload','ydump']

def yload(stream,Loader=None):
    return _yload(stream,Loader=yLoader)

def ydump(data,stream=None,Dumper=None,**kwds):
    return _ydump(data,stream=stream,Dumper=yDumper,**kwds)
