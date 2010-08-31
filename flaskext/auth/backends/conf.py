"""This module authenticates based on the app.conf['AUTH_USERS']
dictionary, use utils.enc_password for generating the password values"""
from flaskext.auth.backends.base import AuthBackend
from flaskext.auth import utils
from flask import current_app


class User(object):
    def __init__(self, username, data):
        self.username = username
        self.__dict__.update(data)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.username == other.username
        else:
            return NotImplemented


class ConfBackend(AuthBackend):
    def authenticate(self, data):
        try:
            username, password = data['username'], data['password']
        except KeyError:
            return # Bad form data, don't authenticate

        users = current_app.config['AUTH_USERS']

        if username in users and utils.check_password(password,
                                                      users[username]['password']):
            return username # Good
        
            
    def load_user(self, auth_key):
        users = current_app.config['AUTH_USERS']
        if auth_key in users:
            return User(auth_key, users[auth_key])
