
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_auth
import sys
import argparse
from nav_1.nav1_dash import get_nav1
from nav_2.nav2_dash import get_nav2

parser = argparse.ArgumentParser(description='Vizdum Dashboard')
parser.add_argument('--debug', action='store_true')

VALID_USERNAME_PASSWORD_PAIRS = {
    "admin": "admin"
}

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

NAVBAR_STYLE = {
    "padding-left": "1rem",
    "width": "100%",
    "background-color": "#f8f9fa",
    "min-height": "7vh",
}

CONTENT_STYLE = {"position": "relative", "border-top": "1px solid darkgray"}

def get_navbar():
    navbar = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Nav1", href="/nav_1",
                                active="partial"),
                    dbc.NavLink("Nav2", href="/nav_2", active="partial"),
                ],
                pills=True,
                style={"justify-content": "center", "padding": "0.5em"},
            ),
        ],
        style=NAVBAR_STYLE,
    )

    return navbar

navbar = get_navbar()
nav1 = get_nav1(app)
nav2 = get_nav2(app)
content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), navbar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print("Pathname", pathname)
    if type(pathname) == str:
        if pathname == "/":
            return "Root"
        elif pathname.startswith("/nav_1"):
            return nav1
        elif pathname.startswith("/nav_2"):
            return nav2
      
       


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    app.run_server(host="0.0.0.0", port=8080, debug=True)
