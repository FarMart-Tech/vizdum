

from dash import Dash, html, dcc, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pytz import timezone
import numpy as np
from .data import side_2_db


from datetime import datetime



WIDGET_ID = 'side2_'

def side2_demo(app):
    side2 = html.Div([
    html.H4('Example of cloropleth'),
    html.P("Select a option:"),
    dcc.RadioItems(
        id=f'{WIDGET_ID}candidate', 
        options=["Joly", "Coderre", "Bergeron"],
        value="Coderre",
        inline=True
    ),
    dcc.Graph(id=f'{WIDGET_ID}graph'),])



    @app.callback(
    Output(f'{WIDGET_ID}graph', "figure"), 
    Input(f'{WIDGET_ID}candidate', "value"))
    def display_choropleth(candidate):
        df = side_2_db() # replace with your own data source
        geojson = px.data.election_geojson()
        fig = px.choropleth(
            df, geojson=geojson, color=candidate,
            locations="district", featureidkey="properties.district",
            projection="mercator", range_color=[0, 6500])
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    return side2

    
    
