from .crypto import HDPrivateKey, HDPublicKey, HDKey

def get_privkey_address_from_mnemonic(mnemonic: str, passphrase: str = ''):
    master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic, passphrase)
    root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
    acct_priv_key = root_keys[-1]
    keys = HDKey.from_path(acct_priv_key, '0/0')
    private_key = keys[-1]

    private_key_hex = private_key._key.to_hex()
    address = private_key.public_key.address()

    assert len(private_key_hex) > 0, 'Error get private key from mnemonic'
    assert len(address) > 0, 'Error get address from mnemonic'

    private_key_hex = f'0x{private_key_hex}'

    return (private_key_hex, address)