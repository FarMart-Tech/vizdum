from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pytz import timezone
import numpy as np
from .data import side_1_db


from datetime import datetime



WIDGET_ID = 'n1side1_'

def side1_demo(app):
    n1side1 =  html.Div([
    html.H4('Restaurant tips by day of week'),
    dcc.Dropdown(
        id=f"{WIDGET_ID}dropdown",
        options=["Fri", "Sat", "Sun"],
        value="Fri",
        clearable=False,
    ),
    dcc.Graph(id=f"{WIDGET_ID}graph"),
])
    @app.callback(
    Output(f"{WIDGET_ID}graph", "figure"), 
    Input(f"{WIDGET_ID}dropdown", "value"))

    def update_bar_chart(day):
        df = side_1_db() # replace with your own data source
        mask = df["day"] == day
        fig = px.bar(df[mask], x="sex", y="total_bill", 
                    color="smoker", barmode="group")
        return fig
    return n1side1