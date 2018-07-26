from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name="readypipe",
        version='0.0.1',
        description="readypipe",
        long_description="",
        author='Yipit Coders',
        author_email='coders@yipitdata.com',
        url='http://www.readypipe.io/',
        packages=find_packages(exclude=['*tests*']),
        install_requires=[],
        include_package_data=True,
        dependency_links=[],
        classifiers=[
            'Programming Language :: Python',
        ],
        zip_safe=False,
    )
