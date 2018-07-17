import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="detectDashCam",
    version="0.0.3",
    author="Ayush21298",
    author_email="patel.ayush08@gmail.com",
    description="Detecting if a video is DashCam Video.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ayush21298/ITRI/tree/master/detectDashCam",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)