from setuptools import setup, find_packages

setup(
    name='taolunet',
    version='0.1.2',
    author='Wei ZUO',
    author_email='victorzuo@outlook.com',
    packages=find_packages(),
    url='https://github.com/ainrichman/taolunet',
    include_package_data=True,
    license='LICENSE.txt',
    description='Taolunet on Pytorch.',
    long_description=open('README.txt').read(),
    install_requires=[
        "torch==0.4.0",
        "numpy==1.14.5",
        "torchvision==0.2.1",
        "opencv_python==3.3.0.10",
        "scipy==1.0.0"
    ],
)
