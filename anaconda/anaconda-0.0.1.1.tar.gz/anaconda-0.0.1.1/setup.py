from setuptools import setup

long_description = """\
Anaconda Python cannot be installed via pip or other PyPI-based installers.
Please use the Anaconda Installer to bootstrap Anaconda Python onto your system.
"""

setup(
    name = "anaconda",
    version = "0.0.1.1",
    author = "Kale Franz",
    author_email = "kfranz@anaconda.com",
    description = "Please use the Anaconda installer.",
    long_description=long_description,
)
