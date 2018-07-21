from distutils.core import setup

setup(name="help_support",
      version="0.2",
      description="Python built-in help() function support for linked ctypes functions and structures.",
      long_description=open("README.txt", "r").read(),
      author="Dalen Bernaca",
      author_email="dbernaca@gmail.com",
      py_modules=["help_support"],
      keywords=["help", "ctypes", "functions", "structures", "shared object", "dynamic linked library", "dylib", "so", "dll"],
      license="GPL",
      classifiers=(
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules')
    )