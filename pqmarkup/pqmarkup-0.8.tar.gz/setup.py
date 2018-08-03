from setuptools import setup
setup(
    name = 'pqmarkup',
    py_modules = ['pqmarkup'],
    version = '0.8',
    description = 'A Python implementation of pq markup to HTML converter.',
    long_description = open('README.md', encoding = 'utf-8').read(),
    long_description_content_type = 'text/markdown',
    author = 'Alexander Tretyak',
    author_email = 'pqmarkup@gmail.com',
    url = 'http://pqmarkup.org',
    download_url = 'https://bitbucket.org/pqmarkup/pqmarkup/get/default.zip',
    license = "BSD",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
