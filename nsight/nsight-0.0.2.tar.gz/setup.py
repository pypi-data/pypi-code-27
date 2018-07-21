import os
from setuptools import setup

# nsight
# Determine services on a server and possible pivots for pentesting


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="nsight",
    version="0.0.2",
    description="Determine services on a server and possible pivots for pentesting",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3+",
    keywords="",
    url="https://www.bitbucket.org/johannestaas/nsight",
    packages=['nsight'],
    package_dir={'nsight': 'nsight'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'nsight=nsight:main',
        ],
    },
    package_data={
        'nsight': ['data/*.txt'],
    },
    include_package_data=True,
)
