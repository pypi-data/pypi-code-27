# -*- coding: utf-8 -*-
""" Certificate generation module """

import os

from OpenSSL import crypto

DIGEST  = ('md2',
           'md5',
           'mdc2',
           'rmd160',
           'sha',
           'sha1',
           'sha224',
           'sha256',
           'sha384',
           'sha512')

class GenCert(object):
    def __init__(self, bits=None, crypto_type=None, digest_type=None, notbefore_days=None, notafter_days=None):
        self.bits           = 2048
        self.crypto_type    = crypto.TYPE_RSA
        self.digest_type    = 'md5'
        self.notbefore_days = 0
        self.notafter_days  = 365

        if bits:
            self.set_bits(bits)

        if crypto_type:
            self.set_crypto_type(crypto_type)

        if digest_type:
            self.set_digest_type(digest_type)

        if notbefore_days:
            self.set_notbefore_days(notbefore_days)

        if notafter_days:
            self.set_notafter_days(notafter_days)

    def set_bits(self, bits):
        if not isinstance(bits, int):
            raise ValueError("Invalid bits: %r" % bits)
        self.bits = bits
        return self

    def set_crypto_type(self, xtype):
        if xtype in (crypto.TYPE_RSA, crypto.TYPE_DSA):
            self.crypto_type = xtype
        elif xtype in ('rsa', 'dsa'):
            self.crypto_type = getattr(crypto, "TYPE_%s" % xtype.upper())
        else:
            raise ValueError("Invalid crypto type: %r" % xtype)
        return self

    def set_digest_type(self, digest):
        if digest not in DIGEST:
            raise ValueError("Invalid digest type: %r" % digest)
        self.digest_type = digest
        return self

    def set_notbefore_days(self, days):
        if isinstance(days, int):
            days    = str(days)
        if not isinstance(days, basestring) or not days.isdigit():
            raise ValueError("Invalid days for notbefore: %r" % days)
        self.notbefore_days = int(days)
        return self

    def set_notafter_days(self, days):
        if isinstance(days, int):
            days    = str(days)
        if not isinstance(days, basestring) or not days.isdigit():
            raise ValueError("Invalid days for notafter: %r" % days)
        self.notafter_days = int(days)
        return self

    def make_privatekey(self, export_file=False):
        pkey = crypto.PKey()
        pkey.generate_key(self.crypto_type, self.bits)

        if isinstance(export_file, basestring):
            dpkey   = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)

            if not os.path.exists(export_file):
                open(export_file, 'w').close()
            os.chmod(export_file, 0600)

            f       = open(export_file, 'w')
            f.writelines(dpkey)
            f.close()
        return pkey

    def make_certreq(self, pkey, attributes, export_file=False):
        csr     = crypto.X509Req()
        subject = csr.get_subject()
        for key, value in attributes.iteritems():
            setattr(subject, key, value)

        csr.set_pubkey(pkey)
        csr.sign(pkey, self.digest_type)

        if isinstance(export_file, basestring):
            dcsr    = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr)

            if not os.path.exists(export_file):
                open(export_file, 'w').close()
            os.chmod(export_file, 0600)

            f       = open(export_file, 'w')
            f.writelines(dcsr)
            f.close()
        return csr

    def make_certificate(self, csr, ca, ca_pkey, serial, export_file=False):
        crt = crypto.X509()
        crt.set_serial_number(serial)
        crt.gmtime_adj_notBefore(86400 * self.notbefore_days)
        crt.gmtime_adj_notAfter(86400 * self.notafter_days)
        crt.set_issuer(ca.get_subject())
        crt.set_subject(csr.get_subject())
        crt.set_pubkey(csr.get_pubkey())
        crt.sign(ca_pkey, self.digest_type)

        if isinstance(export_file, basestring):
            dcrt    = crypto.dump_certificate(crypto.FILETYPE_PEM, crt)

            if not os.path.exists(export_file):
                open(export_file, 'w').close()
            os.chmod(export_file, 0600)

            f       = open(export_file, 'w')
            f.writelines(dcrt)
            f.close()
        return crt
