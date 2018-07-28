
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='cynpy',
      version='0.17',
      description='Ray\'s public DVT utilities in Python 2.7',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://canyon-semi.com.tw',
      author='Ray Huang',
      author_email='rayjhuang@msn.com',
      zip_safe=False,
      packages=setuptools.find_packages(),
      package_data={
          '' : ['py_writer.bat'],
          },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Win32 (MS Windows)',
          'Framework :: IDLE',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows :: Windows 7',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
          ],
      )
