#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is the module's setup script.  To install this module, run:
#
#   python setup.py install
#
"""RotatingFileHandler replacement with concurrency, gzip and Windows support

Overview
========
This package provides an additional log handler for Python's standard logging
package (PEP 282). This handler will write log events to a log file which is
rotated when the log file reaches a certain size.  Multiple processes can
safely write to the same log file concurrently. Rotated logs can be gzipped
if enabled. Both Windows and POSIX systems are supported. An optional threaded
queue logging handler is provided to perform logging in the background.

This is a fork from Lowell Alleman's version with updates for Windows and
recent versions of Python. It should be a drop-in replacement for users
of the old version, except for changing the package name from
`cloghandler` to `concurrent_log_handler`.

Details
=======
.. _portalocker:  http://code.activestate.com/recipes/65203/

The ``ConcurrentRotatingFileHandler`` class is a drop-in replacement for
Python's standard log handler ``RotatingFileHandler``. This module uses file
locking so that multiple processes can concurrently log to a single file without
dropping or clobbering log events. This module provides a file rotation scheme
like with ``RotatingFileHanler``.  Extra care is taken to ensure that logs
can be safely rotated before the rotation process is started. (This module works
around the file rename issue with ``RotatingFileHandler`` on Windows, where a
rotation failure means that all subsequent log events are dropped).

This module attempts to preserve log records at all cost. This means that log
files will grow larger than the specified maximum (rotation) size. So if disk
space is tight, you may want to stick with ``RotatingFileHandler``, which will
strictly adhere to the maximum file size.

If you have multiple instances of a script (or multiple scripts) all running at
the same time and writing to the same log file, then *all* of the scripts should
be using ``ConcurrentRotatingFileHandler``. You should not attempt to mix
and match ``RotatingFileHandler`` and ``ConcurrentRotatingFileHandler``.

This package bundles `portalocker`_ to deal with file locking.

Installation
============
Use the following command to download and install this package::

    pip install concurrent-log-handler

If you are installing from source, you can use::

    python setup.py install


Examples
========

Simple Example
--------------
Here is a example demonstrating how to use this module directly (from within
Python code)::

    from logging import getLogger, INFO
    from concurrent_log_handler import ConcurrentRotatingFileHandler
    import os

    log = getLogger()
    # Use an absolute path to prevent file rotation trouble.
    logfile = os.path.abspath("mylogfile.log")
    # Rotate log after reaching 512K, keep 5 old copies.
    rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", 512*1024, 5)
    log.addHandler(rotateHandler)
    log.setLevel(INFO)

    log.info("Here is a very exciting log message, just for you")


Automatic fallback example
--------------------------
If you are distributing your code and you are unsure if the
`concurrent_log_handler` package has been installed everywhere your code will run,
Python makes it easy to gracefully fallback to the built in
`RotatingFileHandler`, here is an example::

    try:
        from concurrent_log_handler import ConcurrentRotatingFileHandler as RFHandler
    except ImportError:
        # Next 2 lines are optional:  issue a warning to the user
        from warnings import warn
        warn("concurrent_log_handler package not installed.  Using builtin log handler")
        from logging.handlers import RotatingFileHandler as RFHandler

    log = getLogger()
    rotateHandler = RFHandler("/path/to/mylogfile.log", "a", 1048576, 15)
    log.addHandler(rotateHandler)



Config file example
-------------------
This example shows you how to use this log handler with the logging config file
parser. This allows you to keep your logging configuration code separate from
your application code.

Example config file: ``logging.ini``::

    [loggers]
    keys=root

    [handlers]
    keys=hand01

    [formatters]
    keys=form01

    [logger_root]
    level=NOTSET
    handlers=hand01

    [handler_hand01]
    class=handlers.ConcurrentRotatingFileHandler
    level=NOTSET
    formatter=form01
    args=("rotating.log", "a", 512*1024, 5)

    [formatter_form01]
    format=%(asctime)s %(levelname)s %(message)s

Example Python code: ``app.py``::

    import logging, logging.config
    import concurrent_log_handler

    logging.config.fileConfig("logging.ini")
    log = logging.getLogger()
    log.info("Here is a very exciting log message, just for you")


Change Log
==========
- 0.9.11: Fix issues with gzip compression option (use buffering)

- 0.9.10: Fix inadvertent lock sharing when forking
   Thanks to @eriktews for this fix

- 0.9.9: Fix Python 2 compatibility broken in last release

- 0.9.8: Bug fixes and permission features
   * Fix for issue #4 - AttributeError: 'NoneType' object has no attribute 'write'
      This error could be caused if a rollover occurred inside a logging statement
      that was generated from within another logging statement's format() call.
   * Fix for PyWin32 dependency specification (explicitly require PyWin32)
   * Ability to specify owner and permissions (mode) of rollover files [Unix only]

- 0.9.7 / 0.9.6: Fix platform specifier for PyPi

- 0.9.5: Add `use_gzip` option to compress rotated logs. Add an optional threaded
logging queue handler based on the standard library's `logging.QueueHandler`.

- 0.9.4: Fix setup.py to not include tests in distribution.

- 0.9.3: Refactoring release
   * For publishing fork on pypi as `concurrent-log-handler` under new package name.
   * NOTE: PyWin32 is required on Windows but is not an explicit dependency because
           the PyWin32 package is not currently installable through pip.
   * Fix lock behavior / race condition

- 0.9.2: Initial release of fork by Preston Landers.
   * Fixes deadlocking issue with recent versions of Python
   * Puts `.__` prefix in front of lock file name
   * Use `secrets` or `SystemRandom` if available.
   * Add/fix Windows support

.. _Red Hat Bug #858912: https://bugzilla.redhat.com/show_bug.cgi?id=858912
.. _Python Bug #15960: http://bugs.python.org/issue15960
.. _LP Bug 1199332: https://bugs.launchpad.net/python-concurrent-log-handler/+bug/1199332
.. _LP Bug 1199333: https://bugs.launchpad.net/python-concurrent-log-handler/+bug/1199333


- 0.9.1:  Bug fixes - `LP Bug 1199332`_ and `LP Bug 1199333`_.
   * More gracefully handle out of disk space scenarios. Prevent release() from
     throwing an exception.
   * Handle logging.shutdown() in Python 2.7+. Close the lock file stream via
     close().
   * Big thanks to Dan Callaghan for forwarding these issues and patches.

- 0.9.0:  Now requires Python 2.6+
   * Revamp file opening/closing and file-locking internals (inspired by
     feedback from Vinay Sajip.)
   * Add the 'delay' parameter (delayed log file opening) to better match the
     core logging functionality in more recent version of Python.
   * For anyone still using Python 2.3-2.5, please use the latest 0.8.x release

- 0.8.6:  Fixed packaging bug with test script
   * Fix a small packaging bug from the 0.8.5 release.  (Thanks to Björn Häuser
     for bringing this to my attention.)
   * Updated stresstest.py to always use the correct python version when
     launching sub-processes instead of the system's default "python".

- 0.8.5:  Fixed ValueError: I/O operation on closed file
   * Thanks to Vince Carney, Arif Kasim, Matt Drew, Nick Coghlan, and
     Dan Callaghan for bug reports.  Bugs can now be filled here:
     https://bugs.launchpad.net/python-concurrent-log-handler.  Bugs resolved
     `Red Hat Bug #858912`_ and `Python Bug #15960`_
   * Updated ez_setup.py to 0.7.7
   * Updated portalocker to 0.3 (now maintained by Rick van Hattem)
   * Initial Python 3 support (needs more testing)
   * Fixed minor spelling mistakes

- 0.8.4:  Fixed lock-file naming issue
   * Resolved a minor issue where lock-files would be improperly named if the
     log file contained ".log" in the middle of the log name.  For example, if
     you log file was "/var/log/mycompany.logging.mysource.log", the lock file
     would be named "/var/log/mycompany.ging.mysource.lock", which is not correct.
     Thanks to Dirk Rothe for pointing this out.  Since this introduce a slight
     lock-file behavior difference, make sure all concurrent writers are updated
     to 0.8.4 at the same time if this issue effects you.
   * Updated ez_setup.py to 0.6c11

- 0.8.3:  Fixed a log file rotation bug and updated docs
   * Fixed a bug that happens after log rotation when multiple processes are
     witting to the same log file. Each process ends up writing to their own
     log file ("log.1" or "log.2" instead of "log"). The fix is simply to reopen
     the log file and check the size again.  I do not believe this bug results in
     data loss; however, this certainly was not the desired behavior.  (A big
     thanks goes to Oliver Tonnhofer for finding, documenting, and providing a
     patch for this bug.)
   * Cleanup the docs. (aka "the page you are reading right now") I fixed some
     silly mistakes and typos... who writes this stuff?

- 0.8.2:  Minor bug fix release (again)
   * Found and resolved another issue with older logging packages that do not
     support encoding.

- 0.8.1:  Minor bug fix release
   * Now importing "codecs" directly; I found some slight differences in the
     logging module in different Python 2.4.x releases that caused the module to
     fail to load.

- 0.8.0:  Minor feature release
    * Add better support for using ``logging.config.fileConfig()``. This class
      is now available using ``class=handlers.ConcurrentRotatingFileHandler``.
    * Minor changes in how the ``filename`` parameter is handled when given a
      relative path.

- 0.7.4:  Minor bug fix
    * Fixed a typo in the package description (incorrect class name)
    * Added a change log; which you are reading now.
    * Fixed the ``close()`` method to no longer assume that stream is still
      open.

To-do
=====
* This module has had minimal testing in a multi-threaded process.  I see no
  reason why this should be an issue, but no stress-testing has been done in a
  threaded situation. If this is important to you, you could always add
  threading support to the ``stresstest.py`` script and send me the patch.

* Update: this works in a multi-process concurrency environment but I have
  not tested it extensively with threads or async, but that should be handled
  by the parent logging class.
"""

import sys

extra = {}
if sys.version_info >= (3, 0):
    extra['use_2to3'] = True

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup

VERSION = "0.9.11"
classifiers = """\
Development Status :: 4 - Beta
Topic :: System :: Logging
Operating System :: POSIX
Operating System :: Microsoft :: Windows
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Topic :: Software Development :: Libraries :: Python Modules
License :: OSI Approved :: Apache Software License
"""
doc = __doc__.splitlines()

install_requires = []
if "win" in sys.platform:
    try:
        import win32file
    except ImportError:
        # Only require pywin32 if not already installed
        # version 223 introduced ability to install from pip
        install_requires.append("pywin32>=223")

setup(name='concurrent-log-handler',
      version=VERSION,
      author="Preston Landers",
      author_email="planders@gmail.com",
      packages=['concurrent_log_handler'],
      package_dir={'': 'src', },
      # These aren't needed by the end user and shouldn't be installed to the Python root.
      # data_files=[
      #     ('tests', ["stresstest.py"]),
      #     ('docs', [
      #         'README.md',
      #         'LICENSE',
      #     ]),
      # ],
      url="https://github.com/Preston-Landers/concurrent-log-handler",
      license="http://www.apache.org/licenses/LICENSE-2.0",
      description=doc.pop(0),
      long_description="\n".join(doc),
      # platforms=["nt", "posix"],
      install_requires=install_requires,
      keywords="logging, windows, linux, unix, rotate, QueueHandler, QueueListener, portalocker",
      classifiers=classifiers.splitlines(),
      zip_safe=True,
      # test_suite=unittest.TestSuite,
      **extra
      )

# Development build:
# python setup.py clean build sdist bdist_wheel
