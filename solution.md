1. Load the environment variables from the .env file <br> <br>
    `$ source .env`

2. View the owner. This is the same address as the Leader of the DAO. <br> <br>
    `$ curl 127.0.0.1:5000/owner` <br>
    Owner: 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577

3. Get the public key of the cryptosystem. <br> <br>
    `$ curl http://127.0.0.1:5000/enckey` <br>
    Public key: {'n': 49492109, 'g': 967163927424980}

4. Encrypt the value m=40 (student tries random numbers from 0 to 49), because our account is 40 votes short of becoming the leader. <br>
   c = (g^m.r^n) mod n^2 is the encryption formula. <br>
   g and n are from the previous step and r is a random number. <br>
   We also have an endpoint to encrypt the value (note this api is not revealed to the students). <br> <br>
    `$ curl http://127.0.0.1:5000/encryptpailliernotpublic/40` <br>
    Encrypted value: 72640196653196

    ```python
    >>> n = 49492109
    >>> g = 967163927424980
    >>> m = 40
    >>> r = 17
    >>> (pow(g, m, n**2) * pow(r, n, n**2)) % n**2
    435163805563742
    ```

5. The student generates the private key of the right hand. <br> <br>
    ```python
    >>> from hashlib import sha256
    >>> sha256(b'john').hexdigest()
    '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a'
    >>> sha256(b'96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a' + b'doe').hexdigest()
    '3a1b906d49d4314442d61323a2c5b3a98d02033c20f493db0200e84e9cc23416'
    ```

6. Trade the encrypted votes from the right hand to the hero. <br>
   Student gets the hero private key from the /game endpoint. <br> <br>
    `$ curl http://127.0.0.1:5000/trade/$PRIV_KEY_RIGHT_HAND/$PUB_KEY_HERO/{encryptedvalue}` <br>
    Trade successful: True

7. Verify that the owner has been updated to show the hero as the new owner. <br> <br>
    `$ curl 127.0.0.1:5000/owner` <br>
    Owner: 0xd5DA4652E012e5629A3491616cC89F4E7339bA05

8. Get the decryption key that is only available to the owner. <br> <br>
    `$ curl 127.0.0.1:5000/deckey/$PRIV_KEY_HERO` <br>
    Private keys of the system are: {'lambda': 12369504, 'mew': 12369504}

9. To get the flag pass lamba||mew which in our case is 1236950412369504. <br> <br>
    `$ curl http://127.0.0.1:5000/flag/{concat(lambda,mew)}` <br>
    CTF_SDaT{CS561ROCKS}