# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from .config import GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
import json
import requests
from oauthlib.oauth2 import WebApplicationClient
# OAuth 2 client setup

client = WebApplicationClient(GOOGLE_CLIENT_ID)
auth = Blueprint('auth', __name__)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def ensure_https(url):
    return url.replace('http://', 'https://')


google_provider_cfg = get_google_provider_cfg()
authorization_endpoint = google_provider_cfg["authorization_endpoint"]
token_endpoint = google_provider_cfg["token_endpoint"]


@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    else:
        return render_template('index.jinja2')


@auth.route('/login')
def login():
    # OAuth
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    redirect_uri = request.base_url + "/callback"
    redirect_uri = ensure_https(redirect_uri)
    print(redirect_uri)
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    print("Preparing token request")
    print(request.url)
    print(request.base_url)
    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=ensure_https(request.url),
        redirect_url=ensure_https(request.base_url),
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    print(userinfo_response.json())
    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    user_info = userinfo_response.json()
    if user_info.get("email_verified"):
        unique_id = user_info["sub"]
        users_email = user_info["email"]
        full_name = user_info["name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Checking if the user exists in our DB
    user = User.query.filter_by(email=users_email).first()
    if not user:
        # This is a new user
        # Create a user in our db with the information provided
        # by Google
        user = User(email=users_email, name=full_name,
                    password=unique_id)

        # add the new user to the database
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("/dashboard")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
