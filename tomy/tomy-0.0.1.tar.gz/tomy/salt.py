import hashlib
import random


def saltizer():
    rand_word = str(random.random())
    rand_word = rand_word.encode('utf8')
    salt = hashlib.sha1(rand_word).hexdigest()[:18]
    #print(salt)
    return salt


def small_saltizer():
    rand_word = str(random.random())
    rand_word = rand_word.encode('utf8')
    salt = hashlib.sha1(rand_word).hexdigest()[:4]
    #print(salt)
    return salt

def get_otp_pin():
    rand_word = str(random.random())
    rand_word = rand_word.encode('utf8')
    salt = hashlib.sha1(rand_word).hexdigest()[:6]
    #print(salt)
    return salt

def userslug():
    rand_word = str(random.random())
    rand_word = rand_word.encode('utf8')
    salt = hashlib.sha1(rand_word).hexdigest()[:10]
    #print(salt)
    return salt.upper()