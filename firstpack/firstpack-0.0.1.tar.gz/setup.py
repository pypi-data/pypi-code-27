# @Author: Cameron Owens <cameron>
# @Date:   2018-07-17T20:58:47-05:00
# @Email:  cameronallanowens@gmail.com
# @Last modified by:   cameron
# @Last modified time: 2018-07-17T23:06:18-05:00

"""
setup.py install file for the firstpack package
"""


from distutils.core import setup

setup(name='firstpack',
      version='0.0.1',
      description='How to create a python package',
      url="https://github.com/ideaGarageIO/PythonTutorials/tree/master/PackageCreation/Lesson1/FirstPack",
      author='Cameron Owens',
      author_email='cameronallanowens@gmail.com',
      license='BSD 3-Clause',
      packages=['firstpack','firstpack.classes', 'firstpack.methods','firstpack.categoryX'],
)
