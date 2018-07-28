from bitcash import PrivateKeyTestnet, format

import gcl_secrets

initiator_key = PrivateKeyTestnet(gcl_secrets.INITIATOR_PRIVATE_KEY)
print(initiator_key.public_key)
print(len(initiator_key.public_key))

message = b"123fsafsafsfsfsafsaffsafse3223gsdgbdbJGoeffffddw23abc"

sig = initiator_key.sign(message)
print(sig)
print(len(sig))
pubkey = initiator_key.public_key
print(len(initiator_key.public_key))

verified = format.verify_sig(sig, message, pubkey)

print(verified)

