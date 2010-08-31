from flask import (Module, request, abort, current_app, session, flash,
                   redirect, render_template)
import re

mod = Module(__name__, name="auth")

def check_next(next):
    """return the value of next if next is a valid next param,
    it returns None if the next param is invalid"""
    # security check stolen from Django, thanks Django!

    # Try to get the next param 
    # Light security check -- make sure redirect_to isn't garbage.
    if ' ' in next:
        return None
    # Heavier security check -- redirects to http://example.com should
    # not be allowed, but things like /view/?param=http://example.com
    # should be allowed. This regex checks if there is a '//' *before* a
    # question mark.
    elif '//' in next and re.match(r'[^\?]*//', next):
        return None
    else:
        return next


@mod.route("/login/", methods=["GET", "POST"])
def login():
    backend = current_app.config['AUTH_BACKEND']


    next = request.args.get("next", "")
    next = check_next(next)

    # Try to authenticate
    error = None
    if request.method == "POST":
        # Try to authenticate based on the form data
        result = backend.authenticate(request.form)

        # If something is returned, use that as the auth_key in the session
        if result is not None:
            session["auth_key"] = result

            flash("Login successful.")
            if next:
                return redirect(next)
        else:
            flash("Login Invalid", "error")

    return render_template("auth/login.html")

@mod.route("/logout/")
def logout():
    # Get the AUTH_BACKEND
    backend = current_app.config['AUTH_BACKEND']

    auth_key = session.get("auth_key")
    if auth_key:
        next = request.args.get("next", "/")

        # Let the backend know about the logout
        backend.logout(auth_key)

        # Throw away the auth_key
        session.pop("auth_key", None)

    # Flash a pretty message
    flash("You are now logged out")

    return redirect(next)
