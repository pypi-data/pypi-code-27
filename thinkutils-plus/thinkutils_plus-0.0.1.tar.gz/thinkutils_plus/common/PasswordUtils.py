#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from random import choice
import string
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import Crypto
from Crypto.PublicKey import RSA
import base64
from base64 import b64decode
from thinkutils_plus.common_utils.think_hashlib import *

def random_password(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

# def make_rsa_pub_key(exponent, modulus):
#     numbers = RSAPublicNumbers(exponent, modulus)
#     public_key = numbers.public_key(backend=default_backend())
#     return public_key
#
#
# expected_n = int("00833c4af965ff7a8409f8b5d5a83d87f2f19d7c1eb40dc59a98d2346cbb145046b2c6facc25b5cc363443f0f7ebd9524b7c1e1917bf7d849212339f6c1d3711b115ecb20f0c89fc2182a985ea28cbb4adf6a321ff7e715ba9b8d7261d1c140485df3b705247a70c28c9068caabbedbf9510dada6d13d99e57642b853a73406817", 16)
#
# publicKey = make_rsa_pub_key(65537, expected_n)
# pem = publicKey.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
# print publicKey
# print str(pem).strip()
# print type(pem)
#
# # szPem = str(pem).replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----").strip()
# # # pem = pem.replace("-----END PUBLIC KEY-----").strip()
# #
# # print szPem
#
# # key64 = b'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDPEr5Zf96hAn4tdWoPYfy8Z18HrQNxZqY0jRsuxRQRrLG+swltcw2NEPw9+vZUkt8HhkXv32EkhIzn2wdNxGxFeyyDwyJ/CGCqYXqKMu0rfajIf9+cVupuNcmHRwUBIXfO3BSR6cMKMkGjKq77b+VENrabRPZnldkK4U6c0BoFwIDAQAB'
#
# key64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDPEr5Zf96hAn4tdWoPYfy8Z18HrQNxZqY0jRsuxRQRrLG+swltcw2NEPw9+vZUkt8HhkXv32EkhIzn2wdNxGxFeyyDwyJ/CGCqYXqKMu0rfajIf9+cVupuNcmHRwUBIXfO3BSR6cMKMkGjKq77b+VENrabRPZnldkK4U6c0BoFwIDAQAB"
# keyDER = b64decode(key64)
# keyPub = RSA.importKey(keyDER)
#
# encryptedPwd = keyPub.encrypt(("Ab123456").upper(), 256)
# print encryptedPwd[0].encode('hex')
# print encryptedPwd
#
#
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
#
# rsakey = RSA.importKey(keyDER)
# rsakey = PKCS1_OAEP.new(rsakey)
# decrypted_message= rsakey.encrypt("Ab123456")
# print decrypted_message.encode('hex')

#print random_password()
#print random_password()
#print random_password()
#print random_password()
#print random_password()

