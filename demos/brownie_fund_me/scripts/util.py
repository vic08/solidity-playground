from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 18
STARTING_PRICE = 2000

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_ENV = ["development", "ganache-local"]

def get_account():
    if network.show_active() in LOCAL_ENV or network.show_active() in FORKED_LOCAL_ENV:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print(f"Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": account})

    print("Mocks deployed.")
