import setuptools

with open("README.rst", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="schedule_jobs",
    version="0.0.4",
    author="Tsotsi",
    author_email="tsotsi@tsotsi.cn",
    description="A Schedule Jobs Library",
    long_description=long_description,
    url="https://github.com/Tsotsi/schedule_jobs",
    packages=setuptools.find_packages(exclude=['test*', 'jobs', '.idea']),
    install_requires=[
        'schedule>=0.5.0,<1',
        'six>=1.11.0,<2'
    ],
    python_requires="~=3.6",
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
    )
)