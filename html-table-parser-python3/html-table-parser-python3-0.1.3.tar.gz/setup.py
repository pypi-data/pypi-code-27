import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='html-table-parser-python3',
                 version='0.1.3',
                 description='A small and simple HTML table parser not requiring any external dependency.',
                 url='https://github.com/ahobsonsayers/html_table_parser_python3',
                 author='Arran Hobson Sayers',
                 author_email='ahobsonsayers@gmail.com',
                 license='AGPLv3',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 classifiers=(
                     "Programming Language :: Python :: 3 :: Only",
                     "License :: OSI Approved :: GNU Affero General Public License v3",
                     "Operating System :: OS Independent",
                     "Topic :: Text Processing :: Markup :: HTML")
                 )
