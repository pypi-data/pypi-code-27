from setuptools import setup, find_packages

setup(
    name='random_name_generator',
    version='1.0.7',
    packages=find_packages(),
    package_data = {'':['random_name_generator/files/*.txt']},
    data_files=[("random_name_generator",
             ["random_name_generator/resources/adjectives.txt", "random_name_generator/resources/latin_adjectives.txt",
              "random_name_generator/resources/latin_nouns.txt","random_name_generator/resources/nouns.txt",
              "random_name_generator/resources/sicilian_nouns.txt"])],
    python_requires='~=3.6',
    url='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='Random Names Generator',
    install_requires=[],
    include_package_data=True

)
