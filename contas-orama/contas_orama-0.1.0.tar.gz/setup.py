import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="contas_orama",
    version="0.1.0",
    author="Felippe",
    author_email="felippemsc@gmail.com",
    description="API para gestão de contas financeiras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felippemsc/teste_orama",
    packages=setuptools.find_packages(),
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        "License :: OSI Approved :: MIT License",
    ),
)
