from setuptools import setup, find_packages

def readFile(fileName):
    with open(fileName) as file: return file.read()

setup(
    name="sqlScanner",
    version="1.0.2",
    author="Henning Arvid Ladewig",
    author_email="anne@opentrash.com",
    py_modules=["sqlScanner"],
    description="Scans .db-files for SQL tables.",
    long_description=readFile("README.md"),
    url="https://github.com/letsCodeMyLife/sqlScanner",
    packages=find_packages()
)
