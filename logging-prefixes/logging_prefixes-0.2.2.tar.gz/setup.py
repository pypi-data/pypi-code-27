from setuptools import find_packages, setup

setup(
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
