import requests
import time
from . import which_net


def get_tx(txid) -> str:
    insight_url = which_net.get_bitpay_insight_api_url()
    url = f"{insight_url}/tx/{txid}"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            time.sleep(0.3)


def get_transaction_ids_for_address(addr):
    insight_api_url = which_net.get_bitpay_insight_api_url()
    addr_url = f"{insight_api_url}/addr/" + which_net.ensure_prefixed_address_str(addr)
    addr_data = requests.get(addr_url).json()
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
    tx = get_tx("91955d1d228453fac7113850eeab48bf31350f5e0767a7d2357ca47af1836cde")

    print(tx)
