from flask import Flask, render_template
from paillier import Paillier
import blockchain_handler as bh
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__)

approved_keys = [config['PRIV_KEY_LEADER'], config['PRIV_KEY_RIGHT_HAND']]

paillier_keys = Paillier()
bh.deploy_contracts()

# curl http://127.0.0.1:5000
@app.route('/')
def home():
    return render_template('index.html')

# curl http://127.0.0.1:5000/game
@app.route('/game')
def game():
    return render_template('game.html')

# curl http://127.0.0.1:5000/hint
@app.route('/hint')
def hint():
    return render_template('hint.html')

# curl http://127.0.0.1:5000/info
@app.route('/info')
def hacker_info():
    return render_template('info.html')

# curl http://127.0.0.1:5000/encrypt/10
@app.route('/encrypt/<int:tokens>')
def encrypt(tokens):
    return str(paillier_keys.encrypt(tokens))

# curl http://127.0.0.1:5000/decrypt/$PRIV_KEY_RIGHT_HAND/${ENCRYPTED_VALUE}
@app.route('/decrypt/<string:key>/<int:encrypted_value>')
def dec_tokens(key, encrypted_value):
    if key not in approved_keys:
        return 'Invalid key'

    token_value = paillier_keys.decrypt(encrypted_value)
    return str(token_value)

# curl http://127.0.0.1:5000/balance/$PUB_KEY_HERO
@app.route('/balance/<string:address>')
def hacker_balance(address):
    hacker_balance = bh.get_hacker_balance(address)
    return str(hacker_balance)

# curl http://127.0.0.1:5000/owner
@app.route('/owner')
def get_owner():
    hacker_owner = bh.get_hacker_owner()
    return str(hacker_owner)

# curl http://127.0.0.1:5000/trade/$PRIV_KEY_RIGHT_HAND/$PUB_KEY_HERO/${ENCRYPTED_VALUE}
@app.route('/trade/<string:from_key>/<string:to_address>/<int:encrypted_token_value>')
def trade(from_key, to_address, encrypted_token_value):
    token_value = int(dec_tokens(from_key, encrypted_token_value))
    from_address = bh.gen_pub_from_priv(from_key)
    tx_hash= bh.transfer_tokens(from_address, to_address, token_value)
    return tx_hash

# curl http://127.0.0.1:5000/update
@app.route('/update')
def update_owner():
    tx_hash = bh.update_owner()

    return tx_hash

if __name__ == '__main__':
    app.run()