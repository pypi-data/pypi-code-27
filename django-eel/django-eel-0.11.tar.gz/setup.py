import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                       os.pardir)))

requirements = [
    'django>=2.0.7',
    'channels>=2.1.2',
    'gevent>=1.3.4',
]

extras_require = {
    'test': [],
}

setup(
    name='django-eel',
    version='0.11',
    packages=find_packages(),
    #include_package_data=True, # comment this line to include `package_data`
    package_data={
        'django_eel': ['static/eel/js/eel.js'],
    },
    install_requires=requirements,
    extras_require=extras_require,
    license='MIT License',
    description='A Django App for little HTML GUI applications, with easy Python/JS interoperation.',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type="text/markdown",
    url='https://github.com/seLain/Django-Eel',
    download_url = 'https://github.com/seLain/Django-Eel/tarball/v0.1',
    keywords = ['gui', 'javascript', 'python', 'html', 'django'],
    author = 'Victor Hu',
    author_email='selain@nature.ee.ncku.edu.tw',
    zip_safe=False, # not being egg
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: MIT License'],
)