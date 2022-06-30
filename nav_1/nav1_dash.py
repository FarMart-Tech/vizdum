from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .side_1.index import side1_demo
from .side_2.index import side2_demo

WIDGET_ID = 'nav1_'

SIDEBAR_STYLE = {
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "padding": "2rem 1rem",
    "flex-grow": "1"
}

LAYOUT_STYLE = {
    "display": "flex",
    "min-height": "93vh"
}

def get_nav1(app):

    sidebar = dbc.Nav(
        [
            dbc.NavLink("Side_1",
                        href="/nav_1/side_1", active="exact"),
            dbc.NavLink("Side_2",
                        href="/nav_1/side_2", active="exact"),
            
        ],
        vertical=True,
        pills=True,
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id=f"{WIDGET_ID}page-content", style=CONTENT_STYLE)

    layout = html.Div([sidebar, content], style=LAYOUT_STYLE)
    s1_n1 = side1_demo(app)
    s2_n2 = side2_demo(app)
    @app.callback(Output(f"{WIDGET_ID}page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/nav_1/side_1":
            return s1_n1
        elif pathname == "/nav_1/side_2":
            return s2_n2
   
        else:
            return 'No result'
        

    return layout