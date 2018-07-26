#!/usr/bin/env python

"""
    usage: regcomsrv [-h] [-u] [--unattended] [--quiet] [--debug] module classes [classes ...]

	positional arguments:
	    module            Module from that the COM-servers will be imported
	    classes           List of classes from specified module. This classes must implements COM-servers
	
	optional arguments:
	    -h, --help        show this help message and exit
	    -u, --unregister  For unregistering COM-servers
	    --unattended      See more at win32com.server.register
	    --quiet           See more at win32com.server.register
	    --debug           See more at win32com.server.register
"""

from regcomsrv import reg

if __name__ == '__main__':
	reg()