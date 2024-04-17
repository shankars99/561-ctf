from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to this Crypto CTF designed by Shankar.'

@app.route('/hint')
def poem():
    return 'Jack and Jill went up a hill <br> To fetch a pailer water. <br> (there might be a hint in the poem)'

@app.route('/crypto')
def calculator():
    return render_template('enc_dec.html')

@app.route('/crypto')
def calculator():
    return render_template('enc_dec.html')

if __name__ == '__main__':
   app.run()