from setuptools import setup


def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


with open('./README.rst') as f:
    long_description = f.read()

setup(
    name='swimlane_utils',
    packages=['swimlane_utils'],
    version='0.0.4',
    description='Swimlane Utilities Package',
    author='Swimlane',
    author_email="info@swimlane.com",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['utilities', 'dictionary', 'flattening', 'rest'],
    classifiers=[],
)

