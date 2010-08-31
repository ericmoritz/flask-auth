import unittest
from flaskext.auth import utils
import mock
import random


class TestGetHexDigest(unittest.TestCase):
    def test_get_hexdigest(self):
        expect = '59b3e8d637cf97edbe2384cf59cb7453dfe30789'
        result = utils.get_hexdigest("sha1", "salt", "password")
        self.assertEqual(expect, result)


    def test_bad_algo(self):
        self.assertRaises(ValueError, utils.get_hexdigest, 
                          "aesntaosuthasonth", "salt", "password")


class TestCheckPassword(unittest.TestCase):
    def test_check_password(self):
        enc_password = 'sha1$02da8$fd82a5c0083656bdd157782e9ad8d9bf4fbc5c3e'

        self.assertTrue(utils.check_password("password", enc_password))
        self.assertFalse(utils.check_password("notpassword", enc_password))
        

class TestEncodePassword(unittest.TestCase):
    def setUp(self):
        random.random = mock.Mock()
        random.random.return_value = "Something Random"

    def tearDown(self):
        reload(random)

    def test_encodepassword(self):
        result = utils.encode_password("password")
        
        self.assertTrue(utils.check_password("password", result))

    def test_encodepasswordrandom(self):
        "Test that the random salt works correctly"
        reload(random) # Clear the mock
        
        # Two encodings of the same password will be different because the
        # salt will be a different random set of chars
        result1 = utils.encode_password("password")
        result2 = utils.encode_password("password")

        self.assertNotEqual(result1, result2)

    
