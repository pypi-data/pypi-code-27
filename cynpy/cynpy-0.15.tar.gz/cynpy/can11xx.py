
from cynpy.sfr import *

class can11xx (object):
    '''
    can11xx hierarchy
    -----------------                                     csp
                                                         /
                        sfr { sfrmst               updrpl - ams
                                            {i2c  /
            sfr1108                         cani2c - tsti2c
           /                               /        /
    sfr11xx - sfr111x - sfr1110  }  can11xx      atm 
                     \                     \        \
                      sfr1112                - - - - tstcsp
                                                       {csp
    '''
    def __init__ (me):
        me.sfr = sfr11xx() # initial
        if me.is_master_rdy():
            revid = me.get_revid ()
#           print 'master is ready', revid
            if revid > 0: # found
                if sfr1108().check (revid): me.sfr = sfr1108(revid)
                if sfr1110().check (revid): me.sfr = sfr1110(revid)
                if sfr1112().check (revid): me.sfr = sfr1112(revid)
#       else:
#           print 'master is not ready'


    def is_master_rdy (me): raise NotImplementedError()
    def sfrwx (me, adr, wdat): raise NotImplementedError() # NINC mode
    def sfrrx (me, adr, cnt): raise NotImplementedError() # NINC mode
    def sfrri (me, adr, cnt): raise NotImplementedError() # INC mode


    def get_revid (me):
        sav = me.sfrrx (me.sfr.DEC, 1) # try slave
        if len(sav): # data returned
            me.sfrwx (me.sfr.DEC, [me.sfr.REVID])
            revid = \
            me.sfrrx (me.sfr.REVID, 1)[0] & 0x7f
            me.sfrwx (me.sfr.DEC, [sav[0]])
            return revid
        return 0



class cani2c (can11xx):
    def __init__ (me, busmst, deva, rpt=0):
        me.deva = deva
        me.busmst = busmst # SFR master (I2C)
        can11xx.__init__ (me) # SFR target

        if me.sfr.revid:
            if rpt:
                print 'I2C master finds %s, 0x%02x' % (me.sfr.name, me.deva)
            if me.sfr.inc == 1: # CAN1108/11
                me.sfrwx (me.sfr.I2CCTL, [me.sfrrx (me.sfr.I2CCTL,1)[0] | 0x01]) # we'll work in NINC mode


    def is_master_rdy (me):
        ''' Is this master ready for issuing things?
        '''
        return TRUE if me.busmst else FALSE


    def sfrwx (me, adr, wdat):
        return me.busmst.write (me.deva, adr, wdat)


    def sfrrx (me, adr, cnt):
        return me.busmst.read (me.deva, adr, cnt, FALSE)


    def sfrri (me, adr, cnt):
        sav = me.sfrrx (me.sfr.I2CCTL, 1)[0]
        setinc = sav & 0xfe if me.sfr.inc else sav | 0x01
        me.sfrwx (me.sfr.I2CCTL, [setinc]) # INC mode
        rdat = me.busmst.read (me.deva, adr, cnt, TRUE)
        me.sfrwx (me.sfr.I2CCTL, [sav])
        return rdat



from cynpy.atm import *

class tsti2c (cani2c, atm):
    pass


class tstcsp (can11xx, atm):
    def __init__ (me, busmst, rpt=0):
        me.busmst = busmst # SFR master (CSP)
        super(me.__class__, me).__init__ () # SFR target

        if me.sfr.revid and rpt:
            print 'CSP master finds %s, %d' % (me.sfr.name, me.busmst.TxOrdrs)


    def is_master_rdy (me):
        ''' Is this master ready for issuing things?
        '''
        return me.busmst.busmst.handle


    def sfrwx (me, adr, wdat):
        return me.busmst.cspw (adr, 1, wdat)


    def sfrrx (me, adr, cnt):
        return me.busmst.cspr (adr, 1, cnt)


    def sfrri (me, adr, cnt):
        return me.busmst.cspr (adr, 0, cnt)


    def insert_dummy (me, rawcod, block):
        '''
        load the memory file 'memfile' and insert dummys
        '''
        lowcod = [] # low-byte
        wrcod = []
        for xx in rawcod:                
            if len(lowcod)>0 or me.sfr.nbyte==1:
                if len(wrcod)%block > 0:
                    for yy in range(me.sfr.dummy):
                        wrcod += [0xdd]
                wrcod += lowcod + [xx]
                lowcod = []
            else:
                lowcod = [xx]

        return (len(rawcod), wrcod)


    def nvm_prog_block (me, addr, wrcod, rawsz, hiv=0):
        """
        override atm's method
        calc. block length
        insert dummy byte(s)
        """
        w_unit = (me.sfr.bufsz - me.sfr.nbyte - 2) \
                              / (me.sfr.nbyte + me.sfr.dummy) # CSP command needs 2 bytes
        block = (me.sfr.nbyte + me.sfr.dummy) * w_unit \
               + me.sfr.nbyte # optimize block size by CSP buffer

        (rawsz, dmycod) = me.insert_dummy (wrcod, block)
        super(me.__class__, me).nvm_prog_block (addr, dmycod, rawsz, hiv, block)


    def nvm_comp_block (me, args, block=32):
        '''
        limit block size by CSP buffer
        '''
        super(me.__class__, me).nvm_comp_block (args, block)



class sfr (object):
    """
    to monitor I2C/CSP register
    to save read/modify time on communication channel
    """

    def __init__ (me, sfrmst, port, val=-1, dbmsg=FALSE):
        me.p = port # port/address
        me.v = [0] # one element for recovering
        me.sfrmst = sfrmst
        me.d = dbmsg
        if val<0: me.v[0] = me.sfrmst.sfrrx (port, 1)[0] # initial condition
        else:     me.v[0] = val                          # power-on value

    def __del__ (me):
        '''
        DIFFICULT TO CONTROL THIS
        SO THIS RECOVERY FUNCTION DOESN'T WORK YET
        '''
#       me.set (me, me.v[0])
        print 'SFR.%02X died' % (me.p)

    def doit (me):
        me.sfrmst.sfrwx (me.p, [me.v[-1]]) # main job of this class
        if me.d:
            print 'SFR.%02X: %02X, [' % (me.p,me.v[-1]), \
                  '%02X ' * len(me.v) % tuple(me.v)

    def get (me): return me.v[-1]

    def set (me, val, force=FALSE): # to set without push
        assert val==(val&0xff), '"val" out of range'
        chk = me.v[-1] != val
        me.v[-1] = val 
        if force or chk:
            me.doit ()

    def psh (me, val=-1, force=FALSE):
        if val<0:
            me.v += [ me.v[-1] ] # duplicate
        else:
            assert val==(val&0xff), '"val" out of range'
            me.v += [ val ] # push
            if force or me.v[-1] != me.v[-2]:
                me.doit ()

    def pop (me, force=FALSE): # resume
        tmp = me.v.pop ()
        if force or me.v[-1] != tmp:
            me.doit ()

    def msk (me, a, o=0):
        me.psh ((me.v[-1] & a) | o)



if __name__ == '__main__':
    '''
    % python can11xx.py [cmd] [argv2] [...]
    % python can11xx.py rev
    % python can11xx.py write bc 8
    '''
    import cynpy.i2c as i2c
    i2cmst = i2c.choose_i2cmst (rpt=i2c.FALSE)
    tstmst = tsti2c(busmst=i2cmst, deva=0x70)

    import cynpy.basic as cmd
    if not cmd.no_argument ():
        if i2cmst!=0:
            cmd.tstmst_func (tstmst)
