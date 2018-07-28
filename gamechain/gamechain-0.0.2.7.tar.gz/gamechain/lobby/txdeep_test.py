
from bitcash import PrivateKeyTestnet

import gcl_secrets, time


initiator_key = PrivateKeyTestnet(gcl_secrets.INITIATOR_PRIVATE_KEY)

print(initiator_key.get_unspents())

print(initiator_key.get_balance())

to_send = [('bchtest:qqtp5le4dp59tmavqdsapc5u0n2qm89rfuty833q5u', 1112, 'satoshi')]


next_to_spend_txid = None
# next_to_spend_txid = "7ff29e72dfbce5a631699175d6ef6b16c9acbcfc0a424b765378602de9d1bb59s"


if not next_to_spend_txid:
    next_to_spend_txid = initiator_key.get_unspents()[0].txid

next_tx_found = False

for i in range(30):
    while not next_tx_found:
        unspents = initiator_key.get_unspents()
        for unspent in unspents:
            if unspent.txid == next_to_spend_txid:
                to_spend = [unspent]
                next_tx_found = True
                print(unspent)
        if not next_tx_found:
            time.sleep(1)

    next_to_spend_txid = initiator_key.send(to_send, unspents=to_spend)
    print(next_to_spend_txid)
    next_tx_found = False

    print(i)


