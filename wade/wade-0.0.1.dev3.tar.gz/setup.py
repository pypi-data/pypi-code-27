from setuptools import setup, find_packages  

# chardet's setup.py
from distutils.core import setup

setup(
    name = "wade",
    version = "0.0.1.dev3",
    description = "Web Application Downtime Estimation",
    author = "wizardbyron",
    author_email = "wizard0530@gmail.com",
    url = "https://github.com/wizardbyron/wade",
    keywords = ["url", "redirection", "redirect", "verify", "test", "tests"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities"
        ],
    install_requires=['requests'],
    packages = find_packages(),
    entry_points={  
        'console_scripts':[ 
            'wade = wade.wade:main'      
        ] 
    },
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    long_description = "Web Application Downtime Estimation."
)