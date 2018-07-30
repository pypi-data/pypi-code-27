
_use_testnet: bool = True


def set_use_mainnet(use_it: bool):
    global _use_testnet
    _use_testnet = not use_it


def is_testnet() -> bool:
    return _use_testnet


def get_bitpay_insight_api_url() -> str:
    if _use_testnet:
        return f"https://test-bch-insight.bitpay.com/api"

    raise Exception("Insight API only tested/available with testnet")


def ensure_prefixed_address_str(addr: str) -> str:
    if is_testnet():
        if not addr.startswith("bchtest:"):
            return f"bchtest:{addr}"
    else:
        if not addr.startswith("bitcoincash:"):
            return f"bitcoincash:{addr}"

    return addr
