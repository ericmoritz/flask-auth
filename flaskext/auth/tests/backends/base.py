from flaskext.auth.backends import base
import unittest
import mock


class TestBaseBackend(unittest.TestCase):
    
    def test_base(self):
        base_backend = base.AuthBackend()

        self.assertRaises(NotImplementedError, base_backend.authenticate, {})
        self.assertRaises(NotImplementedError, base_backend.load_user,
                          "auth_key")
        self.assertEqual(base_backend.logout("auth_key"), None)


class PasswordBackendMixIn(object):
    """A mixin that tests username/password based authentication backends

    Just set three attributes, app, user and backend
    """
    app = None
    user = None
    backend = None

    def test_authenticate_good(self):
        fixture = {'username': 'superuser',
                   'password': 'password'}

        expect = "superuser"

        with self.app.test_request_context("/"):
            result = self.backend.authenticate(fixture)
        
        self.assertEqual(expect, result)


    def test_authenticate_baddata(self):
        fixture = {'username': 'superuser'} # whoops, I forgot the password
        expect = None

        with self.app.test_request_context("/"):
            result = self.backend.authenticate(fixture)

        self.assertEqual(expect, result)

    def test_authenticate_badusername(self):
        fixture = {'username': 'superuserer',
                   'password': 'password'}

        expect = None

        with self.app.test_request_context("/"):
            result = self.backend.authenticate(fixture)

        self.assertEqual(expect, result)

    def test_authenticate_badpassword(self):
        fixture = {'username': 'superuser',
                   'password': 'notpassword'}

        expect = None

        with self.app.test_request_context("/"):
            result = self.backend.authenticate(fixture)

        self.assertEqual(expect, result)
        

    def test_get_user(self):
        expect = self.user
        with self.app.test_request_context("/"):
            result = self.backend.load_user("superuser")
        self.assertEqual(expect, result)

    def test_get_user_unknown(self):
        expect = self.user
        with self.app.test_request_context("/"):
            result = self.backend.load_user("superuser")
        self.assertEqual(expect, result)
