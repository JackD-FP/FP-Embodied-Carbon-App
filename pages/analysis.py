from gc import callbacks
from click import option, style
from dash import Input, Output, State, dcc, html, dash_table, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go 
import pandas as pd
import numpy as np
from src import greenbook_options
from src import analysis_cards
from pages import dashboard
import json

gb_df = pd.read_csv("src/Greenbook _reduced.csv")

layout = html.Div([
    dcc.Store(id="page_storage", storage_type="session"),
    html.H1("Analysis", className="display-2 mb-5 "),
    html.Hr(),
    html.Div(id="table_div"),
], id="analysis_div")

@callback(
Output('table_div', 'children'),
Input('main_store', 'data'), 
)
def definition(data):
    if data is not None:
        df = pd.read_json(data, orient="split")
        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        df = df.drop(columns=["Complex Profile", "Structure"])

        return html.Div([
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
            analysis_cards.greenbook_card,
            analysis_cards.epic_card,
        ])

    elif data is None: dbc.Alert( #not sure why this is not working
            [
                html.H1("UPLOAD you schule"),
                html.Hr(),
                html.P("please upload your structure schedule in the dashboard page", className="h4"),
                html.P("Happy designing! 😁")
            ], 
            is_open=True, 
            dismissable=True,
            # className= "fixed-top w-25 mt-5 p-3",
            # style = {
            #     "zIndex": "2",
            #     "marginLeft": "73%",
            # },
        ),

