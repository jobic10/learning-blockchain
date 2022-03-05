import json
from solcx import compile_standard
# install_solc("0.6.0")
from web3 import Web3
with open("./SimpleStorage.sol")as file:
    simpleStorageFile = file.read()


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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xA3b477b7673CCAD96Ab02D660a6CDD6e76cCbCcf"
private_key = "0x965d1fd74aed1a54d9317471efdb37df38163d29a6b79d39b9a3ee085df85852"


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1: Build a transaction
# 2: Sign "" ""
# 3: Send "" ""

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
print(transaction)
