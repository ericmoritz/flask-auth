from flaskext.auth.backends import conf
from flaskext.auth.tests.backends.base import PasswordBackendMixIn
from flask import (current_app, Flask)
import unittest

app = Flask(__name__)
app.config['AUTH_USERS'] = {
    'superuser': {
        'password': 'sha1$02da8$fd82a5c0083656bdd157782e9ad8d9bf4fbc5c3e'
        }
}

class TestUser(unittest.TestCase):
    def test_equality(self):
        u1 = conf.User('user1',{})
        u2 = conf.User('user1',{'somedata': 'data'})
        u3 = conf.User('user2',{'somedata': 'data'})
        
        self.assertEqual(u1, u2)
        self.assertNotEqual(u1, u3)
        self.assertNotEqual(u1, "something else")

        
class TestConfBackend(PasswordBackendMixIn, unittest.TestCase):
    app = app
    user = conf.User('superuser', app.config['AUTH_USERS']['superuser'])
    backend = conf.ConfBackend()
