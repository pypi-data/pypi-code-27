import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'rolldice_binding',
    version = '0.1',
    author = 'Berin Smaldon',
    author_email = 'noodels555@gmail.com',
    description = 'Command line bindings for the py-rolldice library',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/bsmaldon/rolldice-binding',
    packages = setuptools.find_packages(),
    classifiers = (
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        ),
    install_requires = [
        'py-rolldice'
        ],
    python_requires = '>=3.5',
    entry_points = {
        'console_scripts': [
            'rolldice = rolldice_binding.__main__:main',
            ]
        }
    )
