import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example_pkg_sbedi",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["pywinauto","autopy==0.51","selenium","SendKeys","requests","lxml==3.4.2","ifaddr","py-cpuinfo","xmltodict","netifaces","winregistry","pypiwin32==219","psutil","pyautogui"],
	 classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
