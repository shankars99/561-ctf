from flask import Flask, render_template
import blockchain_sim as bs
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__)

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
    value = str(bs.encrypt_votes(tokens))
    return f'Encrypted value: {value}'

# curl http://127.0.0.1:5000/decrypt/$PRIV_KEY_RIGHT_HAND
@app.route('/decrypt/<string:key>')
def dec_tokens(key):
    value = str(bs.decrypt_votes(key))
    return f'Decrypted value: {value}'

# curl http://127.0.0.1:5000/owner
@app.route('/owner')
def get_owner():
    owner = bs.compute_owner()
    return f'Owner: {owner}'

# curl http://127.0.0.1:5000/trade/$PRIV_KEY_RIGHT_HAND/$PUB_KEY_HERO/${ENCRYPTED_VALUE}
@app.route('/trade/<string:from_hacker_priv_key>/<string:to_hacker_pub_key>/<int:encrypted_token_value>')
def trade(from_hacker_priv_key, to_hacker_pub_key, encrypted_token_value):
    state = str(bs.trade_votes(from_hacker_priv_key, to_hacker_pub_key, encrypted_token_value))
    return f'Trade successful: {state}'

if __name__ == '__main__':
    app.run()