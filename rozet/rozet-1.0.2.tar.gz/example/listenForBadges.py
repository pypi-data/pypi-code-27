from rozet import Rozet

r = Rozet()

previousBlocks = 1000000

events = r.events(previousBlocks)

for event in events:
    sender = event['args']['sender']
    tx_hash = event['transactionHash'].hex()
    print(f'{sender} sent a badge with txHash {tx_hash}!')