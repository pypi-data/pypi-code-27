# -*- coding:UTF-8 -*-
import json
import random
import time
import urllib

import requests
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import binascii
import tempfile
import os
import subprocess


# 当前python RSA私钥解密只支持pkcs1格式，所以使用python进行解密前，如果是pkcs8格式，必须先将pkcs8格式转换成pkcs1格式的，然后在 python 中使用该密钥进行解密。
# 将pkcs8格式私钥转换成pkcs1格式时，需要保证pkcs8私钥是完整的包含了头尾，然后再使用命令：
# openssl rsa -in pkcs8.pem -out pkcs1.pem
# 执行操作(在windows上可以安装openssl win32版本，或者如果安装了git，可以在git bash环境中手动执行该命令)，其中pkcs8.pem为完整的包含了头尾的pkcs8格式私钥文件，
# pkcs1.pem为输出的完整的包含了头尾的pkcs1格式私钥文件。更详细信息可参考网址：https://www.jianshu.com/p/08e41304edab
# 该步操作当前已经集成到demo中了，但需要确保openssl已经正常安装并已经添加到系统路径PATH中，能够正常调用。


class Constant:
    RANDOM_KEY = 'randomKey'
    BIZ_CONTENT = 'bizContent'
    DATA = 'data'
    SIGN_TYPE = 'signType'
    SIGN = 'sign'
    CHARSET = 'charset'
    FORMAT = 'format'
    TIMESTAMP = 'timestamp'
    CHARSET_UTF8 = 'utf-8'
    RSA = 'RSA'
    FORMAT_JSON = 'json'
    SUCCESS = '0'
    VERSION = 'version'
    APP_ID = 'appId'
    CODE = 'code'
    MESSAGE = 'message'
    AMOUNT = 'amount'


# 获取以ms为单位的时间戳
def get_timestamp():
    ms_per_sec = 1000
    return str(int(time.time() * ms_per_sec))


def read_file_content(file_name):
    fh = open(file_name, 'r')
    data = fh.read()
    fh.close()

    return data


def write_to_file(name, data):
    fh = None
    if data:
        try:
            if type(data) == str:
                fh = open(name, 'w')
            else:
                fh = open(name, 'wb')

            fh.write(data)
        finally:
            if fh:
                fh.close()


# 生成公私钥后保存到指定目录
def generate_rsa_key_pair(target_dir):
    # 伪随机数生成器
    random_generator = Random.new().read

    # rsa算法生成实例
    rsa = RSA.generate(1024, random_generator)

    # 秘钥对的生成
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    private_file = os.path.join(target_dir, 'private.pem')
    if os.path.isfile(private_file):
        os.remove(private_file)
    write_to_file(private_file, private_pem)
    print('have written private key to {}.'.format(private_file))

    public_file = os.path.join(target_dir, 'public.pem')
    if os.path.isfile(public_file):
        os.remove(public_file)
    write_to_file(public_file, public_pem)
    print('have written public key to {}.'.format(public_file))


# 将pkcs8_key先写文件，转换完成之后再读文件获取转换后的内容
def convert_pkcs8_to_pkcs1_with_cmd(pkcs8_key):
    pkcs1_key = None
    temp_dir = tempfile.gettempdir()
    dir_name = 'pkcs8to1'
    work_dir = os.path.join(temp_dir, dir_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    src_file_name = 'pkcs8.pem'
    dst_file_name = 'pkcs1.pem'
    src_file = os.path.join(work_dir, src_file_name)
    if os.path.exists(src_file):
        os.remove(src_file)

    write_to_file(src_file, pkcs8_key)

    dst_file = os.path.join(work_dir, dst_file_name)
    cmd_fmt = 'openssl rsa -in {} -out {}'
    cmd_str = cmd_fmt.format(src_file, dst_file)
    rtn = subprocess.check_call(cmd_str, shell=True)
    if rtn != 0:
        return pkcs1_key

    pkcs1_key = read_file_content(dst_file)

    return pkcs1_key


# 将public key先写文件，转换完成之后再读文件获取转换后的内容
def format_public_key_with_cmd(public_key):
    pkcs1_key = None
    temp_dir = tempfile.gettempdir()
    dir_name = 'pkcs8_public'
    work_dir = os.path.join(temp_dir, dir_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    src_file_name = 'pkcs8_src.pem'
    dst_file_name = 'pkcs8_dst.pem'
    src_file = os.path.join(work_dir, src_file_name)
    if os.path.exists(src_file):
        os.remove(src_file)

    write_to_file(src_file, public_key)

    dst_file = os.path.join(work_dir, dst_file_name)
    cmd_fmt = 'openssl rsa -pubin -in {} -pubout -out {}'
    cmd_str = cmd_fmt.format(src_file, dst_file)
    rtn = subprocess.check_call(cmd_str, shell=True)
    if rtn != 0:
        return pkcs1_key

    pkcs1_key = read_file_content(dst_file)

    return pkcs1_key


def convert_pkcs8_to_pkcs1_with_key_spec(key_spec):
    key_begin = '-----BEGIN PRIVATE KEY-----\n'
    key_end = '\n-----END PRIVATE KEY-----\n'
    pkcs8_key = key_begin + key_spec + key_end
    pkcs1_key = convert_pkcs8_to_pkcs1_with_cmd(pkcs8_key)

    return pkcs1_key


def combine_public_key_with_key_spec(key_spec):
    key_begin = '-----BEGIN PUBLIC KEY-----\n'
    key_end = '\n-----END PUBLIC KEY-----\n'
    pkcs8_key = key_begin + key_spec + key_end
    return pkcs8_key


# 将公钥进行格式化
def format_public_key_with_key_spec(key_spec):
    src_key = combine_public_key_with_key_spec(key_spec)
    dst_key = format_public_key_with_cmd(src_key)

    return dst_key


def convert_pkcs8_to_pkcs1(pkcs8_key):
    pkcs1_key = convert_pkcs8_to_pkcs1_with_cmd(pkcs8_key)
    return pkcs1_key


# 公钥加密之后转换成base64编码
def encrypt_with_rsa(message, public_pem):
    if type(message) == str:
        to_enc_data = bytes(message, 'utf-8')
    else:
        to_enc_data = message

    rsakey = RSA.importKey(public_pem)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(to_enc_data))
    return cipher_text.decode()


# 私钥解密base64编码的数据
def decrypt_with_rsa(cipher_text, private_pem):
    rsakey = RSA.importKey(private_pem)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # 伪随机数生成器
    random_generator = Random.new().read
    text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
    return text.decode()


class AESECB:
    def __init__(self, key, hex_switch=False):
        if type(key) == str:
            to_use_key = bytes(key, 'utf-8')
        else:
            to_use_key = key

        self.key = to_use_key
        self.mode = AES.MODE_ECB

        # encrypt时，hex_switch表示是否需要进行hex形式(0x##)切换到正常展示(##)
        # decrypt时, hex_switch表示是否需要进行正常展示(##)切换到hex形式(0x##)
        self.hex_switch = hex_switch

        self.bs = 16  # block size
        self.pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    # parameter data should be string type.
    def encrypt(self, data):
        generator = AES.new(self.key, self.mode)  # ECB模式无需向量iv
        enc_bytes = bytes(self.pad(data), 'utf-8')
        crypt = generator.encrypt(enc_bytes)

        if self.hex_switch:
            result = binascii.b2a_hex(crypt)
        else:
            result = crypt

        return result

    def decrypt(self, data):
        if self.hex_switch:
            to_dec = binascii.a2b_hex(data)
        else:
            if type(data) == str:
                to_dec = bytes(data, 'utf-8')
            else:
                to_dec = data

        result = self._decrypt_bytes(to_dec)
        return result

    def _decrypt_bytes(self, byte_data):
        generator = AES.new(self.key, self.mode)  # ECB模式无需向量iv
        meg = generator.decrypt(byte_data)
        result = self.unpad(meg.decode('utf-8'))

        return result


def encrypt_with_aes(data, aes_key, hex_switch=False):
    aes = AESECB(aes_key, hex_switch)
    return base64.b64encode(aes.encrypt(data)).decode()


def encrypt_with_aes_key_base64(data, aes_key, hex_switch=False):
    aes = AESECB(base64.b64decode(aes_key), hex_switch)
    return base64.b64encode(aes.encrypt(data)).decode()


def decrypt_with_aes(enc_info, aes_key, hex_switch=False):
    aes = AESECB(aes_key, hex_switch)
    return aes.decrypt(enc_info)


def decrypt_with_aes_key_base64(enc_info, aes_key, hex_switch=False):
    aes = AESECB(base64.b64decode(aes_key), hex_switch)
    return aes.decrypt(enc_info)


def get_aes_random_key():
    value = random.randint(0, 0xffffffffffffffff)
    return '{:016x}'.format(value)


def urlencode_orderly(dict_data):
    keys = sorted(dict_data.keys())
    items = []
    item_str_format = '{}={}'
    for k in keys:
        value = dict_data[k]
        if value:
            item_str = item_str_format.format(k, value)
            items.append(item_str)

    return '&'.join(items)


def sign_with_sha256_rsa(data, key):
    if type(data) == str:
        data_bytes = bytes(data, 'utf-8')
    else:
        data_bytes = data

    if type(key) == str:
        key_bytes = bytes(key, 'utf-8')
    else:
        key_bytes = key

    signer = serialization.load_pem_private_key(
        key_bytes,
        password=None,
        backend=default_backend()
    )

    # 使用私钥对数据进行签名
    # 指定填充方式为PKCS1v15
    # 指定hash方式为sha256
    signature = signer.sign(
        data_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return signature


def sign_with_sha256_rsa_and_output_base64_str(data, key):
    signature = sign_with_sha256_rsa(data, key)
    return base64.b64encode(signature).decode()


def verify_with_sha256_rsa(signature, data, key):
    if type(data) == str:
        data_bytes = bytes(data, 'utf-8')
    else:
        data_bytes = data

    if type(key) == str:
        key_bytes = bytes(key, 'utf-8')
    else:
        key_bytes = key

    # 使用公钥对数据进行验签
    # 指定填充方式为PKCS1v15
    # 指定hash方式为sha256
    verifier = serialization.load_pem_public_key(
        key_bytes,
        backend=default_backend()
    )

    try:
        verifier.verify(
            signature,
            data_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return True
    except InvalidSignature:
        return False


class ApiRequestFlag:
    charset = 'charset'
    sign_type = 'signType'
    format = 'format'
    timestamp = 'timestamp'
    sign = 'sign'
    random_key = 'randomKey'
    biz_content = 'bizContent'


def combine_request_body(signature, enc_biz_content, enc_random_key, timestamp):
    item_map = dict()

    item_map[ApiRequestFlag.biz_content] = enc_biz_content
    item_map[ApiRequestFlag.sign] = signature
    item_map[ApiRequestFlag.charset] = Constant.CHARSET_UTF8
    item_map[ApiRequestFlag.format] = Constant.FORMAT_JSON
    item_map[ApiRequestFlag.random_key] = enc_random_key
    item_map[ApiRequestFlag.sign_type] = Constant.RSA
    item_map[ApiRequestFlag.timestamp] = timestamp

    return json.dumps(item_map)


def combine_data_for_signing(enc_data, enc_random_key, timestamp):
    data = dict()
    data[Constant.CHARSET] = Constant.CHARSET_UTF8
    data[Constant.FORMAT] = Constant.FORMAT_JSON
    data[Constant.SIGN_TYPE] = Constant.RSA
    data[Constant.BIZ_CONTENT] = enc_data
    data[Constant.RANDOM_KEY] = enc_random_key
    data[Constant.TIMESTAMP] = timestamp

    # result = urllib.parse.urlencode(data)
    # 不能直接使用urlencode进行编码，需要先排序再拼接
    result = urlencode_orderly(data)

    return result


def combine_data_for_verifying(data, random_key):
    data_map = dict()
    data_map[Constant.DATA] = data
    data_map[Constant.RANDOM_KEY] = random_key

    return urlencode_orderly(data_map)


# 将所有参数拼接成一个大的urlencode有序的字符串
def combine_page_url_params(biz_map, version, app_id, public_key, private_key):
    random_key = get_aes_random_key()
    enc_random_key = encrypt_with_rsa(random_key, public_key)
    data_json = json.dumps(biz_map)
    enc_biz_content = encrypt_with_aes(data_json, random_key)
    timestamp = get_timestamp()
    to_sign_data = combine_data_for_signing(enc_biz_content, enc_random_key, timestamp)
    signature = sign_with_sha256_rsa_and_output_base64_str(to_sign_data, private_key)

    data_map = dict()
    data_map[Constant.VERSION] = version
    data_map[Constant.BIZ_CONTENT] = urllib.parse.quote(enc_biz_content)
    data_map[Constant.RANDOM_KEY] = urllib.parse.quote(enc_random_key)
    data_map[Constant.APP_ID] = app_id
    data_map[Constant.SIGN_TYPE] = Constant.RSA
    data_map[Constant.SIGN] = urllib.parse.quote(signature)
    data_map[Constant.TIMESTAMP] = timestamp
    data_map[Constant.CHARSET] = Constant.CHARSET_UTF8
    data_map[Constant.FORMAT] = Constant.FORMAT_JSON

    return urlencode_orderly(data_map)


# 使用post请求调用接口
def post_for_response(url, data_map, public_key, private_key):
    random_key = get_aes_random_key()
    data_json = json.dumps(data_map)
    enc_data = encrypt_with_aes(data_json, random_key)
    enc_random_key = encrypt_with_rsa(random_key, public_key)
    timestamp = get_timestamp()

    to_sign_data = combine_data_for_signing(enc_data, enc_random_key, timestamp)
    signature = sign_with_sha256_rsa_and_output_base64_str(to_sign_data, private_key)
    body = combine_request_body(signature, enc_data, enc_random_key, timestamp)

    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    rtn_map = response.json()
    return rtn_map
