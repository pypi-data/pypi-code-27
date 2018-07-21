#!/usr/bin/env python

"""
Library of common APIs for Python Applications.

PyLib is a set of common APIs and Classes that are used by many of
my personal Python applications and packages. In this initial version of
the library, I've stripped it down to just those things that I have functional
unittests for. As I have time to add additional tests and documentation, I
will add more functionality back in.

I recommend importing this package using the syntax:

.. code::

    import kenl380.pylib as pylib

So that you only need to use the ``pylib`` part of the namespace, e.g.:

.. code::

    pylib.USER
    pylib.context(__file__)

"""

__all__ = ['context', 'ntpx', 'parent', 'popd', 'pushd', 'TEMPDIR', 'USER', 'COMPUTER']

TEMPDIR = '/temp'       #: This points to a writable location for temporary files
USER = ''               #: This is the name of the currently logged-in user.
COMPUTER = ''           #: This is the host name where your app is running.


class context(object):
    """
    Provides context to a Python module.

    The context object provides methods to give useful context to a Python
    module. Things like current location, fully qualified script name, an
    alias and more.

    when you instantiate one of these, you pass in __file__ if defined,
    otherwise sys.argv[0].

    Parameters
    ----------
        module : str
            the fully qualified path for this module
        alias : str, optional
            the preferred alias for this module, defaults to basename
            of the ``module`` variable.

    Examples
    --------
    For example, add the following code to your main module.

    .. code::

        import kenl380.pylib as pylib

        def context():
            try:
                myself = __file__
            except NameError:
                myself = argv[0]

            return pylib.context(myself)

        me = context()

    Now, the ``me`` object can be used to extract useful information
    about the module, such as: ``me.whereami()`` to get the fully
    qualified pathname of your script.
    """

    def __init__(self, module, alias=None):
        from os.path import abspath, split, splitext

        self._whoami = abspath(module)
        self._whereami,whocares = split(self._whoami)
        
        name,ext = splitext(whocares)

        if alias is None:
            self._alias = name
        else:
            self._alias = alias

    def whoami(self):
        """Get the fully qualified name of the current module.

        Returns
        -------
        str
            Fully qualified name of the current module
        """
        return self._whoami

    def alias(self):
        """Returns the alias (shortname) of the current module

        By default, the alias is simply the basename (module name without
        extension) of the module; however, you can override that by passing
        in a specific value for the alias when you construct the object.

        Returns
        -------
        str
            The alias for the current module
        """
        return self._alias

    def whereami(self):
        """Returns the fully qualified path where the current module is stored

        Returns
        -------
        str
            Fully qualified path to the current module
        """
        return self._whereami

    def pyVersionStr(self):
        """Version of Python running my script

        Returns
        -------
        str
            A descriptive string containing the version of Python running
            this script.
        """
        from sys import version_info

        return "Python Interpreter Version: {}.{}.{}".format(version_info.major,
                                                             version_info.minor,
                                                             version_info.micro)

try:
    __me = context(__file__)
except:
    from sys import argv
    __me = context(argv[0])
    
def _init():
    from os import name, environ
    from os.path import normcase

    global USER, COMPUTER, TEMPDIR

    if name == 'nt':
        ENVUSERNAME = 'USERNAME'
        ENVTMPDIR = 'TEMP'
    else:   # assume name == 'posix'
        this_var = None
        for env_var in ['LOGNAME', 'USER']:
            if env_var in environ:
                this_var = env_var
                break

        ENVUSERNAME = 'LOGNAME' if not this_var else this_var
        ENVTMPDIR = 'TMPDIR'

    if ( ENVUSERNAME in environ):
        USER = environ[ENVUSERNAME]

    from platform import node
    
    COMPUTER = node()

    if (ENVTMPDIR in environ):
        TEMPDIR = environ[ENVTMPDIR]

    TEMPDIR = normcase(TEMPDIR)


class ntpx(object):
    """Implements Windows NT command shell path manipulation.

    This class implements methods for manipulating paths, including a
    simple formatter that accepts a format string similar to what the
    Windows NT command shell allows.

    Parameters
    ----------
        path : str
            A path that you want to manipulate

        normalize : bool
            Whether or not to normalize the path that is passed in.
            Default is True.
        
    Examples
    --------
    .. code::

        print ntpx('c:/dir/foo.ext').format('dp')  - prints 'c:/dir/'
        print ntpx('c:/dir/foo.ext').format('nx')  - prints 'foo.ext'

    Of course on any Posix system, drive letter doesn't make sense, so
    if you run this same code on Mac OS X or Linux, you'd get:

    .. code::

        print ntpx('c:/dir/foo.ext').format('dp')  - prints 'CWD/c:/dir/'
        print ntpx('c:/dir/foo.ext').format('nx')  - prints 'foo.ext'

    TODO
    ----
    Refactor this code when running on Python 3 to use the :py:mod:`pathlib`
    module, which is a superior alternative with many more features.
    """

    def __init__(self, path, normalize=True):
        from os import sep
        from os.path import abspath, normpath, splitdrive, split, splitext
        from os.path import getsize, getmtime, exists

        if normalize:
            self._full = abspath(normpath(path))
        else:
            self._full = abspath(path)

        self._driv,x = splitdrive(self._full)
        self._path,y = split(x)
        self._path += sep
        self._name,self._ext = splitext(y)

        if exists(self._full):
            self._size = getsize(self._full)
            self._time = getmtime(self._full)

        else:
            self._size = None
            self._time = None


    def all(self):
        """Returns a tuple containing all elements of the object

        This method returns all elements of the path in the form of a tuple.
         e.g.: `(abs_path, drive_letter, path_only, rootname, extension, 
         filesize, time_in_seconds)`.

        Returns
        -------
        tuple
            All elements of the path associated with this object as a tuple.

        Notes
        -----
        If path points to a non-existant file, the size and datetime will
        be returned as None (NoneType).
        """

        return (self._full, self._driv, self._path, self._name, self._ext, self._size, self._time)

    def format(self, fmt):
        """Returns string representing the items specified in the format string

        The format string can contain:

        .. code::

            d - drive letter
            p - path
            n - name
            x - extension
            z - file size
            t - file time in seconds

        And, you can string them together, e.g. `dpnx` returns the fully 
        qualified name.

        On platforms like Unix, where drive letter doesn't make sense, it's simply
        ignored when used in a format string, making it easy to construct fully
        qualified path names in an os independent manner.

        Parameters
        ----------
            fmt : str
                A string representing the elements you want returned.

        Returns
        -------
            str
                A string containing the elements of the path requested in `fmt`
        """

        val = ''
        for x in fmt:
            if x == 'd':
                val += self._driv

            elif x == 'p':
                val += self._path

            elif x == 'n':
                val += self._name

            elif x == 'x':
                val += self._ext

            elif x == 'z':
                if self._size != None: val += str(self._size)

            elif x == 't':
                if self._time != None: val += str(self._time)

        return val

    def drive(self):
        """returns the drive letter

        Returns
        -------
        str
            The drive letter for the path

        Notes
        -----
        Drive letters are a Windows thing. On Posix platforms, this
        will return an empty string.
        """
        return self._driv

    def path(self):
        """returns the path

        Returns
        -------
        str
            Path to the file or directory
        """
        return self._path

    def name(self):
        """returns the name

        Returns
        -------
        str
            Base name of the file or directory
        """
        return self._name

    def ext(self):
        """returns the extension

        Returns
        -------
        str
            Extension of the file or directory
        """
        return self._ext

    def size(self):
        """returns the size of the file

        Returns
        -------
        int
            Size of the file or None if file doesn't exist
        """
        return self._size

    def datetime(self):
        """returns the modified date and time of the file in seconds

        Returns
        -------
        int
            Modify DateTime of the file in seconds or None if file 
            doesn't exist
        """
        return self._time

_pushdstack = []

def parent(pathspec):
    """Return the parent directory of ``pathspec``.

    This function calls abspath() on pathspec before splitting the path.
    If you pass in a partial path, it will return the normalized absolute path,
    and not just any relative path that was on the original pathspec.

    Parameters
    ----------
        pathspec : str
            The path (or partial path) whose parent you want to extract

    Returns
    -------
        str
            The parent directory of ``pathspec``
    """
    from os.path import dirname, abspath
    return dirname(abspath(pathspec))

def pushd(dir=None, throw_if_dir_invalid=True):
    """Push the current working directory (CWD) onto a stack, set CWD to 'dir'

    Save the CWD onto a global stack so that we can return to it later. If dir
    is None, the function simply stores the CWD onto the stack and returns.
    Use :py:meth:`popd()` to restore the original directory.

    Parameters
    ----------
        dir : str, optional
            The directory to switch to or None. If None, the default if it
            is not passed, this function will simply push the current working
            directory onto the global stack and return.
        throw_if_dir_invalid : bool, optional
            Whether or not to pass back up any exception raised by chdir().
            Default is True.

    Returns
    -------
        True : bool
            Success
        False : bool
            Failure

    Raises
    ------
        OSError
            If `throw_if_dir_invalid` is True and chdir raises an exception,
            this function will chain the same exception as chdir, typically 
            OSError

        TypeError
            If the type of ``dir`` is not an instance of `str`

    Notes
    -----
    This method and its counterpart :py:meth:`popd` are `not` thread safe!
    """
    global _pushdstack
    from os import getcwd, chdir

    if dir is None:
        dir = getcwd()

    if not isinstance(dir,type('')):
        raise TypeError("pushd() expected string object, but got {}".format(type(dir)))

    _pushdstack.append(getcwd())
    
    if not dir:
        return

    try:
        chdir(dir)
        err = 0
    except OSError:
        _pushdstack.pop()
        if throw_if_dir_invalid:
            raise
        err = 1

    return True if err == 0 else False

def popd(pop_all=False, throw_if_dir_invalid=True):
    """Restore current working directory to previous directory.

    The previous directory is whatever it was when last :py:meth:`pushd()` was 
    *last* called. :py:meth:`pushd()` creates a stack, so each call to popd() 
    simply sets the CWD back to what it was on the prior pushd() call.

    Parameters
    ----------
        pop_all : bool, optional
            When `pop_all` is True, sets the CWD to the state when pushd() was 
            first called. Does NOT call os.getcwd() for intervening paths, only 
            the final path.

        throw_if_dir_invalid : bool, optional
            Whether or not to pass back up any exception raised by chdir().
            Default is True.

    Returns
    -------
        True : bool
            Success
        False : bool
            Failure

    Raises
    ------
        OSError
            If `throw_if_dir_invalid` is True and chdir raises an exception,
            this function will chain the same exception as chdir, typically 
            OSError

        ValueError
            If popd() called on an empty stack; i.e. before :py:meth:`pushd()`
            has been called.

    Notes
    -----
    This method and its counterpart :py:meth:`pushd` are **not** thread safe!
    """
    global _pushdstack
    from os import chdir

    if len(_pushdstack) == 0:
        raise ValueError("popd() called on an empty stack.")

    if pop_all:
        while( len(_pushdstack) > 1):
            _pushdstack.pop()

    try:
        chdir(_pushdstack.pop())
        err = 0
    except OSError:
        if throw_if_dir_invalid:
            raise
        err = 1

    return err == 0


if (__name__=="__main__"):
    print('PyLib Library Module, not directly callable.')
    from sys import exit
    exit(1)
else:
    _init()
