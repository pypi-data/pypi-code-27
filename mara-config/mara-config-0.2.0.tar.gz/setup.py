from setuptools import setup, find_packages

def get_long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name='mara-config',
    version='0.2.0',

    description="Mara app composing and configuration infrastructure.",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    install_requires=[
        # only for the contributed click command, not for the core mara_config functionality
        'click'
    ],

    extras_require={
        'test': [
            'pytest'
        ],
    },

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

)
