import setuptools

setuptools.setup(
    name='cziconvert',
    version='0.1.1',
    description='Convert czi files to images and/or video.',
    author='Brian Knep',
    author_email='None@none.com',
    url='http://pypi.org',
    scripts=['bin/cziconvert'],
    install_requires=[
        'cython',
        'czifile',
        'imageio'
    ],
    license='BSD',
)
