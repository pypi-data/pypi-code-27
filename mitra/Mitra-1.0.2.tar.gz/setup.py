import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mitra",
    version="1.0.2",
    author="Rahul Dangi & Som Durgesh Gupta",
    author_email="rdsquare144@gmail.com",
    description="Provides basic operatons of Matrix and solve system of linear equations using Matrix.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdsquare/Mitra.git",
    license="GNU General Public License, Version 3",
    packages=setuptools.find_packages(),
    classifiers=(
        "Intended Audience :: Developers",
	"Intended Audience :: Science/Research",
	"Topic :: Software Development :: Libraries",	
	"License :: OSI Approved",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
