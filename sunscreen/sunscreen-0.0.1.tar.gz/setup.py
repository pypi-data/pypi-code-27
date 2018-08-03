from setuptools import setup


setup(
    name="sunscreen",
    version="0.0.1",
    description="What's the UV forecast?",
    author="Jon Miller",
    author_email="jondelmil@gmail.com",
    url="https://github.com/jmillxyz/sunscreen",
    py_modules=["sunscreen"],
    install_requires=["appdirs", "arrow", "colored", "click", "requests"],
    entry_points="""
        [console_scripts]
        sunscreen=sunscreen:main
    """,
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ),
)
