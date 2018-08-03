import os
from setuptools import setup, find_packages


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(
    name='interactive-judger-py',
    version='1.0.0',
    description="An interactive program judger for Python3",
    long_description=read('README.md'),
    author='AD1024',
    author_email='dh63@uw.edu',
    python_requires='>=3.6.0',
    license='AGPL',
    packages=find_packages('src', exclude=['*.pyc', '__pycache__', '.DS_Store']),
    package_dir={'': 'src'},
    keywords=['interactive', 'tester', 'cli'],
    url='https://github.com/AD1024/InteractiveJudgerPy',
    entry_points={
        'console_scripts': [
            'interactive_judge = interactive_judger:start_judge',
            'add_judge_config = interactive_judger:add_config',
            'remove_config = interactive_judge:remove_config',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]

)
