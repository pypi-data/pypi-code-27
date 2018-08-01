import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "heroescli",
    packages = ["heroescli"],
    entry_points = {
        "console_scripts": ['hero = heroescli.heroescli:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.2",
    description = "Get Awesome Random Heroes names in CLI!",
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
        'Source': 'https://gitlab.com/yoginth/heroescli',
    },
    install_requires=[
        'heroes',
    ],
)
