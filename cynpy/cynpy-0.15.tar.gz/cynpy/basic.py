
TRUE  = 1 # ACK, YES, success
FALSE = 0 # NAK, NO,  failed

import sys, string

global argv_hex, argv_dec
argv_hex = []
argv_dec = []
for xx in sys.argv:
    if len(xx) > 0:
        argv_hex += [int(xx,16)] if all (yy in '+-*/^%' + string.hexdigits for yy in xx) else [xx]
        argv_dec += [int(xx,10)] if all (yy in '+-*/^%' + string.digits    for yy in xx) else [xx]


def no_argument ():
    if len(sys.argv) < 2:
        f = open (sys.argv[0],'r')
        cmd = ''
        for line in f:
            if line.find ('line')<0 and line.find ('sys.argv[')>=0 and line.find (']==')>0:
                print line,
            if line.find ('line')<0 and line.find ('% python')>=0:
                cmd += '\n' + ' '.join(line.split()[0:])
            if line.find ('line')<0 and line.find ('tstmst_func')>=0:
                basic_path = '\\'.join(sys.argv[0].split('\\')[0:-1]) + '\\basic.py'
                for gg in open (basic_path,'r'):
                    if gg.find ('line')<0 and gg.find ('sys.argv[')>=0 and gg.find (']==')>0:
                        print gg,

        print 'ex:',
        print cmd if len(cmd) else '\n% '+sys.argv[0]
        f.close ()
        return TRUE
    else:
        return FALSE


def tstmst_func (tstmst):
    if   sys.argv[1]=='rev'   : print tstmst.sfr.name
    elif sys.argv[1]=='sfr'   : print tstmst.sfr.get_sfr_name (argv_hex[2])
    elif sys.argv[1]=='adc'   : print tstmst.get_adc10 (argv_hex[2])
    elif sys.argv[1]=='wrx'   : print tstmst.sfrwx (argv_hex[2],argv_hex[3:])
    elif sys.argv[1]=='write' : print tstmst.sfrwx (argv_hex[2],[argv_hex[3]])
    elif sys.argv[1]=='read'  : print '0x%02x' % tstmst.sfrrx (argv_hex[2],1)[0]
    elif sys.argv[1]=='loopr' : tstmst.loopr (100,sys.argv[2:])
    elif sys.argv[1]=='loopw' : tstmst.loopw (100,sys.argv[2:])

    elif sys.argv[1]=='dump'  :
        if len(sys.argv)==2:    tstmst.sfr_form (0x80,0x80)
        else:                   tstmst.sfr_form (argv_hex[2],argv_hex[3])
    elif sys.argv[1]=='nvm'   :
        if len(sys.argv)==2:    tstmst.nvm_form (0x900,0x80)
        else:                   tstmst.nvm_form (argv_hex[2],argv_hex[3])

    elif sys.argv[1]=='stop'  : print tstmst.sfrwx (0xBC,[8]) # stop MCU
    elif sys.argv[1]=='reset' : print tstmst.sfrwx (0xF7,[1,1,1]) # reset MCU
    elif sys.argv[1]=='trim'  : print ['0x%02x' % xx for xx in tstmst.get_trim ()]

    elif sys.argv[1]=='prog_hex'  : tstmst.nvm_prog (argv_hex[3],argv_hex[4:],argv_hex[2])
    elif sys.argv[1]=='prog_asc'  : tstmst.nvm_prog (argv_hex[3],map(ord,list(sys.argv[4])),argv_hex[2])
    elif sys.argv[1]=='prog_str'  : tstmst.nvm_prog_block ( \
                                                     argv_hex[3],map(ord,list(sys.argv[4])),len(sys.argv[4]),argv_hex[2])
    elif sys.argv[1]=='upload'    : tstmst.nvm_upload_block (sys.argv[2],argv_hex[3])
    elif sys.argv[1]=='comp'      : tstmst.nvm_comp_block (sys.argv[2:])
    elif sys.argv[1]=='test'      : tstmst.test ()
    else: print "command not recognized,", sys.argv[1]



import os
if os.name=="nt": # if not, the loop won't break by keyboard
    import msvcrt

    def check_break ():
        if os.name=="nt" and msvcrt.kbhit():
            return ord(msvcrt.getch())
        else:
            return FALSE
