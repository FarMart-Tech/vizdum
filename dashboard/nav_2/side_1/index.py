
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






WIDGET_ID = 'side1_'




def side1_demo(app):
    
    side1 = html.Div([
        html.H4('Example of an Interactive Scattter plot'),
        html.P("Select legend position:"),
        dcc.RadioItems(
            id=f'{WIDGET_ID}xanchor', value=0, inline=True,
            options=[{'label': 'left', 'value': 0}, 
                    {'label': 'right', 'value': 1}]
        ),
        dcc.RadioItems(
            id=f'{WIDGET_ID}yanchor', value=1, inline=True,
            options=[{'label': 'top', 'value': 1}, 
                    {'label': 'bottom', 'value': 0}],
        ),
        dcc.Graph(id=f"{WIDGET_ID}graph"),
    ])

    @app.callback(
    Output(f"{WIDGET_ID}graph", "figure"), 
    Input(f"{WIDGET_ID}xanchor", "value"), 
    Input(f"{WIDGET_ID}yanchor", "value"))
    def modify_legend(pos_x, pos_y):
        df = side_1_db()# replace with your own data source
        fig = px.scatter(
            df, x="gdpPercap", y="lifeExp", 
            color="continent", size="pop", 
            size_max=45, log_x=True)
        fig.update_layout(legend_x=pos_x, legend_y=pos_y)
        return fig

    return side1
    













