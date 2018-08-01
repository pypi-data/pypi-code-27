import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="chatq_util",
        version="0.0.1",
        author="Khoi Nguyen Hoang",
        author_email="khoi.hoang@chatq.sg",
        description="Chatq utility library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ChatQSG/chatq-helping-hand",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        )
    )