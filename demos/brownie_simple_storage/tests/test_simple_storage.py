from brownie import SimpleStorage, accounts


def test_deploy():
    account = accounts[0]

    simpleStorage = SimpleStorage.deploy({"from": account})
    startingValue = simpleStorage.retrieve()

    expected = 0

    assert startingValue == expected


def test_updating_storage():
    account = accounts[0]

    simple_storage = SimpleStorage.deploy({"from": account})

    expected = 15
    simple_storage.store(expected, {"from": account})

    assert expected == simple_storage.retrieve()
