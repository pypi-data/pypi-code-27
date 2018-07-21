"""
This module provides a built-in help() function support for Python ctypes bindings.

Copyright (C) 2018 by Dalen Bernaca
                      dbernaca@gmail.com

help_support enables you to use help() on modules containing functions from
ctypes linked libraries.
It uses pydoc and it is based on it and tries to emulate the original help() function as much as possible,
but I took some liberties to change the output a little.
Submodules are not shown and the order of presentation is slightly different.

Features it shows (in presented order) are:
    NAME
    FILE
    [MODULE DOCS]
    [DESCRIPTION]
    [CTYPES FUNCTIONS]
    [CTYPES STRUCTURES]
    [PYTHON FUNCTIONS]
    [PYTHON CLASSES]
    [DATA]
    [VERSION]
    [DATE]
    [AUTHOR]
    [CREDITS]

How does it work?

It substitutes __builtin__.help() with a new
_Helper() object that will always call original help() except in cases where
presented object is a module containing ctypes._CFuncPtr i.e. the ctypes function(s) and/or ctypes structure(s)
or the object is one of the listed itself.
All variables containing some other ctypes types are recognized as DATA.

In order for the module to show the output that makes sense your ctypes functions should have
the "__doc__" attribute added with the __doc__ string and properly configured attributes "argtypes" and "restype".

An extra, help_support specific, "argnames" attribute can be added to your ctypes function to improve the representation of the function's arguments.
It is a list containing strings with names of each argument in a row.
If "argnames" is properly specified then help() will show a defined name along with the argument's type.

* Note that defining "argnames" will not have inpact on the function itself.
  It is only used by help_support to make the help() more descriptive and remind
  developers what goes where when the function is called.

Structures can also have a "__doc__" string and they should have the "_fields"_ attribute.

When you are making a ctypes Python bindings, just include the
help_support in your package and keep good documentation
of each function pulled from the DLL/DYLIB/SO and declared structures.

Example:
    # examp_module:
    import ctypes
    import ctypes.util

    import help_support
    del help_support # If you want you can remove it now
                     # to avoid cluttering your globals() namespace.
                     # Once it is called you do not usually need it any more.

    l = ctypes.CDLL(ctypes.util.find_library("c"))

    # Pull the time() function from libc,
    # declare and document it:
    time = l.time
    time.argtypes = []
    #time.argnames = ["c_void"] # The function takes no arguments, but you can trick help_support 
                                # to show something in parenthesis if you want to be consistent with C
                                # If there is/are argument(s) you should put its/their name(s) in "argnames".
    time.restype = ctypes.c_int
    time.__doc__ = "Function that returns a system time in seconds."
    -------------------------------------------
    >>> # Usage:
    >>> import examp_module
    >>> help(examp_module)
    >>> help(examp_module.time)
    >>>

The usage is simple.
Just pack it into your ctypes bindings and import it in every module containing ctypes functions and/or structures.
Users of your package will hardly notice that help() was changed a little and they will be glad it did anyway
because they will be able to use it on your bindings and thus
speed up their development.

The module is not very extensively tested and still may have bugs in getting the documentation,
presenting a proper ctypes type names and help's formatting in general.

The module was tested for Python 2.5, 2.6 and 2.7 on the following platforms:
Ubuntu 16.04, Windows XP and Cygwin.

The author does not guarantee you anything.
He just hopes the module will be useful and that it will work on your modules as intended.
Feel free to modify and improve it as you need, but please notify the author about improvements you made that can be useful to others.
The module is free for any use under GNU GPL.

ToDo:
- Support documenting ctypes functions that
  are pulled into a class (stored as attributes)
  when showing a help() of a module.
"""

import site
import inspect
import pydoc
import __builtin__
import ctypes
import sys

__author__  = "Dalen Bernaca"
__version__ = "0.2"

__all__ = []

def indent(text, prefix=' |  '):
    """
    Indent text by prepending a given prefix to each line.
    Modified version of pydoc.text.indent().
    """
    if not text: return ''
    lines = text.lstrip("\r\n").expandtabs(4).splitlines()
    scoot(lines)
    lines = map(lambda line, prefix=prefix: prefix + line.rstrip(), lines)
    while lines and lines[-1]=="":
        del lines[-1]
    return "\n".join(lines)

def scoot (lines):
    """Removes the minimal indentation from lines list()."""
    # Find the minimal indentation:
    indents = []
    for line in lines:
        line = line.rstrip()
        if not line: continue
        ws = len(line)-len(line.lstrip())
        indents.append(ws)
    sc = min(indents)
    if not sc: return
    # Pull back each line for sc characters:
    for x in xrange(len(lines)):
        lines[x] = lines[x][sc:]

def isinctypes (obj, name):
    """
    Returns whether the ctypes has the attribute from obj given by the name argument
    and that its value comes from ctypes.
    Returns True if ctypes has a variable with the same name,
    and the memory address of the variable in the object and
    the one in ctypes match.
    Otherwise False is returned.
    The test can be improved but it is considered good enough for now.
    It is used to determine whether an item was imported from ctypes or not.
    Because there is no sense in documenting them
    They are just a part of stdlib for creating the bindings.
    """
    # Renamed things will be overlooked
    a = None; b = None
    return id(getattr(ctypes, name, a))==id(getattr(obj, name, b))

def getall (obj):
    """Returns or constructs the iterator over modules __all__ attribute.
    If there is None, it is constructed using rules:
    Every name that doesn't start with "_" and it doesn't belong to ctypes module.
    """
    try: all = iter(obj.__all__)
    except:
        all = (y for y in dir(obj) if not y.startswith("_") and not isinctypes(obj, y))
    return all

def iscfunc (obj):
    """
    Returns True if the obj is the ctypes function, False otherwise.
    """
    return isinstance(obj, ctypes._CFuncPtr)

def iscstruct (obj):
    """
    Returns True if the obj is the ctypes structure, False otherwise.
    """
    return type(obj)==type(ctypes.Structure)

def hasctypes (obj):
    """
    Search a module or a class for a ctypes function or structure.
    True if any is present, False otherwise.
    """
    isctypes = lambda o: iscfunc(o) or iscstruct(o)
    return any(isctypes(getattr(obj, x)) for x in getall(obj) if hasattr(obj, x))

def iscmodule (obj):
    """
    Returns True if obj is a module containing
    ctypes function(s) and/or structure(s).
    """
    return inspect.ismodule(obj) and hasctypes(obj)

def ctype (t):
    """
    Returns a name of the ctypes C type.
    It can be improved I think, but let declare it good enough for now.
    """
    try: return t.__name__
    except:
        try: return t.__class__.__name__
        except: pass
    return pydoc.stripid(str(t)).lstrip("<").rstrip(">")

def visiblename(name, all=None, obj=None):
    """
    Decide whether to show documentation on a variable.
    Copied from a pydoc of Python 2.7 to improve backward compatibility.
    """
    # Certain special names are redundant.
    _hidden_names = ('__builtins__', '__doc__', '__file__', '__path__',
                     '__module__', '__name__', '__slots__', '__package__')
    if name in _hidden_names: return 0
    # Private names are hidden, but special names are displayed.
    if name.startswith('__') and name.endswith('__'): return 1
    # Namedtuples have public fields and methods with a single leading underscore
    if name.startswith('_') and hasattr(obj, '_fields'):
        return 1
    if all is not None:
        # only document that which the programmer exported in __all__
        return name in all
    else:
        return not name.startswith('_')

def getmodule (obj):
    """
    Finds a module the obj came from.
    Solving the problem of inspect.getmodule()
    where ctypes is returned for each ctypes._CFuncPtr().
    """
    # Unfortunately ctypes._CFuncPtr().__module__ is always "ctypes"
    # which is essentially correct, but we need our module, not ctypes
    # Fortunately, inheriting ctypes.Structure makes our structures
    # properly placed
    if obj.__module__ and obj.__module__!="ctypes":
        return sys.modules[obj.__module__]
    # Be very KISSy
    elif obj.__module__ and obj.__module__=="ctypes":
        addr = id(obj)
        # Try first the package that includes help_support
        try:
            mod = sys.modules[__package__]
            for x in getall(mod):
                if id(getattr(mod, x, None))==addr:
                    return mod
        except: pass
        # It returns a first module it finds that contains the obj
        for mn, mod in sys.modules.iteritems():
            if mn==__name__ or mn=="ctypes" or mn.startswith("__"): continue
            if not iscmodule(mod): continue
            for x in getall(mod):
                if id(getattr(mod, x, None))==addr:
                    return mod
        return inspect.getmodule(obj)

def getaliases (obj):
    """
    Finds out all aliases of the obj.
    In your bindings, you might want to call the DLL's function
    something other than original.
    They usually have a prefix that you might want to exclude.
    But ctypes._CFuncPtr().__name__ returns the name of the original function (as in DLL).
    So this is a way of finding out how you named it elsewhere.
    The problem can probably be solved in some other way,
    but use inspection of its module for now.
    """
    a = []
    addr = id(obj)
    mod = getmodule(obj)
    for x in getall(mod):
        if id(getattr(mod, x, None))==addr:
            a.append(x)
    if not a: a.append(obj.__name__) # Hope not to happen
    return a

# Preserve the original help() function to use later:
_help = __builtin__.help

class _Helper (site._Helper):
    def __call__ (self, *args, **kwargs):
        if args and isinstance(args[0], basestring):
            o = pydoc.locate(args[0])
            if o: args = list(args); args[0] = o
            else: return _help(*args, **kwargs)
        if args and iscfunc(args[0]):
            return pydoc.pager(self.docctypes(args[0]))
        if args and iscstruct(args[0]):
            return pydoc.pager(self.doccstruct(args[0]))
        if args and iscmodule(args[0]):
            return pydoc.pager(self.doccmodule(args[0]))
        return _help(*args, **kwargs)

    def docctypes (self, obj, title=1, name=None):
        fn   = name if name else getaliases(obj)[0]
        doc  = ""
        if title:
            doc += "Help on ctypes function %s():\n\n" % fn
        if hasattr(obj, "restype"):
            doc += ctype(obj.restype)+" " if obj.restype!=None else ""
        doc += fn+"(%s)\n" % self.docargs(obj)
        if hasattr(obj, "__doc__"):
            doc += indent(obj.__doc__)
        return doc.rstrip()

    def doccmodule (self, obj):
        doc = "Help on "
        if hasattr(obj, "__module__"):
            doc += "module %s:\n\n" % obj.__module__
        elif hasattr(obj, "__package__") and "." in obj.__name__:
            doc += "module %s in %s:\n\n" % (obj.__name__, obj.__package__)
        elif hasattr(obj, "__package__") and obj.__package__:
            doc += "package %s:\n\n" % obj.__package__
        else:
            # Perform backward compatible check for older Python versions:
            import os.path
            if obj.__file__:
                if os.path.basename(obj.__file__).startswith("__init__."):
                    doc += "package %s:\n\n" % obj.__name__
                else: doc += "module %s:\n\n" % obj.__name__
            else: doc += "module %s:\n\n" % obj.__name__
        synopsis, docstr = pydoc.splitdoc(pydoc.getdoc(obj))
        try: file = inspect.getabsfile(obj)
        except: file = "(built-in)"
        doc += "NAME\n    %s\n\nFILE\n    %s\n\n" % (
            (obj.__name__+" - "+synopsis if synopsis else obj.__name__),
            file)
        docloc = pydoc.text.getdocloc(obj)
        if docloc is not None:
            doc += "MODULE DOCS\n    %s\n\n" % docloc
        if docstr:
            doc += "DESCRIPTION\n%s\n\n" % indent(docstr, "    ")
        all = list(getall(obj))
        cfuncs = sorted(x for x in all if iscfunc(getattr(obj, x)))
        if cfuncs:
            doc += "CTYPES FUNCTIONS\n"
            doc += indent("\n\n".join(self.docctypes(getattr(obj, x), 0, x) for x in cfuncs), "    ")
            doc += "\n\n"
        # Modified from pydoc.text.docmodule():
        classes = []
        structures = []
        for key, value in inspect.getmembers(obj, inspect.isclass):
            if visiblename(key, all, obj):
                if iscstruct(value):
                    structures.append((key, value))
                else:
                    classes.append((key, value))
        funcs = []
        for key, value in inspect.getmembers(obj, inspect.isroutine):
            if visiblename(key, all, obj):
                funcs.append((key, value))
        data = []
        for key, value in inspect.getmembers(obj, pydoc.isdata):
            if visiblename(key, all, obj):
                if key not in cfuncs and key not in structures:
                    data.append((key, value))
        if structures:
            contents = []
            for key, value in structures:
                contents.append(self.doccstruct(value, 0, key))
            doc += "CTYPES STRUCTURES\n%s\n\n" % indent("\n\n".join(contents), "    ")
        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(pydoc.text.document(value, key, obj.__name__))
            doc += "PYTHON FUNCTIONS\n%s\n\n" % indent("\n".join(contents), "    ")
        if classes:
            classlist = map(lambda key_value: key_value[1], classes)
            contents = [pydoc.text.formattree(
                inspect.getclasstree(classlist, 1), obj.__name__)]
            for key, value in classes:
                contents.append(pydoc.text.document(value, key, obj.__name__))
            doc += "PYTHON CLASSES\n%s\n\n" % indent("\n".join(contents), "    ")
        if data:
            contents = []
            for key, value in data:
                contents.append(pydoc.text.docother(value, key, obj.__name__, maxlen=70))
            doc += "DATA\n%s\n\n" % indent("\n".join(contents), "    ")
        if hasattr(obj, '__version__'):
            version = str(obj.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            doc += "VERSION\n    %s\n\n" % version
        if hasattr(obj, '__date__'):
            doc += "DATE\n    %s\n\n" % obj.__date__
        if hasattr(obj, '__author__'):
            doc += "AUTHOR\n    %s\n\n" % str(obj.__author__)
        if hasattr(obj, '__credits__'):
            doc += "CREDITS\n    %s\n\n" % str(obj.__credits__)
        return doc.rstrip()

    def doccstruct (self, obj, title=1, name=None):
        if not name:
            try: name = "%s.%s" % (obj.__module__, obj.__name__)
            except: name = obj.__name__
            sn = obj.__name__
        else: sn = name.rsplit(".", 1)[-1]
        if title:
            s = "Help on ctypes structure %s:\n\n" % name
        else:
            s = "structure %s\n" % name
        if hasattr(obj, "__doc__") and obj.__doc__:
            s += indent(obj.__doc__, "    ")+"\n\n"
        if hasattr(obj, "_fields_"):
            if title:
                s += "FIELDS\n"+"\n".join("    "+sn+"."+f+" = "+ctype(t) for f, t in obj._fields_)
            else:
                s += "    FIELDS\n"+"\n".join("     |  "+sn+"."+f+" = "+ctype(t) for f, t in obj._fields_)
        return s

    def docargs (self, obj):
        if iscfunc(obj):
            atypes = map(ctype, (getattr(obj, "argtypes", []) or []))
            anames = getattr(obj, "argnames", []) or []
            a = zip(atypes, anames)
            if len(atypes)<len(anames):
                a += [("", x) for x in anames[len(a):]]
            if len(atypes)>len(anames):
                a += [(x, "") for x in atypes[len(a):]]
            return ", ".join(" ".join(x).strip(" ") for x in a)
        # Accept Python functions too:
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            argspec = inspect.getargspec(obj)
            argspec = inspect.formatargspec(*argspec)
            return argspec[1:-1] # remove parentheses
        raise TypeError, "%s is not a function" % str(obj)

# Swap the original help() function:
__builtin__.help = _Helper()
