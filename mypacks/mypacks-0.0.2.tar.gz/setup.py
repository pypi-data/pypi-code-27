import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypacks",
    version="0.0.2",
    author="Asad",
    author_email="melen1um202@gmail.com",
    description="A small example package",
    long_description=long_description,
    url="https://github.com/Melen1um/testpack1",
    packages=setuptools.find_packages(),
    classifiers=[]
)
