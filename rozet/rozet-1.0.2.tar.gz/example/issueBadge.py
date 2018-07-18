from rozet import Rozet, Badge

mnemonic = 'example example example example example example example example example example example example'
r = Rozet(mnemonic=mnemonic)

badge = Badge(
    'Great guy!',
    'Great doing business with you!',
    5,
    'john_b',
    '0x1111111111111111111111111111111111111111',
    'nathan!',
    '0x1111111111111111111111111111111111111111'
)


tx_hash = r.issueBadge(badge)

print(f'Issue badge in tx {tx_hash}')