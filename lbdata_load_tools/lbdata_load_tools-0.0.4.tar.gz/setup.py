import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='lbdata_load_tools',
    version='0.0.4',
    author='Alexandre PECCAUD',
    author_email='alexandre.peccaud@gmail.com',
    description='Tools to help loading data in Redshift',
    long_description=long_description,
    url='https://github.com/lovebonito/lbdata_load_tools',
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3==1.7.44',
        'botocore==1.10.44',
        'psycopg2==2.7.5',
        'psycopg2-binary==2.7.5'
    ]
)
