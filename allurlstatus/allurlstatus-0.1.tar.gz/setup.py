from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='allurlstatus',
      version='0.1',
      description='pypi package to get status of all urls',
      long_description=readme(),
      url='https://github.com/jogind3r/allurlstatus',
      author='jogind3r',
      author_email='jogind3r@gmail.com',
      license='MIT',
      packages=find_packages(),
      keywords="url status",
      scripts=['bin/getallurlstatus'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      project_urls={
          "Source Code": "https://github.com/jogind3r/allurlstatus",
      },
      include_package_data=True,
      zip_safe=False)
