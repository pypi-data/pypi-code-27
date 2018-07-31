import logging
from cliparser._version import __version__ as version
import pipdate


logging.basicConfig(format='%(message)s', level=logging.INFO)
def checkforupdate():
    print("You are now using version: {}".format(version))
    update = pipdate.check('accoladecli', version)
    if update is not "":
        print('\n')
        logging.info( 'This version of accoladecli is outdated. Re-install by typing "pip install accoladecli --upgrade" on command line!')
        print('\n')
