import sys
import webbrowser
from distutils.core import setup

trailer_url = 'https://ep2018.europython.eu/en/'
message = 'You should go to EuroPython!!'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    webbrowser.open_new(trailer_url)
    raise Exception(message)


if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)


setup(
    name='europython2018',
    version='0.0.1',
    maintainer='Thomas Grainger',
    maintainer_email='europython2018@graingert.co.uk',
    long_description=message,
    url=trailer_url,
)
