#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms_lite.utils.settings_manager import conf

conf += 'pyforms_lite.settings'

__author__ 		= "Ricardo Ribeiro"
__credits__ 	= ["Ricardo Ribeiro"]
__license__ 	= "MIT"
__version__ 	= '3.0.1'
__maintainer__ 	= ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ 		= ["ricardojvr@gmail.com", "cajomferro@gmail.com"]
__status__ 		= "Production"

from pyforms_lite.gui import controls
from pyforms_lite.gui.basewidget import BaseWidget
from pyforms_lite.gui.appmanager import start_app
from pyforms_lite.gui.basewidget import vsplitter, hsplitter
