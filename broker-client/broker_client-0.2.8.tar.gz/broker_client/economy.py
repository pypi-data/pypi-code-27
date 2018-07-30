import base58
import json
import os
from Crypto.Hash import SHA256
from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey, SECP256k1

DEFAULT_FILE_NAME = 'keys.json'

def generate_keys_and_address(filename=DEFAULT_FILE_NAME):
    sk = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
    vk = sk.get_verifying_key()
    signature = sk.sign(b'message')
    assert vk.verify(signature, b'message')
    pub_key_bin = vk.to_string()
    address = get_address(pub_key_bin)
    private_key = base58.b58encode(sk.to_string())
    public_key = base58.b58encode(pub_key_bin)
    keys_dict = {'private-key':private_key.decode(),'public-key':public_key.decode(),'address':address}
    with open(filename, 'w') as file_obj:
        file_obj.write(json.dumps(keys_dict))
    return keys_dict

def get_keys_and_address(filename=None):
    if filename:
        if os.path.exists(str(filename)):
            with open(filename, 'r') as file_obj:
                keys_dict = json.loads(file_obj.read())
                keys_dict['private-key'] = base58.b58decode(keys_dict['private-key'].encode())
                keys_dict['public-key'] = base58.b58decode(keys_dict['public-key'].encode())
                return keys_dict
        else:
            keys_dict = generate_keys_and_address(filename)
            keys_dict['private-key'] = base58.b58decode(keys_dict['private-key'].encode())
            keys_dict['public-key'] = base58.b58decode(keys_dict['public-key'].encode())
            return keys_dict
    elif os.path.exists(DEFAULT_FILE_NAME):
        with open(DEFAULT_FILE_NAME, 'r') as file_obj:
            keys_dict = json.loads(file_obj.read())
            keys_dict['private-key'] = base58.b58decode(keys_dict['private-key'].encode())
            keys_dict['public-key'] = base58.b58decode(keys_dict['public-key'].encode())
            return keys_dict
    else:
        keys_dict = generate_keys_and_address()
        keys_dict['private-key'] = base58.b58decode(keys_dict['private-key'].encode())
        keys_dict['public-key'] = base58.b58decode(keys_dict['public-key'].encode())
        return keys_dict

def get_address(pub_key_bin):
    pub_hash_bin = SHA256.new(pub_key_bin).digest()
    address = base58.b58encode_check(pub_hash_bin)
    return address.decode()

def sign_tx(transaction, keys_dict):
    if type(transaction) == dict:
        msg_signed_bin = json.dumps(transaction, separators=(',', ':')).encode()
        sk = SigningKey.from_string(keys_dict['private-key'], curve=SECP256k1, hashfunc=sha256)
        signature = sk.sign(msg_signed_bin)
        vk = VerifyingKey.from_string(keys_dict['public-key'], curve=SECP256k1, hashfunc=sha256)
        assert vk.verify(signature, msg_signed_bin)
        sig = base58.b58encode_check(signature).decode()
        puk = base58.b58encode_check(keys_dict['public-key']).decode()
        transaction['content']['input']['sig'] = sig
        transaction['content']['input']['pub_key'] = puk
        return transaction
    else:
        return None
