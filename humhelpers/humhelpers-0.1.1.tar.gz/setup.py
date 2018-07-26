import setuptools

with open("README.txt", "tr") as fh:
    long_description = fh.read()

setuptools.setup(
    name="humhelpers",
    version="0.1.1",
    author="vlad1777d (Vladislav Naumov)",
    author_email="naumovvladislav@mail.ru",
    description="Different shortcuts functions (helpers) for humanity.",
    long_description=long_description,
    url="https://vlad1777d@bitbucket.org/vlad1777d/humhelpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

