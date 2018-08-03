### 20180803
### % python setup.py sdist
### % twine upload dist/* --skip-existing
###   Enter your username: rayjhuang
###   Enter your password: xxxxddmm
### % pip search cynpy
### % pip install cynpy --upgrade --no-cache-dir

### $ SET TOTALPHASEPATH=Y:\project\tools\TotalPhase
### $ SET TOTALPHASEPATH=%CD%\..\..\tools\TotalPhase
### $ SET MYPYPATH=E:\Dropbox\script\python
### $ SET MYPY=%MYPYPATH%\rapy
### $ SET PYTHONPATH=%MYPYPATH%;%TOTALPHASEPATH%\aardvark-api-windows-x86_64-v5.13\python
### $ @PATH=%CD%;%PATH%

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='cynpy',
      version='0.201',
      description='Ray\'s public DVT utilities in Python 2.7',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://canyon-semi.com.tw',
      author='Ray Huang',
      author_email='rayjhuang@msn.com',
      zip_safe=False,
      packages=setuptools.find_packages(),
      package_data={
          '' : ['*.bat'],
          },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Win32 (MS Windows)',
          'Framework :: IDLE',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows :: Windows 7',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
          ],
      )
