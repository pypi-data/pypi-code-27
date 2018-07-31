import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="PySimpleGUI",
    version="2.7.0",
    author="MikeTheWatchGuy",
    author_email="mike@VideoPlusInc.com",
    description="A simple to understand, easy to use,  HIGHLY customizable GUI for Python. Based solely on tkinter. Make your own GUIs. Runs on Raspberry Pi too.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MikeTheWatchGuy/PySimpleGUI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)