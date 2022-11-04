from brownie import accounts, config, SimpleStorage, network
import os


def deploySimpleStorage():
    account = get_account()
    # account = accounts.load("testacc")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])

    simpleStorage = SimpleStorage.deploy({"from": account})

    storedValue = simpleStorage.retrieve()

    transaction = simpleStorage.store(15, {"from": account})
    transaction.wait(1)
    updatedStoredValue = simpleStorage.retrieve()

    print(updatedStoredValue)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploySimpleStorage()
