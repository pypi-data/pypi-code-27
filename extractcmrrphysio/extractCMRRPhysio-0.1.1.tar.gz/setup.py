import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.1.1"
setuptools.setup(name='extractCMRRPhysio',
                 version=VERSION,
                 description='extractCMRRPhysio.m(https://github.com/CMRR-C2P/MB/blob/master/extractCMRRPhysio.m) in Python',
                 author='YingLi Lu',
                 author_email='yinglilu@gmail.com',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/yinglilu/extractCMRRPhysio",
                 license='MIT',
                 entry_points={
                     'console_scripts': [
                         'extractCMRRPhysio = extractCMRRPhysio.main:run']},
                 packages=setuptools.find_packages(),
                 install_requires=['pydicom'],
                 zip_safe=False)
