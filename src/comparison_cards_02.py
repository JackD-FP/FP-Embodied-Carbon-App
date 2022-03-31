import base64
import datetime
import io

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate

from src import uploader

card02 = html.Div([
    html.P("test POTATO test"),
    dcc.Upload(
        id='card2_upload_data',
        children=html.Div([
            dmc.Button(
                    html.I(className="bi bi-cloud-upload"),
                    radius="xl",
                    size="md",
                    class_name="shadow-sm",
                )
        ]),
        className='position-absolute translate-middle',
        style={
            'zIndex':'5', 
            'left':'98%', 
            'top':'10%'
        },
    # Allow multiple files to be uploaded
    multiple=True
    ),
    html.Div(id='card2_output'),
])


@callback(Output('card2_output', 'children'),
              Input('card2_upload_data', 'contents'),
              State('card2_upload_data', 'filename'),
              State('card2_upload_data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            uploader.parse_contents(c, n, d, "card2_temp_store") for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
