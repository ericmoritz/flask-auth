from flaskext.auth.backends import mongoengine_auth
from flaskext.auth import utils
from flaskext.auth.tests.backends.base import PasswordBackendMixIn
from flask import (current_app, Flask)
import unittest
from mongoengine import connect
import os


app = Flask(__name__)


if raw_input("This test alters mongodb's test.users collection, is that ok? [y/n] ").lower() != 'y':
    assert False, "Can't alter test.users"


class TestMongoengineBackend(PasswordBackendMixIn,unittest.TestCase):
    app = app
    backend = mongoengine_auth.MongoEngineAuth()

    def setUp(self):
            
        connect("test")

        self.user = mongoengine_auth.User(username="superuser")
        self.user.set_password("password")
        self.user.save()


    def tearDown(self):
        self.user.delete()


class TestUser(unittest.TestCase):
    def test_set_password(self):
        user = mongoengine_auth.User(username="superuser")
        user.set_password("password")

        self.assertTrue(utils.check_password("password", user.password))

    def test_check_password(self):
        user = mongoengine_auth.User(username="superuser")
        user.set_password("password")

        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.check_password("notpassword"))        
