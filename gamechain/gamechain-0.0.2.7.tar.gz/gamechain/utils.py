import requests
import time


def get_tx_testnet(txid):
    url = f"https://test-bch-insight.bitpay.com/api/tx/{txid}"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            time.sleep(0.3)


def ensure_prefixed_address(addr):
    if not addr.startswith("bchtest:"):
        return f"bchtest:{addr}"

    return addr


def get_transaction_ids_for_address(addr):
    # https://test-bch-insight.bitpay.com/api/addr/bchtest:qqngkfyr38e6gp8cmmzejfdc47h3ppum5qflqpr87y
    # {
    #     "addrStr": "qqngkfyr38e6gp8cmmzejfdc47h3ppum5qflqpr87y",
    #     "balance": 0,
    #     "balanceSat": 0,
    #     "totalReceived": 0,
    #     "totalReceivedSat": 0,
    #     "totalSent": 0,
    #     "totalSentSat": 0,
    #     "unconfirmedBalance": 0,
    #     "unconfirmedBalanceSat": 0,
    #     "unconfirmedTxApperances": 0,
    #     "txApperances": 1,
    #     "transactions": [
    #         "bd4282b683102bf0e2e4fb025d27c88511a3c7aab4c911d73e00ce9553e1ed01"
    #     ]
    # }
    testnet_addr_url = "https://test-bch-insight.bitpay.com/api/addr/" + ensure_prefixed_address(addr)
    addr_data = requests.get(testnet_addr_url).json()
    txids = addr_data["transactions"]
    return txids


def single(items, predicate, raiseExceptionOnNotFound=True):
    filtered = [i for i in items if predicate(i)]
    if len(filtered) == 0:
        if raiseExceptionOnNotFound:
            raise Exception("No item that matches predicate %s" % predicate)
        return None
    if len(filtered) > 1:
        raise Exception("More than one item matches predicate %s" % predicate)

    return filtered[0]


def where(items, predicate):
    filtered = [i for i in items if predicate(i)]
    return filtered


if __name__ == "__main__":
    tx = get_tx_testnet("91955d1d228453fac7113850eeab48bf31350f5e0767a7d2357ca47af1836cde")

    print(tx)
