import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="four_relay",
    version="0.1.2",
    author="HAchina",
    author_email="648993779@qq.com",
    description="Four relay control for micropython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.hachina.io",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
