
from cynpy.updprl import *

class csp (updprl):
    '''
    CC-ISP for can11xx
    '''

    def csp_prefix (me, txlst):
        '''
        send a UVDM for entering Mode 0
        and send the 'txlst' as a CSP command
        CRC32 will be turnned off
        '''
        err = me.msg_tx (15,[0x412a412a])
        if err == '':
#           msvcrt.getch()
            me.sfrwx (me.sfr.TXCTL,[0x28 | me.TxOrdrs]) # turn off CRC32
            me.sfrwx (me.sfr.FFSTA,[0x00]) # clear FIFO
            me.sfrwx (me.sfr.STA0, [0xff]) # clear STA0
            me.sfrwx (me.sfr.STA1, [0xff]) # clear STA1
            me.sfrwx (me.sfr.FFCTL,[0x40]); me.sfrwx (me.sfr.FFIO, txlst[:-1]) # first
            me.sfrwx (me.sfr.FFCTL,[0x80]); me.sfrwx (me.sfr.FFIO, txlst[-1:]) # last
            sta1 = me.sfrrx (me.sfr.STA1,1)[0]
            sta1 = me.sfrrx (me.sfr.STA1,1)[0]
            sta1 = me.sfrrx (me.sfr.STA1,1)[0] # a little delay make the extra data disapeared??
            
            if (sta1&0x30)==0x10: return ''
            else:                 return 'CSP cmd discardrd, 0x%02x' % (sta1)
        else:
            return err

        
    def probe (me, rpt=0):
        '''
        query each SOP* for searching responding target(s)
        '''
        me.prltx.msk (0xff, 0x08) # enable auto-RX-GoodCRC
        sav = me.TxOrdrs
        fnd = []
        for xx in range(1,6):
            me.TxOrdrs = xx
            ret = me.csp_prefix ([0x00,0x01]) # no-data CSP write
            if rpt:
                print me.OrdrsType[xx-1],
                if ret == '':
                    print 'responded'
                else:
                    print '...'
            if ret == '':
                fnd += [xx]

        me.prltx.pop ()
        me.TxOrdrs = sav
        return fnd


    def cspw (me, adr, io, wdat):
        assert len(wdat) > 0 and \
               len(wdat)+2 <= me.sfr.bufsz, 'invalid data size, %d' % (len(wdat))
        ret = me.csp_prefix ([adr, 0x01|((io&0x01)<<1)] + wdat)

        if ret != '':
            print ret
            return 0 # 0-byte written
        else:
            return len(wdat)


    def cspr (me, adr, io, cnt):
        assert cnt <= me.sfr.bufsz and cnt > 0, 'invalid read data count, %d' % (cnt)
        ret = []
        err = me.csp_prefix ([adr, 0x00|((io&0x01)<<1), cnt-1])
        if err == '': # continue to receive the CSP read data
            sta0 = 0
            for xx in range(20): # wait for something rcvd
                if sta0 & 0xfc: break;
                sta0 = me.sfrrx (me.sfr.STA0,1)[0] & 0xfe
            if sta0 == 0x12 or sta0 == 0x10: # why 0x10 ??
                staf = me.sfrrx (me.sfr.FFSTA,1)[0]
                if staf == 0x80:
                    print 'no CSP read data returned'
                else:
                    me.sfrwx (me.sfr.FFCTL,[0x40]) # first
                    ret = me.sfrrx (me.sfr.FFIO, cnt)
            elif sta0 == 0x00:
                print 'CSP read not responded'
            else:
                print 'CSP responds a bad data, 0x%02x' % (sta0)
        else: # print the error message during the UVDM
            print err

        return ret


        

if __name__ == '__main__':
    '''
    % python csp.py [cmd|SOP*] [cmd] [...]
    % python csp.py query
    % python csp.py 1 read bb
    '''
    import cynpy.i2c as i2c
    i2cmst = i2c.choose_i2cmst (rpt=i2c.FALSE)

    import sys
    import cynpy.basic as cmd
    if not cmd.no_argument ():
        if i2cmst != 0:
            if sys.argv[1]=='query' : # query SOP*
                cspbdg = csp(i2cmst, 0x70) # no SOP*
                print cspbdg.probe (1)
            else:
                if cmd.argv_hex[1]>0 and cmd.argv_hex[1]<=5: # assign SOP* by command line
                    cspbdg = csp(i2cmst, 0x70, cmd.argv_hex[1])
                    sys.argv = sys.argv[1:]
                    cmd.argv_hex = cmd.argv_hex[1:]
                    cmd.argv_dec = cmd.argv_dec[1:]
                else:
                    cspbdg = csp(i2cmst, 0x70, 5)

                cspbdg.prltx.msk (0xff, 0x08) # enable auto-RX-GoodCRC
                from cynpy.can11xx import tstcsp
                tstmst = tstcsp(cspbdg)
                cmd.tstmst_func (tstmst)
                cspbdg.prltx.pop ()
