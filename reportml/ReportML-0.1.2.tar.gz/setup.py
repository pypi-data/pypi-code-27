from setuptools import setup,find_packages
setup(
    name='ReportML',
    version='0.1.2',
    author='Josh McGrath',
    author_email='mcgrath@cs.wisc.edu',
    package_dir={'':'.'},
    packages= find_packages("."),
    description='A simple reporting tool for ML',
    install_requires=[
        "matplotlib",
        "weasyprint",
        "jinja2"
    ],
    include_package_data=True,
    package_data = {'':['*.html']}
)