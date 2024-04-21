from web3 import Web3
from solcx import compile_source
from hexbytes import HexBytes as hb
from dotenv import dotenv_values
config = dotenv_values(".env")

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))


PUB_KEY_LEADER = config['PUB_KEY_LEADER']
PUB_KEY_RIGHT_HAND = config['PUB_KEY_RIGHT_HAND']
PUB_KEY_HERO = config['PUB_KEY_HERO']

PUB_KEY_BOT = config['PUB_KEY_BOT']

contract_src = 'src/contracts/'

hackers = [PUB_KEY_LEADER, PUB_KEY_RIGHT_HAND, PUB_KEY_HERO]
# Contract state information, used to deploy and then store the contract addresses
contracts = {
    'EvilHackerDAO': {
        'contract': 'EvilHackerDAO',
        'constructor': [hackers],
        'address': ''
    },
    'EvilHackerWallet': {
        'contract': 'EvilHackerWallet',
        'constructor': [PUB_KEY_BOT],
        'address': ''
    }
}

# Fetches the ETH balance of a public key
def get_balance(public_key):
    return w3.eth.get_balance(public_key)

# Generates a public key from a private key
def gen_pub_from_priv(private_key):
    return Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)

# Reads a contract from a file and returns the contract interface that contains the ABI and bytecode
def get_contract_interface(contract_name: str):
    with open(contract_src + contract_name + ".sol", 'r') as f:
        contract_data = f.read()

    compiled_contract = compile_source(contract_data)
    contract_id, contract_interface = compiled_contract.popitem()
    return contract_interface

# Returns a smart contract object using the interface. It then stores and returns the contract address
def get_w3_contract(contract_name: str):
    contract_interface = get_contract_interface(contract_name)
    return w3.eth.contract(address=contracts[contract_name]['address'], abi=contract_interface['abi'])

# Deploys a contract (from the account bot) and returns the contract address
def deploy_contract(contract_name):
    contract = contracts[contract_name]['contract']
    args = contracts[contract_name]['constructor']

    contract_interface = get_contract_interface(contract)

    tx_hash = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']).constructor(*args).transact({'from': PUB_KEY_BOT})

    w3.eth.wait_for_transaction_receipt(tx_hash)

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    contracts[contract_name]['address'] = address
    return address

# Deploys all contracts and writes the addresses to a json file
def deploy_contracts():
    contracts = ['EvilHackerDAO', 'EvilHackerWallet']

    address1 = deploy_contract(contracts[0])
    address2 = deploy_contract(contracts[1])

    addresses = [address1, address2]

    # Write the addresses as {contract_name: address} to a json file
    with open('src/contracts.json', 'w') as f:
        f.write('{\n')
        for i in range(len(contracts)):
            f.write(f'"{contracts[i]}": "{addresses[i]}"')
            if i != len(contracts) - 1:
                f.write(',\n')
        f.write('\n}')

    return addresses

# Transfers hacker tokens between two addresses. Transaction is signed by the bot
def transfer_tokens(from_address: str, to_address: str, token_value: int):
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    tx_hash = EvilHackerDao.functions.transfer(from_address, to_address, token_value).transact({'from': PUB_KEY_BOT})

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return hb.hex(tx_hash)

# Updates the owner of the EvilHackerDAO contract. Transaction is signed by the bot
def update_owner():
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    tx_hash = EvilHackerDao.functions.updateOwner().transact({'from': PUB_KEY_BOT})

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return hb.hex(tx_hash)

# Returns the hacker token balance of a public key in the EvilHackerDAO contract
def get_hacker_balance(public_key):
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    balance = EvilHackerDao.functions.getHackerBalance(public_key).call()

    return balance

# Returns the owner of the EvilHackerDAO contract
def get_hacker_owner():
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    owner = EvilHackerDao.functions.owner().call()

    return owner