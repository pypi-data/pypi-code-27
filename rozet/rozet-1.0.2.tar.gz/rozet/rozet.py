import os
import json

from .config import Config, rinkeby_config
from .utils import mnemonic as Mnemonic

from web3 import Web3
from web3.utils import events as Events

class Badge(object):
    title: str
    content: str
    rating: int
    recipient: str
    recipientsEthAddress: str
    sender: str
    sendersEthAddress: str
    image: str = ''
    banner: str = ''
    permalink: str = ''
    video: str = ''

    def __init__(self, title: str, content: str, rating: int, recipient: str, recipientsEthAddress: str, sender: str, sendersEthAddress: str, image: str = '', banner: str = '', permalink: str = '', video: str = ''):
        self.title = title
        self.content = content
        self.rating = rating
        self.recipient = recipient
        self.recipientsEthAddress = recipientsEthAddress
        self.sender = sender
        self.sendersEthAddress = sendersEthAddress
        self.image = image
        self.banner = banner
        self.permalink = permalink
        self.video = video

#ABIS
abi_rozet_token_path = os.path.join(os.path.dirname(__file__), 'abis', 'RozetTokenABI.json')
abi_rozet_contract_path = os.path.join(os.path.dirname(__file__), 'abis', 'RozetABI.json')


class Rozet(object):
    """ The Rozet Python SDK implements the client-side libraries used by applications using the Rozet protocols.

            Functions:
                issueBadge  -- create badge;
                events      -- get badge events;
    """
    min_balance_for_badge: int = 1701971370265500

    def __init__(self, mnemonic: str = '', config: Config = rinkeby_config):
        """ Constructor of Rozet class for setup provider, contracts and prepare configurations.

                Parameters:
                    mnemonic    -- seed wordlist, usually with 24 words;
                    config      -- config object for net configurations;

        """
        self.web3 = Web3(Web3.HTTPProvider(config.WEB3_ENDPOINT, request_kwargs={'timeout': 60}))

        self.mnemonic = mnemonic
        self.private_key, self.address = Mnemonic.get_privkey_address_from_mnemonic(mnemonic)
        self.address = self.web3.toChecksumAddress(self.address)

        self.rozet_token_address = self.web3.toChecksumAddress(config.ROZET_TOKEN_CONTRACT)
        self.rozet_address = self.web3.toChecksumAddress(config.ROZET_CONTRACT)

        self._prepare_abis()
        self._prepare_contracts()
        pass

    def _prepare_abis(self):
        with open(abi_rozet_token_path, 'r') as f:
            self.rozet_token_abi = f.read()
        with open(abi_rozet_contract_path, 'r') as f:
            self.rozet_abi = f.read()

    def _prepare_contracts(self):
        self.rozet_token_contract = self.web3.eth.contract(address=self.rozet_token_address, abi=self.rozet_token_abi)
        self.rozet_contract = self.web3.eth.contract(address=self.rozet_address, abi=self.rozet_abi)

    def _truncate_badge(self, badge: Badge) -> Badge:
        urlChars = 100
        videoChars = 50
        permalinkChars = 400
        titleChars = 100
        badgeChars = 400

        if (badge.image and len(badge.image) > urlChars):
            badge.image = badge.image[0:urlChars]  + '...'
        if (badge.banner and len(badge.banner) > urlChars):
            badge.banner = badge.banner[0:urlChars] + '...'
        if (badge.permalink and len(badge.permalink) > permalinkChars):
            badge.permalink = badge.permalink[0:permalinkChars] + '...'
        if (badge.title and len(badge.title) > titleChars):
            badge.title = badge.title[0:titleChars] + '...'
        if (badge.content and len(badge.content) > badgeChars):
            badge.content = badge.content[0:badgeChars] + '...'
        if (badge.video and len(badge.video) > videoChars):
            badge.video = badge.video[0:videoChars] + '...'

        return badge

    def _reputation_str(self, badge: Badge) -> str:
        badge = self._truncate_badge(badge)
        values = badge.__dict__
        result = {}

        for key in values:
            value = values[key]
            if value != '' and value is not None:
                result[key] = value

        reputation = json.dumps(result)

        if (len(reputation) > 1000):
            reputation = reputation[0:1000] + '...'

        return reputation

    def issueBadge(self, badge: Badge):
        """ Create badge in Rozet protocol.

                Parameters:
                    badge -- badge object with all params
        """
        balance = self.web3.eth.getBalance(self.address)

        assert balance > self.min_balance_for_badge, f'Balance ({balance}) is too low'

        reputation = self._reputation_str(badge)
        tx = self.rozet_contract.functions.issueBadge(
            self.web3.toChecksumAddress(badge.sendersEthAddress),
            self.web3.toChecksumAddress(badge.recipientsEthAddress),
            self.web3.toChecksumAddress(badge.sendersEthAddress),
            reputation).buildTransaction({
            'gasPrice' : self.web3.toWei('10', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.address),
            'gas': 4704624
        })
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.private_key)

        result = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result.hex()

    def events(self, previous_blocks: int):
        """ Get all badge events from Rozet protocol.

                Parameters:
                    previous_blocks -- count of last blocks for find
        """
        latestBlock = self.web3.eth.blockNumber
        fromBlock = latestBlock - previous_blocks
        event = self.rozet_contract.events.BadgeIssued()

        filter = {
            'fromBlock': fromBlock,
            'toBlock': latestBlock,
            'address': self.rozet_address
        }

        logs = self.web3.eth.getLogs(filter)

        for log in logs:
            yield Events.get_event_data(event.abi, log)
