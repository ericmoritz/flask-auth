
class AuthBackend(object):
    def authenticate(self, data):
        raise NotImplementedError

    def logout(self, auth_key):
        pass

    def load_user(self, auth_key):
        raise NotImplementedError
