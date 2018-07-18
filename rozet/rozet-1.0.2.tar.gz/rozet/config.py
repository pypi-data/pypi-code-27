class Config:
    WEB3_ENDPOINT: str
    ROZET_TOKEN_CONTRACT: str
    ROZET_CONTRACT: str

    def __init__(self, endpoint, token_contract, contract):
        self.WEB3_ENDPOINT = endpoint
        self.ROZET_TOKEN_CONTRACT = token_contract
        self.ROZET_CONTRACT = contract


rinkeby_config = Config('https://rinkeby.infura.io/uaNKEkpjsyvArG0sHifx', '0xcea271df25a47087252da2fe9b7d6d9152f0c98a', '0xb93ca7fda4422ce8a70daa7058a603bd613033a9')
# main_config = Config('https://mainnet.infura.io/uaNKEkpjsyvArG0sHifx', 'not on mainnet yet', 'not on mainnet yet')