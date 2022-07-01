from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pytz import timezone
import numpy as np
#from .data import side_2_db


from datetime import datetime



WIDGET_ID = 'n1side2_'

def side2_demo(app):
    n1side2 = html.Div([
    html.H4('Interactive normal distribution'),
    dcc.Graph(id=f"{WIDGET_ID}graph"),
    html.P("Mean:"),
    dcc.Slider(id=f"{WIDGET_ID}mean", min=-3, max=3, value=0, 
               marks={-3: '-3', 3: '3'}),
    html.P("Standard Deviation:"),
    dcc.Slider(id=f"{WIDGET_ID}std", min=1, max=3, value=1, 
               marks={1: '1', 3: '3'}),
])


    @app.callback(
    Output(f"{WIDGET_ID}graph", "figure"), 
    Input(f"{WIDGET_ID}mean", "value"), 
    Input(f"{WIDGET_ID}std", "value"))
    def display_color(mean, std):
        data = np.random.normal(mean, std, size=500) # replace with your own data source
        fig = px.histogram(data, range_x=[-10, 10])
        return fig
    return n1side2
