import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example_pkg_riturajjtest",
    version="0.1.0",
    author="Rituraj Jagtap",
    author_email="riturajj@google.com",
    description="A small example package",
    long_description=long_description,
    url="https://github.com/riturajj/example_pkg_riturajjtest",
    packages=setuptools.find_packages()
)
