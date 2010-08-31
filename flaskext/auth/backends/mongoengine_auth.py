from flaskext.auth.backends.base import AuthBackend
from flaskext.auth import utils
from mongoengine import *

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(default="")

    def set_password(self, password):
        self.password = utils.encode_password(password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        return utils.check_password(raw_password, self.password)        


class MongoEngineAuth(object):
    def authenticate(self, data):
        try:
            username, password = data['username'], data['password']
        except KeyError:
            return None 

        user = User.objects(username=username).first()

        if user is None:
            return None # bad username

        if user.check_password(password):
            return user.username
        else:
            return None # bad password

    def load_user(self, auth_key):
        return User.objects(username=auth_key).first()

    
    
