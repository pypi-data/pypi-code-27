
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='cynpy',
      version='0.15',
      description='Ray\'s public DVT utilities in Python 2.7',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://canyon-semi.com.tw',
      author='Ray Huang',
      author_email='rayjhuang@msn.com',
      license='MIT',
      packages=setuptools.find_packages(),
      package_data={
          '' : ['py_writer.bat']
          },
      zip_safe=False)
