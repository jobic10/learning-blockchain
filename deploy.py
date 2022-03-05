import json
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()
with open("./SimpleStorage.sol")as file:
    simpleStorageFile = file.read()

install_solc("0.6.0")
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simpleStorageFile}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }, },
    },
}, solc_version="0.6.0")

# print(compiled_sol)

with open("compiled_code.json", 'w') as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# Get ABI
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']


# Connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

# My Key and Address changes always, hence I did not save them in environs. I'm using Ganache
my_address = "0x5D5c5451193F8f1a30B9002FA10FeC4Cc08c7a10"
private_key = os.getenv('PRIVATE_KEY')


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1: Build a transaction
# 2: Sign "" ""
# 3: Send "" ""
# print(SimpleStorage)
# print(SimpleStorage.constructor())
# print(SimpleStorage.constructor().buildTransaction())
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
})
signed_transaxtion = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
print(signed_transaxtion)


# Send this signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_transaxtion.rawTransaction)
