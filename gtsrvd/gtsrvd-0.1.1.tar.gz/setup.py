from setuptools import setup, find_packages


setup(
    name="gtsrvd",
    version="0.1.1",
    description=("gtsrvd proxies localhost to public internet"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="aws ngrok serveo",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    url="https://github.com/narfman0/gtsrvd",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["boto3", "requests", "click"],
    zip_safe=True,
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "gtsrvd-create=gtsrvd.cli:create",
            "gtsrvd-delete=gtsrvd.cli:delete",
        ]
    },
)
