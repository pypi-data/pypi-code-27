import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_pyirc",
    version="0.0.1",
    author="Maël Kervella",
    author_email="dev@maelkervella.eu",
    description="A light-weighted IRC client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/MoaMoaK/simple-pyirc",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
    ),
)
