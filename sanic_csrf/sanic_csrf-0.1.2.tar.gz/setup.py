import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sanic_csrf",
    version="0.1.2",
    author="vlad1777d (Vladislav Naumov)",
    author_email="naumovvladislav@mail.ru",
    description="Protection from CSRF attacks for Sanic framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlad1777d/sanic_csrf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

