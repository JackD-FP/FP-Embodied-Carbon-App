import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
from src import greenbook_options

epic_layout = html.Div(
    children=[
        html.H1("EPiC DB - Analysis", className="display-2 mb-5 "),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        # Beam card
                        dbc.Card("hello"),
                        # column card
                        dbc.Card("hello"),
                        # slab card
                        dbc.Card("hello"),
                        # wall card
                        dbc.Card("hello"),
                        # stairs card
                        dbc.Card("hello"),
                    ]
                ),
                dbc.Col(id="graphs"),
            ]
        ),
    ]
)
