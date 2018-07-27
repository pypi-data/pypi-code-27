from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
from eth_tester import EthereumTester

tester = EthereumTester()
web3 = Web3(EthereumTesterProvider(tester))


import json

class Package:
    def __init__(self, package_filename):
        with open(package_filename, 'r') as f:
            self.__package = json.loads(f.read())

    def contract_factory(self, contract_name):
        contract_type = self.__package['contract_types'][contract_name]
        interface = {}
        interface['abi'] = contract_type['abi']
        interface['bytecode'] = contract_type['deployment_bytecode']['bytecode']
        interface['bytecode_runtime'] = contract_type['runtime_bytecode']['bytecode']
        return web3.eth.contract(**interface)
