from setuptools import setup, find_packages

with open("README.md") as fp:
    readme = fp.read()

with open("requirements.txt") as fp:
    req = [r.strip() for r in fp.readlines()]

setup(
    name='debu',
    version='0.0.3',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url='https://github.com/SiLeader/debu',
    license='Apache License 2.0',
    author='SiLeader',
    author_email='',
    description='Automatic Deployment and Build tool',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=req,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Interpreters",
        "Topic :: System",
        "Topic :: System :: Installation/Setup"
    ],

    entry_points={
        "console_scripts": [
            "debu=debu.interpreter:main"
        ]
    },
    python_requires=">=3.5"
)
