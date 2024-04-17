import primelibpy
from random import randint
from math import gcd, lcm

'''
Inspired by: https://blog.openmined.org/the-paillier-cryptosystem/
'''
class Paillier:
    def __init__(self, digits=4):
        self.digits = digits
        self.pub_key = {
            "n": None,
            "g": None
        }
        self.priv_key = {
            "lambda": None,
            "mew": None
        }
        self.generate_key()


    def generate_key(self) -> dict:
        def get_random_prime(digits=self.digits):
            return primelibpy.Prime.getRandomPrime("GoodPrime", digits)

        p = get_random_prime()
        q = get_random_prime()

        while gcd(p, q) != 1:
            p = get_random_prime()
            q = get_random_prime()

        n = p*q

        lambd = lcm(p-1, q-1)
        g = randint(1, n**2)

        l = self.L(pow(g, lambd, n**2), n)
        mew = pow(l, -1, n)

        if mew is None:
            self.generate_key()

        self.pub_key["n"] = n
        self.pub_key["g"] = g
        self.priv_key["lambda"] = lambd
        self.priv_key["mew"] = mew

        return {"pub": self.pub_key, "priv": self.priv_key}

    def encrypt(self, m: int) -> int:
        n = self.pub_key["n"]
        g = self.pub_key["g"]
        r = randint(1, n)

        c = (pow(g, m, n**2) * pow(r, n, n**2)) % n**2

        return c

    def decrypt(self, c: int) -> int:
        n = self.pub_key["n"]
        lambd = self.priv_key["lambda"]
        mew = self.priv_key["mew"]
        u = pow(c, lambd, n**2)
        m = self.L(u,n)*mew % n
        return m

    def add(self, c1: int, c2: int) -> int:
        n = self.pub_key["n"]
        return (c1 * c2) % n**2

    def sub(self, c1: int, c2: int) -> int:
        n = self.pub_key["n"]
        return (c1 * pow(c2, -1, n**2)) % n**2

    def multiply(self, c: int, k: int) -> int:
        n = self.pub_key["n"]
        return pow(c, k, n**2)

    def divide(self, c: int, k: int) -> int:
        n = self.pub_key["n"]
        return pow(c, -k, n**2)

    def get_pub_key(self):
        return self.pub_key

    def get_priv_key(self):
        return self.priv_key

    def L(self, x, n):
        return (x-1)//n
