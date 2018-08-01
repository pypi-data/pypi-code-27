from distutils.core import setup
setup(
    name='ReportML',
    version='0.1.0',
    author='Josh McGrath',
    author_email='mcgrath@cs.wisc.edu',
    packages=['report_ml'],
    description='A simple reporting tool for ML',
    install_requires=[
        "matplotlib",
        "weasyprint",
        "jinja2"
    ],
    include_package_data=True
)