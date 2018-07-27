import site, os
from distutils.core import setup

setup(
    name = 'guider',
    version = '3.9.beta3',
    license = 'GPL2',
    description = 'A system-wide analyzer of performance',
    author = 'Peace Lee',
    author_email = 'iipeace5@gmail.com',
    url = 'https://github.com/iipeace/guider',
    download_url = 'https://github.com/iipeace/guider/archive/master.zip',
    keywords = ['guider', 'linux', 'analyzer', 'performance', 'profile', 'trace', 'kernel'],
    packages = ['guider'],
    data_files=[('/usr/sbin', ['guider/guider'])],
    classifiers = [],
)

try:
    os.mkdir('/usr/share/guider')
except:
    pass

for path in site.getsitepackages():
    try:
        pycPath = '/usr/share/guider/guider.pyc'
        pycOrig = '%s/guider/guider.pyc' % path

        if os.isfile(pycPath):
            os.remove(pycPath)

        if sys.version_info >= (3,0):
            cachedPycDir = '%s/guider/__pycache__/' % path
            for cache in os.listdir(cachedPycDir):
                os.rename('%s%s' % (cachedPycDir, cache), pycOrig)

        os.symlink(pycOrig, pycPath)
    except:
        pass
    try:
        shPath = '/usr/sbin/guider'

        if os.isfile(shPath):
            os.remove(shPath)

        os.symlink('%s/guider/usr/sbin/guider' % path, shPath)
    except:
        pass

'''
upload command
    # python setup.py sdist upload -r pypitest
    # python setup.py sdist upload -r https://upload.pypi.org/legacy/
'''

