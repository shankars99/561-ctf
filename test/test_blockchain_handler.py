import unittest
import sys
import os

try:
    sys.path.insert(0, os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), 'src'))
    import blockchain_handler as bh
except ImportError:
    print("Error: failed to import module")
    sys.exit(1)

pub_key_leader = '0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577'
pub_key_right_hand = '0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783'
pub_key_bot = '0x5B0331ED799637DF524bbFC7943f112fB7354a86'
pub_key_hero = '0xd5DA4652E012e5629A3491616cC89F4E7339bA05'
priv_key_bot = '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a'

totalAmount = 100
leaderAmount = 49
rightHandAmount = 45
heroAmount = 6

class TestKeyDerivation(unittest.TestCase):
    def test_gen_pub_from_priv(self):
        self.assertEqual(bh.gen_pub_from_priv(priv_key_bot), pub_key_bot)

class TestETHBalance(unittest.TestCase):
    def test_test_balance(self):
        self.assertEqual(bh.get_balance(pub_key_right_hand), 101*10**18)

class TestContractDeployment(unittest.TestCase):
    def test_deploy_contract(self):
        self.assertIsNotNone(bh.deploy_contracts())

class TestBalance(unittest.TestCase):
    def setUp(self):
        bh.deploy_contracts()

    def test_balances(self):
        self.assertEqual(bh.get_hacker_balance(pub_key_right_hand), rightHandAmount)
        self.assertEqual(bh.get_hacker_balance(pub_key_leader), leaderAmount)

    def test_update_balances(self):
        self.assertEqual(bh.get_hacker_balance(pub_key_right_hand), rightHandAmount)
        self.assertIsNotNone(bh.transfer_tokens(pub_key_right_hand, pub_key_leader, 1))
        self.assertEqual(bh.get_hacker_balance(pub_key_right_hand), rightHandAmount-1)
        self.assertEqual(bh.get_hacker_balance(pub_key_leader), leaderAmount+1)

if __name__ == '__main__':
    unittest.main()