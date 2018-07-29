from setuptools import setup

setup(name='pyfnip',
      version='0.2',
      description='Python wrapper for FutureNow IP relay/dimmer units',
      url='http://github.com/juhaniemi/pyfnip',
      author='Juha Niemi',
      author_email='juha@juhaniemi.net',
      packages=['pyfnip'],
      classifiers=("Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"),
      zip_safe=False)
