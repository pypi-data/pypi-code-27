import setuptools

setuptools.setup(
    name='dynamo-consistency',
    version='1.2.1',
    packages=['dynamo_consistency'],
    author='Daniel Abercrombie',
    author_email='dabercro@mit.edu',
    description='Consistency plugin for Dynamo',
    url='https://github.com/SmartDataProjects/dynamo-consistency',
    install_requires=['timeout-decorator',
                      'cmstoolbox>=0.8.2'],
    python_requires='>=2.6, <3',
    package_data={   # Test data for document building
        'dynamo_consistency': ['consistency_config.json']
        }
    )
