import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pokemonscli",
    packages = ["pokemonscli"],
    entry_points = {
        "console_scripts": ['pokemon = pokemonscli.pokemonscli:main']
        },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.0",
    description = "Get Awesome Random pokemon names in CLI!",
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
        'Source': 'https://gitlab.com/yoginth/pokemonscli',
    },
    install_requires=[
        'pokemons',
    ],
)
