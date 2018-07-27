
import random
import time

from cynpy.basic import check_break

class atm (object):
    '''
    purely a method-only object
    for those SFR master, sfri2c and sfrcsp
    '''

    def sfr_form (me, adr, cnt=16):
        print me.sfrri, adr
        print 'sfr_dump: 0x%02x 0x%02x' % (adr,cnt)
        if ((adr&0x0f)+cnt<=16 and cnt<=8): # in one line
            print '0x%02x:' % adr,
            r_dat = me.sfrri (adr,cnt)
            assert len(r_dat)==cnt, 'sfr read failed'
            for i in range(cnt): print '%02x' % r_dat[i],
        else:
            pos = adr&0x0f
            for ali in range(adr&0xf0,(adr+cnt+15)&0x1f0,0x10):
                print '0x%02x:' % ali,
                r_dat = me.sfrri (ali,16-pos)
                assert len(r_dat)==(16-pos), 'sfr read failed'
                for i in range(0x10):
                    if (i&0x07==0 and i>0): print ' ',
                    if (ali+i<adr or ali+i>=adr+cnt): print '..',
                    else: print '%02x' % r_dat[i-pos],
                print
                pos = 0


    def nvmset (me, ofs):
        assert me.sfrrx (me.sfr.MISC,1)[0] & 0x08, 'MCU is runnung'
        msk = me.sfr.nvmmsk
        me.sfrwx (me.sfr.OFS, [(ofs&msk)&0xff]) # OTP offset [7:0]
        me.sfrwx (me.sfr.DEC, [((ofs&msk)|(0xa000&~msk))>>8]) # OTP offset [??:8], ACK for OTP access


    def nvmrx (me, cnt): # NINC mode
        ret = me.sfrrx (me.sfr.NVMIO, cnt)
        assert len(ret)==cnt, 'NVM read failed'
        return ret


    def nvm_form (me, ofs, cnt):
        assert ofs>=0 and cnt>0 and (ofs+cnt)<=me.sfr.nvmsz, 'out of range'
        print 'remember to halt MCU in advance'
        me.nvmset (ofs)
        if ((ofs&0x0f)+cnt<=16 and cnt<=8): # in one line
            print '0x%04x:' % ofs,
            r_dat = me.nvmrx (cnt)
            for i in range(cnt): print '%02x' % r_dat[i],
            print
        else:
            print 'nvm_form: 0x%04x, %0d' %(ofs,cnt)
            s_pos = ofs&0x0f
            lines = range(ofs&0xfff0,(ofs+cnt+15)&0xfff0,0x10)
            e_pos = 0x0f & (cnt - (16-s_pos))
            for ali in lines:
                print '0x%04x:' % (ali&0x7fff),
                if ali==lines[-1] and e_pos: num = e_pos
                else: num = 16-s_pos
                r_dat = me.nvmrx (num)
                for i in range(0x10):
                    if (i&0x07==0 and i>0): print ' ',
                    if (ali+i<ofs or ali+i>=ofs+cnt): print '..',
                    else: print '%02x' % r_dat[i-s_pos],
                endstr = '  '
                for i in range(0x10):
                    if (ali+i<ofs or ali+i>=ofs+cnt or
                        r_dat[i-s_pos]<ord(' ') or r_dat[i-s_pos]>ord('~')): endstr += '.'
                    else: endstr += chr(r_dat[i-s_pos])
                print endstr
                s_pos = 0
        me.sfrwx (me.sfr.DEC, [(ofs+cnt)>>8])


    def loopr (me, period, plist): # looped read and print
        if (len(plist)>0):
            print me.sfrrx
            print 'looped read, press any key.....'
            cnt = 0
            while 1:
                print "\r%0d:" % cnt,
                for xx in range (len(plist)):
                    try:
                        r_dat = me.sfrrx (int(plist[xx],16),1)[0]
                        print " %02x: %02x" %(int(plist[xx],16),r_dat),
                        cnt += 1
                    except:
                        print " %02x: --" %(int(plist[xx],16)),
                if check_break (): break


    def loopw (me, period, plist): # looped write/read test
        if (len(plist[0])>0):
            print me.sfrwx
            print 'looped write/read test, press any key.....'
            cnt = 0
            while 1:
                print "\r%0d:" % cnt,
                for xx in range (len(plist)):
                    wdat = random.randint(0,255)
                    me.sfrwx (int(plist[xx],16), [wdat]);
                    print " %02x: %02x" % (int(plist[xx],16),wdat),
                    r_dat = me.sfrrx (int(plist[xx],16),1)[0]
                    if r_dat!=wdat:
                        print " failed: %02x returned" % (r_dat)
                        exit (-1)
                if check_break (): break
                cnt += 1


    def preset_adc (me):
        me.sfrwx (me.sfr.DACLSB,[0x06]) # enable DAC1/COMP
        me.sfrwx (me.sfr.DACCTL,[0x00])
        me.sfrwx (me.sfr.SAREN, [0xff])

    def get_adc8 (me, chn): # multiple channel
        me.preset_adc ()
        me.sfrwx (me.sfr.DACEN, [chn])
        me.sfrwx (me.sfr.DACCTL,[0x0d]) # 8-bit once
        ret = []
        msk = 0x01
        for xx in range(8):
            if chn & (msk<<xx):
                ret += [8 * me.sfrrx (me.sfr.DACV0 + xx, 1)[0]] # mV
        return ret

    def get_adc10 (me, chn): # single channel
        me.preset_adc ()
        me.sfrwx (me.sfr.DACEN, [0x01 << chn])
        me.sfrwx (me.sfr.DACCTL,[0x4d]) # 10-bit once (not stable)
##        print \
##            2 * (4 * me.sfrrx (me.sfr.DACV0 + chn, 1)[0] \
##                  + (me.sfrrx (me.sfr.DACLSB, 1)[0] & 0x03)),
        me.sfrwx (me.sfr.DACCTL,[0x4f]) # 10-bit loop
        me.sfrwx (me.sfr.DACCTL,[0x00])
        return \
            2 * (4 * me.sfrrx (me.sfr.DACV0 + chn, 1)[0] \
                  + (me.sfrrx (me.sfr.DACLSB, 1)[0] & 0x03))


    def pre_prog (me, hiv=0): # provide high voltage
        assert hiv==0 or hiv==1, 'error argument, hiv'
        if me.sfr.name=='CAN1108' or \
           me.sfr.name=='CAN1111':
            rlst = []
            print 'Please provide VPP (6.5V) on VC1'
        else:
            rlst = \
                me.sfrrx (me.sfr.PWR_V,1) + \
                me.sfrrx (me.sfr.SRCCTL,1) # save PWR_V
            if hiv > 0: # hiv=0 to emulate
                me.sfrwx (me.sfr.PWR_V, [125]) # set VIN=10V

            print 'pre-VIN:',
            for xx in range(3):
                print '%5.2f' % (10.0 * me.get_adc10 (0) / 1000),
            print 'mV'

            me.sfrwx (me.sfr.SRCCTL, [rlst[1] | 0x40]) # set HVLDO high voltage

            if me.sfr.name.find ('CAN1110')==0:
                me.sfrwx (me.sfr.NVMCTL, [0x10,0x12,0x32]) # set VPP,TM,PROG

        return rlst


    def pst_prog (me, rlst): # resume 5V
        if not \
          (me.sfr.name=='CAN1108' or \
           me.sfr.name=='CAN1111'):
            if me.sfr.name.find ('CAN1110')==0:
                me.sfrwx (me.sfr.NVMCTL, [0x12,0x10,0x00]) # clr PROG,TM,VPP
            me.sfrwx (me.sfr.SRCCTL, [rlst[1] &~0x40]) # recover V5 (HVLDO)

            print 'pos-VIN:',
            print '%5.2f' % (10.0 * me.get_adc10 (0) / 1000),
            me.sfrwx (me.sfr.PWR_V, [rlst[0]]) # recover VIN
            for xx in range(3):
                print '%5.2f' % (10.0 * me.get_adc10 (0) / 1000),
            print 'mV'


    def nvm_prog (me, adr, wlst, hiv=0): # hiv=0 to emulate
        """
        program @adr those in list 'wlst' byte-by-byte
        slowly write for PROG timing
        """
        me.nvmset (adr)
        rlst = me.pre_prog (hiv)
        for xx in range(len(wlst)):
            me.sfrwx (me.sfr.NVMIO, [wlst[xx]])
        me.pst_prog (rlst)
        sav = me.sfrrx (me.sfr.DEC, 1)[0]
        me.sfrwx (me.sfr.DEC, [(me.sfr.nvmmsk >> 8) & sav]) # clear ACK


    def test (me):
        pass


    def get_file (me, memfile):
        """
        load file and return the array with byte-by-byte format
        """
        print memfile
        f = 0
        lines = []
        if memfile[-4:].lower() == '.bin':
            f = open (memfile,'rb')
            lines = map(ord,list(f.read()))
        elif memfile[-7:].lower() == '.1.memh' or \
             memfile[-7:].lower() == '.2.memh':
            f = open (memfile,'r')
            for xx in f.readlines ():
                text = xx.split()[0] # only the 1st word
                if text != '': # ignore empty
                    assert len(text) == 2 * me.sfr.nbyte, \
                           'invalid format for %s' % (me.sfr.name)
                    if me.sfr.nbyte == 2:
                        lines.append (int(text[2:4],16))
                    lines.append (int(text[0:2],16))
        else:
            print 'ERROR: file format'

        print '%d (0x%04x) byte(s)' % (len(lines),len(lines))

        rem = len(lines) % me.sfr.nbyte
        if rem > 0:
            print 'append 0xFF for programming unit,', me.sfr.nbyte - rem
            for xx in range(me.sfr.nbyte - rem):
                lines.append (0xff)

        return lines


    def nvm_prog_block (me, addr, wrcod, rawsz, hiv=0, block=256):
        """
        program the byte-by-byte array 'wrcod' in to the NVM block-by-block
        SFR-by-CSP: limit block size by CSP buffer and dummy
        SFR-by-I2C: 100KHz write for PROG timing
        """
        assert block > 0, 'block size must be positive'
        me.nvmset (addr)
        rlst = me.pre_prog (hiv)
        start = time.time ()

        for xx in range(0, len(wrcod), block):
            wcnt = block if xx+block <= len(wrcod) else len(wrcod)-xx
            me.sfrwx (me.sfr.NVMIO, wrcod[xx:xx+wcnt])

        print "%.1f sec" % (time.time () - start)
        me.pst_prog (rlst)
        ofs = me.sfrrx (me.sfr.OFS, 1)[0]
        dec = me.sfrrx (me.sfr.DEC, 1)[0]
        endadr = (ofs+dec*256) & me.sfr.nvmmsk
        me.sfrwx (me.sfr.DEC, [endadr>>8]) # clear ACK

        print ('ERROR: 0x%04x' % (endadr)) if endadr != addr + rawsz else 'complete'


    def nvm_upload_block (me, memfile, hiv=0):
        """
        load the memory file 'memfile' for uploading to NVM
        """
        wrcod = me.get_file (memfile)
        me.nvm_prog_block (0, wrcod, len(wrcod), hiv)


    def show_mismatch (me, adr, dat, exp, num, limit=32):
        """
        for counting number of mismatch
        and show mismatch messages
        """
        if num  < limit: print '0x%04X : %02X (!=%02X)' % (adr, dat, exp)
        if num == limit: print 'further mismatch(es) will be suppressed',
        return 1


    def nvm_chk_blank (me, start, end, mismatch, block=256): # the byte 'end' is not compared
        """
        check if those contents are all '1' block-by-block
        """
        print 'blank check from 0x%04x to 0x%04x' % (start, end),
        me.nvmset (start)
        while start < end:
            rcnt = block if start+block <= end else end-start
            rdat = me.nvmrx (rcnt)
            for yy in range(len(rdat)):
                if rdat[yy] != 0xff:
                    mismatch += me.show_mismatch (start+yy, rdat[yy], 0xff, mismatch)
            start += rcnt
        return mismatch


    def nvm_comp_block (me, args, block=256):
        print 'compare contents to',
        expcod = me.get_file (args[0]) # memfile
        if len(args) > 1: # exception(s)
            for it in args[1:]:
                [adr_h, text] = it.split('=')
                adr = int(adr_h,16)
                if text[0]=='\\':
                    expcod[adr] = int(text[1:],16)
                else:
                    for tt in range(len(text)):
                        if adr+tt < len(expcod):
                            expcod[adr+tt] = ord(text[tt])
        mismatch = 0
        me.nvmset (0)
        start = time.time ()
        for xx in range(0,len(expcod),block):
            rcnt = block if xx+block <= len(expcod) else len(expcod)-xx
            rdat = me.nvmrx (rcnt)
            for yy in range(len(rdat)):
                if rdat[yy] != expcod[yy+xx]:
                    mismatch += me.show_mismatch (yy+xx, rdat[yy], expcod[yy+xx], mismatch)

#       mismatch = me.nvm_chk_blank (xx + rcnt, me.sfr.nvmsz, mismatch, block)

        print '%.1f sec' % (time.time () - start)
        ofs = me.sfrrx (me.sfr.OFS, 1)[0]
        dec = me.sfrrx (me.sfr.DEC, 1)[0]
        endadr = (ofs+dec*256) & me.sfr.nvmmsk
        me.sfrwx (me.sfr.DEC, [endadr>>8]) # clear ACK

        print ('mismatch: %s' % (mismatch)) if mismatch else 'complete'


    def get_trim (me):
        '''
        search the trim MTTable
        get the newest entry
        '''
        me.nvmset (0x940)
        ret = []
        rdat = me.nvmrx (me.sfr.trimsz *me.sfr.trimnum)
        for xx in range(me.sfr.trimnum):
            cnt_not_ff = 0
            for yy in range(me.sfr.trimsz):
                if rdat[xx*me.sfr.trimsz + yy] != 0xff:
                    cnt_not_ff += 1
            if cnt_not_ff == 0 and xx > 0: # found
                ret = rdat[(xx-1)*me.sfr.trimsz : xx*me.sfr.trimsz]
                break

        ofs = me.sfrrx (me.sfr.OFS, 1)[0]
        dec = me.sfrrx (me.sfr.DEC, 1)[0]
        endadr = (ofs+dec*256) & me.sfr.nvmmsk
        me.sfrwx (me.sfr.DEC, [endadr>>8]) # clear ACK

        return ret

