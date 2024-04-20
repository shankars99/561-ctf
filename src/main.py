from flask import Flask, render_template
from paillier import Paillier
import blockchain_handler as bh

app = Flask(__name__)

approved_keys = ['24871679ddfa877966230f1ff4dbb93616b452c8a251b0c23e631d1c1e36f97d', '3a1b906d49d4314442d61323a2c5b3a98d02033c20f493db0200e84e9cc23416']

paillier_keys = Paillier()
bh.deploy_contracts()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/hint')
def hint():
    return render_template('hint.html')

@app.route('/info')
def hacker_info():
    return render_template('info.html')

@app.route('/encrypt/<int:tokens>')
def encrypt(tokens):
    return str(paillier_keys.encrypt(tokens))

@app.route('/decrypt/<string:key>/<int:encrypted_value>')
def dec_tokens(key, encrypted_value):
    if key not in approved_keys:
        return 'Invalid key'

    token_value = paillier_keys.decrypt(encrypted_value)
    return str(token_value)

@app.route('/balance/<string:address>')
def hacker_balance(address):
    hacker_balance = bh.get_hacker_balance(address)
    return str(hacker_balance)

@app.route('/owner')
def get_owner():
    hacker_owner = bh.get_hacker_owner()
    return str(hacker_owner)

@app.route('/trade/<string:from_key>/<string:to_address>/<int:encrypted_token_value>')
def trade(from_key, to_address, encrypted_token_value):
    token_value = int(dec_tokens(from_key, encrypted_token_value))
    from_address = bh.gen_pub_from_priv(from_key)
    tx_hash= bh.transfer_tokens(from_address, to_address, token_value)
    return tx_hash

@app.route('/update')
def update_owner():
    tx_hash = bh.update_owner()

    return tx_hash

if __name__ == '__main__':
    app.run()