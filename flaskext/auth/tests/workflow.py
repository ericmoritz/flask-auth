from flask import (session, g, current_app, Flask, url_for)
from flaskext.auth.backends import conf
from flaskext.auth import setup
from flaskext.auth import views

import unittest

app = Flask(__name__)

class TestLoginLogout(unittest.TestCase):
    def setUp(self):
        app.config['AUTH_BACKEND'] = conf.ConfBackend()
        app.config['SECRET_KEY'] = "eoustnoheusnth34snph',eunshtaoeun'ht34nuht"
        app.config['AUTH_USERS'] = {
            'superuser': {
                'password':\
                    'sha1$02da8$fd82a5c0083656bdd157782e9ad8d9bf4fbc5c3e'
                }
            }
        app.debug = True

        # Setup auth on the test app
        with setup(app):
            pass

        # Install the default flask-auth views
        app.register_module(views.mod, url_prefix="/account")

    def login(self, c, username, password, next=None):
        url = url_for("auth.login")
        if next:
            url += "?next=" + next

        return c.post(url,
                    data={
                'username': username,
                'password': password
                })

    def logout(self, c):
        url = url_for("auth.logout")
        return c.get(url)

    def test_check_next(self):
        self.assertEqual(views.check_next("/"), "/")
        self.assertEqual(views.check_next("/view/?param=http://example.com"),
                         "/view/?param=http://example.com")
        self.assertEqual(views.check_next("http://www.google.com/"), None)
        self.assertEqual(views.check_next(" "), None)



    def test_login(self):
        with app.test_request_context():
            with app.test_client() as c:
                rv = self.login(c, 'superuser', 'password')
                result = session['auth_key']

        expect = 'superuser' # Conf backend uses the username as the auth_key
        
        self.assertEqual(expect, result)

    def test_login_redirect(self):
        with app.test_request_context():
            with app.test_client() as c:
                rv = self.login(c, 'superuser', 'password',
                                next="/")
                self.assertEqual(rv.headers['location'], 'http://localhost/')
                result = session['auth_key']


        expect = 'superuser' # Conf backend uses the username as the auth_key
        
        self.assertEqual(expect, result)

    def test_bad_login(self):
        with app.test_request_context():
            with app.test_client() as c:
                rv = self.login(c, 'superuser', 'not-password')
                result = session.get('auth_key', None)

        expect = None # Conf backend uses the username as the auth_key
        
        self.assertEqual(expect, result)

    def test_login_logout(self):
        with app.test_request_context():
            with app.test_client() as c:
                self.login(c, "superuser", "password")
                self.assertEqual(session['auth_key'], 'superuser')
                self.logout(c)
                result = session.get('auth_key', None)

        expect = None # Conf backend uses the username as the auth_key
        
        self.assertEqual(expect, result)

