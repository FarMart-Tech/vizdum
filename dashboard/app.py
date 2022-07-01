
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_auth
import sys
import argparse
from dashboard.nav_1.nav1_dash import get_nav1
from dashboard.nav_2.nav2_dash import get_nav2
from .config import URL_PREFIX

parser = argparse.ArgumentParser(description='Vizdum Dashboard')
parser.add_argument('--debug', action='store_true')


NAVBAR_STYLE = {
    "padding-left": "1rem",
    "width": "100%",
    "background-color": "rgb(248, 249, 250)",
    "min-height": "7vh",
    "display": "flex",
    "flex-direction": "row",
    "justify-content": "space-around",
    "align-items": "center"
}

CONTENT_STYLE = {"position": "relative", "border-top": "1px solid darkgray"}


def get_navbar():
    navbar = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Nav1", href=f"{URL_PREFIX}/nav_1",
                                active="partial"),
                    dbc.NavLink(
                        "Nav2", href=f"{URL_PREFIX}/nav_2", active="partial"),
                ],
                pills=True,
                style={"justify-content": "center", "padding": "0.5em"},
            ),
            html.A('Logout', href='/logout')

        ],
        style=NAVBAR_STYLE,
    )

    return navbar


def create_app(server):

    # Basic auth
    app = Dash(
        server=server,
        url_base_pathname="/dashboard/",
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    # auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

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
            elif pathname.startswith(f"{URL_PREFIX}/nav_1"):
                return nav1
            elif pathname.startswith(f"{URL_PREFIX}/nav_2"):
                return nav2

    return app.server


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    app.run_server(host="0.0.0.0", port=8080, debug=True)
