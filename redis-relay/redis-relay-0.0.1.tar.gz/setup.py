try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os.path
import re


setup(
    name="redis-relay",
    description="A useful asynchronous library bases on aiobotocore",
    long_description_content_type="text/markdown",
    license="MIT",
    version="0.0.1",
    author="Yingbo Gu",
    author_email="tensiongyb@gmail.com",
    maintainer="Yingbo Gu",
    maintainer_email="tensiongyb@gmail.com",
    py_modules=["redis_relay"],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "coverage", "pytest-cov", "pytest-asyncio"],
)
