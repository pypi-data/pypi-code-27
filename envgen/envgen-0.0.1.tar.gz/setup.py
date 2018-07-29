import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="envgen",
    version="0.0.1",
    author="Jonathan Beabout",
    author_email="jonebeabout@gmail.com",
    description="A Virtual Environment Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonebeabout/envgen",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ),
    entry_points = {
        'console_scripts': ['envgen-cli=envgen.interface:main','envgen-api=envgen.server:main'],
    },
    install_requires = [
        'aniso8601>=3.0.2',
        'asn1crypto>=0.24.0',
        'bcrypt>=3.1.4',
        'cffi>=1.11.5',
        'click>=6.7',
        'colorama>=0.3.9',
        'cryptography>=2.2.2',
        'enum34>=1.1.6',
        'fabric>=2.2.0',
        'Flask>=1.0.2',
        'Flask-RESTful>=0.3.6',
        'idna>=2.7',
        'invoke>=1.1.0',
        'ipaddress>=1.0.22',
        'itsdangerous>=0.24',
        'Jinja2>=2.10',
        'MarkupSafe>=1.0',
        'paramiko>=2.4.1',
        'psutil>=5.4.6',
        'pyasn1>=0.4.3',
        'pycparser>=2.18',
        'PyNaCl>=1.2.1',
        'python-vagrant>=0.5.15',
        'pytz>=2018.5',
        'six>=1.11.0',
        'Werkzeug>=0.14.1'
    ]
)
