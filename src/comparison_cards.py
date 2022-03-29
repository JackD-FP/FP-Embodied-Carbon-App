from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import numpy as np

card01 = html.Div([
    html.Div(id='card01_table')
])

@callback(
Output('card01_table', 'children'),
Input('main_store', 'modified_timestamp'), 
Input('gfa_input', 'value'),
State('main_store', 'data'))
def update_div(mts, data):
    if mts is None: raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        df = df.filter(items=['Building Materials (All)', 'Mass', 'Volume (Net)'])
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)