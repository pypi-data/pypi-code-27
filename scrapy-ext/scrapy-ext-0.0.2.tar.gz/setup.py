from setuptools import setup, find_packages


def get_req_list(req_file):
    """
    Parse requirements file and return list iof requrements for setuptools
    :param req_file: file_pointer
    :return: list of requirements
    """
    ret = []
    with open(req_file) as rf:
        for l in rf.readlines():
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            ret.append(l)
    return ret


setup_requires = [
    'setuptools_scm',
    'wheel',
]

# install_requires = get_req_list('requirements/base.pip')
# tests_require = get_req_list('requirements/test.pip')


setup(
    name='scrapy-ext',
    author='Vitek Pliska',
    author_email='vitek@creatiweb.cz',
    description='Useful Scrapy extensions',
    url='https://creatiweb.cz',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    use_scm_version=True,
    setup_requires=setup_requires,
    # install_requires=install_requires,
    # tests_require=tests_require,
)
