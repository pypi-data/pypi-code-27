from setuptools import find_packages, setup

setup(
    version='0.0.2.3',
    name="pyrspb",
    packages=find_packages(),
    author="RS Pocketbook",
    author_email="admin@rspocketbook.com",
    url="https://gitlab.com/RS_PocketBot/pyrspb",
    install_requires=[
        "beautifulsoup4",
        "requests",
        "sqlalchemy"
    ],
    include_package_data=True
)
