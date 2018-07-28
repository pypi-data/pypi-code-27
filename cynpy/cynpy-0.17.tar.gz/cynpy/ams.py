
from cynpy.updprl import *

class ams (updprl):
    '''
    Atomic Message Sequence
    1. auto-respond
    2. initiator
    Note:
    a. enable auto-TX/RX-GoodCRC during TX/RX
    b. via AARDVARK (USB-I2C bridge) on virtual machine doesn't work
    '''

    def __init__ (me, i2cmst, deva, check_kb_func, ordrs=0):
        super(ams,me).__init__ (i2cmst, deva, ordrs)
        me.check_kb_func = check_kb_func

        me.pdo = []
        me.rdo = 0

        me.str = '' # command string
        me.kb = ord('1') # command from keyboard
        me.mode = 0 # 0/1/2 : RX/TX/PPS
        me.ppstime = 0
        me.SpecRev = 2 # PD_R3


    def ams_quick_tx_than_wait (me, cmd, do=[]):
        me.sfrwx (me.sfr.STA0, [0xff]) # clear STA0, prepare for the 1st 'quick' upd_rx
        me.sfrwx (me.sfr.STA1, [0xff]) # clear STA1
        me.msg_tx (cmd, do)

        msg = 'TX - %02X%02X' % (me.TxBuffer[1],me.TxBuffer[0]) \
                                          + (':' if len(do) > 0 else '')
        for yy in range(len(do)): # NDO
            msg += ' %08X' % do[yy]
        print '%s (%s)' % (msg, me.DataMsg[cmd] if len(do) > 0 else me.CtrlMsg[cmd])

        return me.upd_rx (quick=1)


    def pps_request (me, cmd):
        '''
        with a command or a target voltage
        don't check voltage range for stressing DUT
        '''
        pos_minus = (me.rdo >> 28) & 0x07 - 1
        ppscur = (me.rdo >> 9) & 0x7ff
        me.rdo &= ~0x000ffe00
#       ppsmax = ((me.pdo[pos_minus] >> 17) & 0x7f) * 5 # 20mV
#       ppsmin = ((me.pdo[pos_minus] >> 8)  & 0x7f) * 5 # 20mV

        if len(cmd) == 1:
            if   cmd[0] == '+':
                me.rdo |= (ppscur + 1) << 9
            elif cmd[0] == '-':
                me.rdo |= (ppscur - 1) << 9
            elif cmd[0] == '*':
                me.rdo |= ppscur << 9
        if len(cmd) > 1:
            ppsv = cmd.split('=')[-1]
            if ppsv.isdigit():
                me.rdo |= (int(ppsv) / 20) << 9

        if me.rdo & 0x000ffe00: # target voltage is valid
            (ndo,mtyp,do) = me.ams_quick_tx_than_wait (2, [me.rdo])
            if me.ppstime > 0:
                me.ppstime = 0
            if (ndo,mtyp) == (0,3): # Accept
                me.upd_rx () # PS_RDY


    def ams_request (me):
        '''
        '''
        pos_minus = (me.kb - ord('1')) & 0x07
        me.rdo = (pos_minus+1) << 28
        ret = (FALSE,FALSE) # not a APDO, not accepted

        if len(me.pdo) > pos_minus:
            if (me.pdo[pos_minus] >> 30) == 3: # APDO, max voltage
                ret = (TRUE,ret[1])
                ppsmax = ((me.pdo[pos_minus] >> 17) & 0x7f) * 5 # 20mV
                me.rdo |= ((ppsmax & 0x7ff) << 9) | (me.pdo[pos_minus] & 0x7f)
            else:
                me.rdo |= me.pdo[pos_minus] & 0x3ff | ((me.pdo[pos_minus] & 0x3ff) << 10)

        (ndo,mtyp,do) = me.ams_quick_tx_than_wait (2, [me.rdo])
        if (ndo,mtyp) == (0,3): # Accept
            ret = (ret[0],TRUE)
            me.upd_rx () # PS_RDY

        return ret


    def ams_get_source_cap (me):
        '''
        '''
        (ndo,mtyp,do) = me.ams_quick_tx_than_wait (7)
        if ndo > 0 and mtyp == 1: # SourceCap
            me.pdo = do
            if me.ams_request () == (TRUE,TRUE): # a APDO accepted
                me.mode = 2
                print '[AMS_PPS]'


    def ams_tx (me):
        '''
        '''
        key = me.check_kb_func ()
        if key == ord('q'): # 'q'
            me.mode = 0
            print '[AMS_RX]'

        elif key == ord('g'): # Get_Source_Cap
            me.ams_get_source_cap ()

        elif key >= ord('0') and key <= ord('7'): # Request
            me.kb = key
            if me.ams_request () == (TRUE,TRUE): # a APDO accepted
                me.mode = 2
                print '[AMS_PPS]'

        elif key > 0:
            me.kb = key


    def ams_pps (me, sleep_func):
        '''
        '''
        if me.ppstime >= 0:
            me.ppstime += 1
        sleep_func (0.01)
        if me.ppstime == 666: # about 10 sec
            me.pps_request ('*') # reset me.ppstime in this

        key = me.check_kb_func ()
        if me.str == '':
            if key == ord('q'): # 'q'
                me.mode = 0
                print '[AMS_RX]'
            elif key == ord('+') or \
                 key == ord('-') or \
                 key == ord('*'): # inc/dec/same
                me.pps_request (chr(key))
            elif key == ord('/'): # switch SinkPPSPeriodTimer
                me.ppstime = 0 if me.ppstime < 0 else -1
                print 'switch SinkPPSPeriodTimer', 'ON' if me.ppstime == 0 else 'OFF'
            elif key == ord('='): # set new voltage
                me.str = '='
                print me.str, '\x0D',

            elif key >= ord('0') and key <= ord('7'): # Request
                me.kb = key
                if me.ams_request () == (FALSE,TRUE): # a PDO accepted
                    me.mode = 1
                    print '[AMS_TX]'

            elif key > 0:
                me.kb = key

        else:
            if key == 13: # press 'enter' to exec 'me.str'
                print me.str
                me.pps_request (me.str)
                me.str = '' # reset 'me.str'
            elif key > ord(' '):
                me.str += chr(key)
                print me.str, '\x0D',


    def ams_rx (me):
        '''
        get/decode RX a message, respond if needed
        '''
        (ndo,mtyp,do) = me.upd_rx ()
        if ndo > 0: # data message
            if mtyp == 1: # SourceCap
                me.pdo = do
                if me.ams_request () == (TRUE,TRUE): # a APDO accepted
                    me.mode = 2
                    print '[AMS_PPS]'
                
        elif ndo == 0: # control message
            if mtyp < 0: # Hard/Cable Reset
                print 'RX -', me.OrdrsType[mtyp+7]

        else: # 'q' pressed
            me.mode = 1
            print '[AMS_TX]'


    def upd_rx (me, quick=0):
        '''
        wait for an auto-TX-GoodCRC sent, then,
        get STA0, get FFSTA, get RX data all take time
        if another RX arrive during these, those data is corrupted
        quick=1 to not clear STA* for a new message may have arrived
            (TX caller is responsible for clearing the STA*)
        '''
        me.prltx.msk (0xff, 0x80) # enable auto-TX-GoodCRC
        if quick == 0:
            me.sfrwx (me.sfr.STA0, [0xff]) # clear STA0
            me.sfrwx (me.sfr.STA1, [0xff]) # clear STA1
        (sta0,sta1) = (0,0)
        (ndo,mtyp,do,key) = (0,0,[],0)
        while not (sta1 & 0x40) and \
              not (sta0 & 0x80):
            sta0 = me.sfrrx (me.sfr.STA0,1)[0]
            sta1 = me.sfrrx (me.sfr.STA1,1)[0]
            key = me.check_kb_func ()
            if key > 0: # key pressed
                if key >= ord('0') and key <= ord('7'):
                    me.kb = key
                    print chr(key) # this 'kb' will effect the next Nego
                elif key == ord('q'):
                    ndo = -1
                    break
                else:
                    me.kb = key # save the 'kb' for main loop usage

        if not ndo < 0: # not break

            if sta1 & 0x40: # auto-TX-GoodCRC sent
                ffcnt = me.sfrrx (me.sfr.FFSTA,1)[0] & 0x3f
                assert ffcnt > 0, 'empty FIFO received'

                me.sfrwx (me.sfr.FFCTL, [0x40]) # first
                rdat = me.sfrrx (me.sfr.FFIO, ffcnt)
                assert ffcnt == len(rdat), 'FIFO read error'

                ndo = (rdat[1] >> 4) & 0x07
                mtyp = rdat[0] & 0x1f
                do = [0] * ndo
                msg = 'RX - %02X%02X' % (rdat[1],rdat[0]) + (':' if ndo > 0 else '')
                for yy in range(ndo):
                    for xx in range(4):
                        do[yy] += rdat[yy*4+2+xx]*(256**xx)
                    msg += ' %08X' % do[yy]
                print msg

            else: # Hard/Cable Reset rcvd
                prls = me.sfrrx (me.sfr.PRLS,1)[0] & 0x70
                if   prls == 0x60: mtyp = -2 # Hard Reset
                elif prls == 0x70: mtyp = -1 # Cable Reset
                else:
                    raise NameError('not recognized ordered set')

        me.prltx.pop () # recover PRLTX settings
        return (ndo,mtyp,do)



if __name__ == '__main__':
    '''
    % python ams.py
    '''
    import cynpy.i2c as i2c
    i2cmst = i2c.choose_i2cmst (rpt=i2c.FALSE)

    import time as time
    import cynpy.basic as cmd
    if i2cmst != 0:
        tstmst = ams(i2cmst, 0x70, cmd.check_break, 1)

        '''
        enable auto-TX/RX-GoodCRC
        recover auto-TX/RX-GoodCRC setting
        '''
        tstmst.prltx.msk (0xff, 0x88) # enable auto-TX/RX-GoodCRC
        print '[AMS_RX]'
        while tstmst.kb != 27:
            if   tstmst.mode == 0: tstmst.ams_rx ()
            elif tstmst.mode == 1: tstmst.ams_tx ()
            elif tstmst.mode == 2: tstmst.ams_pps (time.sleep)

            if tstmst.kb == ord(' '): # toogle PD2/3
                tstmst.kb = ord('1') # reset/clear 'kb'
                tstmst.SpecRev = 3 - tstmst.SpecRev
                print '[PD%d0]' % (tstmst.SpecRev + 1)

        tstmst.prltx.pop () # recover PRLTX settings
