from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

setup(
        name="cloudshell-cp-core",
        author="Quali",
        author_email="support@qualisystems.com",
        description=("A repository for projects providing out of the box capabilities within CloudShell to parse and "
                     "convert cloushell driver request to well defined python objects."
                     "One cloudshell-cp-core For All cloudshell cloud provider shells."),
        packages=find_packages(),
        test_suite='nose.collector',
        package_data={'': ['*.txt']},
        install_requires=[],
        version=version_from_file,
        include_package_data=True,
        keywords="sandbox cloudshell json request",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: Apache Software License",
        ],
        requires=[]
)
