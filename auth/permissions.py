from flask import request, session, redirect, url_for
from flask_login import login_required
from flask_login import current_user
from werkzeug.local import LocalProxy
from . import db


def set_user_access_permissions(app):
    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.before_request
    def do_something_whenever_a_request_comes_in():
        # request is available
        print(request.args)
        print(request.path)
        if request.path.startswith('/dashboard'):
            print('Hitting the dashboard')
            print(session)
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login", next=request.url))
