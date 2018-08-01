import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "superbcli",
    packages = ["superbcli"],
    entry_points = {
        "console_scripts": ['superb = superbcli.superbcli:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.3",
    description = "Get Awesome Random Words in CLI!",
    author = "Yoginth",
    author_email = "yoginth@zoho.com",
    url = "https://yoginth.ml",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Patreon': 'https://www.patreon.com/yoginth',
        'Source': 'https://gitlab.com/yoginth/superbcli',
    },
    install_requires=[
        'superb',
    ],
)
