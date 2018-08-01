import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "catnamescli",
    packages = ["catnamescli"],
    entry_points = {
        "console_scripts": ['catname = catnamescli.catnamescli:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.0",
    description = "Get Awesome Random cat names in CLI!",
    author = "Yoginth",
    author_email = "yoginth@zoho.com",
    url = "https://yoginth.gitlab.io",
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
        'Source': 'https://gitlab.com/yoginth/catnamescli',
    },
    install_requires=[
        'catnames',
    ],
)
