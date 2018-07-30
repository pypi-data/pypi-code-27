import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wgkits",
    version="0.1.1",
    author="rontgen",
    author_email="rontgen@pku.edu.cn",
    description="Android build apk tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rontgen/wgkits",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'jinja2',
        'backports.shutil_which',
    ],
)
