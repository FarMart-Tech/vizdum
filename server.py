"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
from auth import db
from auth.permissions import set_user_access_permissions
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from auth.models import User
from auth.config import GOOGLE_CLIENT_ID
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, AUTH_METHOD


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    assets = Environment()
    assets.init_app(app)

    # Flask Login Stuff
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    if AUTH_METHOD == 'O_AUTH':
        from auth.googe_oauth import auth as auth_blueprint
    elif AUTH_METHOD == 'USER_PASS':
        from auth.user_pass_auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    set_user_access_permissions(app)

    with app.app_context():
        # Import Dash application
        from dashboard.app import create_app

        app = create_app(app)

        return app


if __name__ == "__main__":
    app = init_app()
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
