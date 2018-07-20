import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='animal-cuties',
     description='get sum cute lil ascii animals in your terminal',
     author='unwoundclock',
     author_email='unwoundclock@gmail.com',
     version='0.1',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/unwound/animal-cuties.git",
     scripts=['animal-cuties.py','README.md','LICENSE'],
     packages=setuptools.find_packages(),
     classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
 )
