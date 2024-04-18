import unittest
import sys
import os

try:
    sys.path.insert(0, os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), 'src'))
    from paillier import Paillier
except ImportError:
    print("Error: failed to import module")
    sys.exit(1)

class TestKeyGen(unittest.TestCase):
    def test_init(self):
        paillier_keys = Paillier()
        self.assertIsNotNone(paillier_keys.pub_key["n"])
        self.assertIsNotNone(paillier_keys.pub_key["g"])
        self.assertIsNotNone(paillier_keys.priv_key["lambda"])
        self.assertIsNotNone(paillier_keys.priv_key["mew"])

    def test_generate_key(self):
        paillier_keys = Paillier()
        keys = paillier_keys.generate_key()
        self.assertIsNotNone(keys)
        self.assertIsNotNone(keys["pub"])
        self.assertIsNotNone(keys["priv"])

class TestEncrypt(unittest.TestCase):
    def test_encrypt(self):
        paillier = Paillier()
        c = paillier.encrypt(10)
        self.assertIsNotNone(c)

    def test_decrypt(self):
        paillier = Paillier()
        c = paillier.encrypt(10)
        m = paillier.decrypt(c)
        self.assertEqual(m, 10)

class TestOperations(unittest.TestCase):
    def test_add(self):
        paillier = Paillier()
        c1 = paillier.encrypt(10)
        c2 = paillier.encrypt(20)
        c = paillier.add(c1, c2)
        m = paillier.decrypt(c)
        self.assertEqual(m, 30)

    def test_sub(self):
        paillier = Paillier()
        c1 = paillier.encrypt(20)
        c2 = paillier.encrypt(10)
        c = paillier.sub(c1, c2)
        m = paillier.decrypt(c)
        self.assertEqual(m, 10)

    def test_multiply(self):
        paillier = Paillier()
        c = paillier.encrypt(10)
        k = 5
        c = paillier.multiply(c, k)
        m = paillier.decrypt(c)
        self.assertEqual(m, 50)

if __name__ == '__main__':
    unittest.main()