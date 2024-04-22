from flask import Flask, render_template
import blockchain_sim as bs
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__)

# curl http://127.0.0.1:5000
@app.route('/')
def home():
    return render_template('index.html')

# curl http://127.0.0.1:5000/api
@app.route('/api')
def api():
    return render_template('api.html')

# curl http://127.0.0.1:5000/game
@app.route('/game')
def game():
    return render_template('game.html')

# curl http://127.0.0.1:5000/hero
@app.route('/hero')
def hero():
    return render_template('hero.html')

# curl http://127.0.0.1:5000/pubkey
@app.route('/pubkey/<string:privkey>')
def get_pub_key(privkey):
    pub_key = str(bs.gen_pub_from_priv(privkey))
    return f'Encrypted value: {pub_key}\n'


# curl http://127.0.0.1:5000/encrypt/10
@app.route('/encrypt/<int:votes>')
def encrypt(votes):
    value = str(bs.encrypt_votes(votes))
    return f'Encrypted value: {value}\n'

# curl http://127.0.0.1:5000/votes/$PRIV_KEY_RIGHT_HAND
@app.route('/votes/<string:key>')
def votes(key):
    value = str(bs.decrypt_votes(key))
    return f'Decrypted value: {value}\n'

# curl http://127.0.0.1:5000/owner
@app.route('/owner')
def get_owner():
    owner = bs.compute_owner()
    return f'Owner: {owner}\n'

# curl http://127.0.0.1:5000/trade/$PRIV_KEY_RIGHT_HAND/$PUB_KEY_HERO/${ENCRYPTED_VALUE}
@app.route('/trade/<string:from_hacker_priv_key>/<string:to_hacker_pub_key>/<int:encrypted_token_value>')
def trade(from_hacker_priv_key, to_hacker_pub_key, encrypted_token_value):
    state = str(bs.trade_votes(from_hacker_priv_key, to_hacker_pub_key, encrypted_token_value))
    return f'Trade successful: {state}\n'

# curl http://127.0.0.1:5000/enckey
@app.route('/enckey')
def getenckey():
    pub_key = bs.return_pub_key()
    return f'Public key: {pub_key}\n'

# curl http://127.0.0.1:5000/enckey/$PRIV_KEY_RIGHT_HAND
@app.route('/deckey/<string:from_hacker_priv_key>')
def gedectkey(from_hacker_priv_key):
    pub_key = str(bs.gen_pub_from_priv(from_hacker_priv_key))
    owner = bs.compute_owner()
    if pub_key == owner:
        private_keys = bs.return_private_key()
        return f'Private keys of the system are: {private_keys}\n'
    return f'User is not owner\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)