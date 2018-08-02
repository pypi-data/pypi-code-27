#!/usr/bin/env python
# coding=utf-8

import sys; sys.path.extend(['/autofs/nccs-svm1_home1/kennedy/EVE/eve/'])
import ks

jf = ks.json_file('ks.json')
config = jf['default_v_fast']

cargs = []; [cargs.extend([str('--'+key), str(val)]) for key, val in config.items() if key != 'config']
args = ks.parse_args(cargs)
