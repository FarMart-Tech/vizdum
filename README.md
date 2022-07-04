# vizdum

# Getting Started
Run the server.py file to start the vizdum dashboard.
You can edit basic config in the config.py file

AUTH_METHOD = 'USER_PASS' sets up a basic username and password authentication. However, be careful to add restrictions to allowed users.


AUTH_METHOD = 'O_AUTH' is a google O-Auth flow. Make sure to follow [Google Flask Login](https://realpython.com/flask-google-login/) to setup google OAuth and get client key and secret. Make sure to update auth/config.py file with the information.