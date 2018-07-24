import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drypy_airflow",
    version="0.0.3",
    author="dhan16",
    author_email="chandan.nath@gmail.com",
    description="Airflow extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhan16/drypy-airflow",
    packages=setuptools.find_packages(),
    license="Apache License Version 2.0, January 2004",
)
