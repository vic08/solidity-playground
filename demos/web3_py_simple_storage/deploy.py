from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourcemap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://goerli.infura.io/v3/67fc44b22773407cb14e5142f702a64c")
)

chain_id = 5

my_address = "0x624540C8650caeaCd5e67F3Be658bB58F461EEA9"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

print("Deploying the contract...")
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed.")

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -simulate making a call and get a return value - nothing is sent to the blockchain
# transact - actually make a state change on the blockchain

# print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

print("Sending 'store' transaction...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Transaction sent")

print(simple_storage.functions.retrieve().call())
