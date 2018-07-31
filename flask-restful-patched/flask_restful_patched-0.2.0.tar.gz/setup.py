import setuptools
import re

with open("README.rst", "r") as fh:
    # long_description = re.sub('^\.\. highlight.*\n?', '', fh.read(), flags=re.MULTILINE)
    long_description = fh.read()

setuptools.setup(
    name="flask_restful_patched",
    version_format="{tag}",
    author="David Jablonski",
    author_email="dayjaby@gmail.com",
    description="flask restful patched according to https://github.com/frol/flask-restplus-server-example",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/dayjaby/flask_restplus_patched",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask_restplus',
        'marshmallow',
        'flask_marshmallow',
        'flask_sqlalchemy',
        'webargs',
        'apispec',
        'flasgger'
    ],
    setup_requires=['setuptools-git-version'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
