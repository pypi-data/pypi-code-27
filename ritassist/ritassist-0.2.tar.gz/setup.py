from setuptools import setup

setup(name='ritassist',
      version='0.2',
      description='RitAssist API Access',
      url='http://github.com/depl0y/ritassist-py',
      author='Wim Haanstra',
      author_email='wim@wim.me',
      license='MIT',
      packages=['ritassist'],
      install_requires=[
          'requests',
      ],
      python_requires='>=3',
      zip_safe=False)