from web3 import Web3
from paillier_crypto import Paillier
from dotenv import dotenv_values
config = dotenv_values(".env")

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

PUB_KEY_LEADER = config['PUB_KEY_LEADER']
PUB_KEY_RIGHT_HAND = config['PUB_KEY_RIGHT_HAND']
PUB_KEY_HERO = config['PUB_KEY_HERO']
PUB_KEY_BOT = config['PUB_KEY_BOT']

PRIV_KEY_LEADER = config['PRIV_KEY_LEADER']
PRIV_KEY_RIGHT_HAND = config['PRIV_KEY_RIGHT_HAND']

hackers = [PUB_KEY_LEADER, PUB_KEY_RIGHT_HAND, PUB_KEY_HERO]
approved_keys = [PRIV_KEY_LEADER, PRIV_KEY_RIGHT_HAND]

paillier = Paillier()

votes_map = {
    PUB_KEY_LEADER: paillier.encrypt(44),
    PUB_KEY_RIGHT_HAND: paillier.encrypt(40),
    PUB_KEY_HERO: paillier.encrypt(6)
}

# Generates a public key from a private key
def gen_pub_from_priv(private_key):
    return Web3.to_checksum_address(w3.eth.account.from_key(private_key).address)

def compute_owner():
    max_votes = 0
    owner = None
    for hacker in hackers:
        hacker_balance = paillier.decrypt(votes_map[hacker])
        if  hacker_balance > max_votes:
            max_votes = hacker_balance
            owner = hacker
    return owner

def get_hacker_balance(hacker):
    return votes_map[hacker]


def encrypt_votes(tokens):
    return paillier.encrypt(tokens)

def decrypt_votes(key):
    pub_key = gen_pub_from_priv(key)
    return paillier.decrypt(votes_map[pub_key])

def trade_votes(from_hacker_priv_key, to_hacker_pub_key, encrypted_amount):
    from_hacker_pub_key = gen_pub_from_priv(from_hacker_priv_key)

    if decrypt_votes(from_hacker_priv_key) < paillier.decrypt(encrypted_amount):
        return 'Underflow'

    votes_map[from_hacker_pub_key] = paillier.sub(votes_map[from_hacker_pub_key], encrypted_amount)
    votes_map[to_hacker_pub_key] = paillier.add(votes_map[to_hacker_pub_key], encrypted_amount)
    return True

def return_pub_key():
    return paillier.pub_key

def return_private_key():
    return paillier.priv_key