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
    dcc.Upload(
        id='card2_upload_data',
        children=html.Div([
            dmc.Tooltip(
                label="fade",
                transition="fade",
                transitionDuration=300,
                transitionTimingFunction="ease",
                children=[
                    dmc.Button(
                        html.I(className="bi bi-cloud-upload"),
                        radius="xl",
                        size="md",
                        class_name="shadow-sm",
                    )
                ],
            )

        ]),
        className='position-absolute translate-middle',
        style={
            'zIndex':'5', 
            'left':'98%', 
            'top':'0%'
        },
    # Allow multiple files to be uploaded
    multiple=True
    ),
    html.Div(id='card2_output'),
    html.Div(id="card2_contents")
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


@callback(
Output('card2_contents', 'children'),
Input('card02_store', 'modified_timestamp'), 
State('card02_store', 'data'),
)
def card2_content_update(mts, data,):
    if data is None or mts is None:
        return html.P("Upload another project to compare with!", className="display-6 text-center fs-4")
    else:
        df = pd.read_json(data, orient="split")
        _df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        _df = _df.filter(items=['Building Materials (All)', 'Mass', 'Volume (Net)'])

        return html.Div([
            html.H3("Comparison 2", className="display-5 my-3"),
            dmc.Divider(class_name="mb-3"),
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
            html.H5(["GFA in m", html.Sup(2)]),
            dbc.Input(
                id="comp_card2_gfa",
                placeholder="GFA?",
                className="w-25",
                type="text",
                debounce=True,
                persistence= True,
                persistence_type="session",
                required=True
            ),
            dmc.Divider(class_name="my-3"),
        ])

