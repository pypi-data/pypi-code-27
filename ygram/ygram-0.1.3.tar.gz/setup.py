import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ygram",
    version="0.1.3",
    author="Alexey Yunoshev",
    author_email="alexey.yunoshev@gmail.com",
    description="A simple messenger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexey-yunoshev/python_course_gu",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)