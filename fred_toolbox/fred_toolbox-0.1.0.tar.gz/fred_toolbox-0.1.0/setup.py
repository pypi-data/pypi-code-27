import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fred_toolbox",
    version="0.1.0",
    author="Fred Liang",
    author_email="info@fredliang.cn",
    description="A toolbox for machine learning and data processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fredliang44/ML_Toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)