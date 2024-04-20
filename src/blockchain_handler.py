from web3 import Web3
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
pub_key_head = '0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577'
pub_key_right_hand = '0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783'


public_key_bot = '0x5B0331ED799637DF524bbFC7943f112fB7354a86'
private_key_bot = '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a'

path_to_deploy = 'src/contracts/'
contracts = ['EvilHackerDAO', 'EvilHackerWallet']
hackers = [pub_key_head, pub_key_right_hand]

contracts = {
    'EvilHackerDAO': {
        'contract': 'EvilHackerDAO',
        'constructor': [hackers],
        'address': ''
    },
    'EvilHackerWallet': {
        'contract': 'EvilHackerWallet',
        'constructor': [public_key_bot],
        'address': ''
    }
}

def get_balance(public_key):
    return w3.eth.get_balance(public_key)

def gen_pub_from_priv(private_key):
    return Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)

def read_contract(contract_name: str):
    with open(path_to_deploy + contract_name + ".sol", 'r') as f:
        contract_data = f.read()

    compiled_contract = compile_source(contract_data)
    contract_id, contract_interface = compiled_contract.popitem()
    return contract_interface

def get_w3_contract(contract_name: str):
    contract_interface = read_contract(contract_name)
    return w3.eth.contract(address=contracts[contract_name]['address'], abi=contract_interface['abi'])

def deploy_contract(contract_name):
    contract = contracts[contract_name]['contract']
    args = contracts[contract_name]['constructor']

    contract_interface = read_contract(contract)

    tx_hash = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']).constructor(*args).transact({'from': public_key_bot})

    w3.eth.wait_for_transaction_receipt(tx_hash)

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    contracts[contract_name]['address'] = address
    return address


def deploy_contracts():
    contracts = ['EvilHackerDAO', 'EvilHackerWallet']

    address1 = deploy_contract(contracts[0])
    address2 = deploy_contract(contracts[1])

    addresses = [address1, address2]

    # create a json and write the addresses as {contract_name: address}
    with open('src/contracts.json', 'w') as f:
        f.write('{\n')
        for i in range(len(contracts)):
            f.write(f'"{contracts[i]}": "{addresses[i]}"')
            if i != len(contracts) - 1:
                f.write(',\n')
        f.write('\n}')

    return addresses

def transfer_tokens(from_address: str, to_address: str, token_value: int):
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    tx_hash = EvilHackerDao.functions.transfer(from_address, to_address, token_value).transact({'from': public_key_bot})

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash

def get_hacker_balance(public_key):
    contract = 'EvilHackerDAO'

    EvilHackerDao = get_w3_contract(contract)
    balance = EvilHackerDao.functions.getHackerBalance(public_key).call()

    return balance

