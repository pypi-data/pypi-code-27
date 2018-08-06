import setuptools

with open("README.md", encoding="utf-8", mode="r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cucumber-json-to-junit-xml",
    version="0.0.8",
    author="Raymond Elias",
    author_email="ray.s.elias@gmail.com",
    description="Cucumber JSON to JUnit XML report conversion script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rselias/Cucumber-JSON-to-JUnit",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": ["json_to_junit = cucumber_json_to_junit_xml.cucumber_json_to_junit:main"],
        }
)
