from flask import (session, g, request_started, current_app)
from contextlib import contextmanager


def auth_onrequest(sender):
    backend = current_app.config['AUTH_BACKEND']

    try:
        auth_key = session['auth_key']
    except KeyError:
        return

    user = backend.load_user(auth_key)
    g.user = user


@contextmanager
def setup(app):
    # __enter__
    request_started.connect(auth_onrequest, app)

    @app.context_processor
    def auth_context_processor():
        try:
            return {'user': g.user }
        except AttributeError:
            return {}

    yield app
