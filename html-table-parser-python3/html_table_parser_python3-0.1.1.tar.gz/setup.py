import setuptools

setuptools.setup(name='html_table_parser_python3',
                 version='0.1.1',
                 description='A small and simple HTML table parser not requiring any external dependency.',
                 url='https://github.com/ahobsonsayers/html-table-parser-python3',
                 author='Arran Hobson Sayers',
                 author_email='ahobsonsayers@gmail.com',
                 license='AGPLv3',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 classifiers=(
                     "Programming Language :: Python :: 3 :: Only",
                     "License :: OSI Approved :: GNU Affero General Public License v3",
                     "Operating System :: OS Independent",
                     "Topic :: Text Processing :: Markup :: HTML")
                 )
