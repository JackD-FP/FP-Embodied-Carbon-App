import base64
import io

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import openpyxl  # just so excel upload works
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from src import comparison_cards_01, comparison_cards_02, uploader

layout = html.Div([
    html.H1("Comparison", className="display-2 mb-5 "),
    html.Hr(className="my-5"),
    dbc.Container([
        dbc.Row([

            # ---------- card 01 -----------
            dbc.Col([
                dbc.Card([ # card 01
                    html.Div(id='comp_title', className='my-3'),
                    dmc.Divider(variant="solid", class_name="mb-3"),
                    comparison_cards_01.card01
                ], 
                class_name='shadow p-4',)
            ], width=4,),

            # ---------- card 02 -----------
            dbc.Col([
                dbc.Card([ # card 02
                    comparison_cards_02.card02,
                    ],
                    class_name='shadow p-4')
            ], width=4),

            # ---------- card 03 -----------
            dbc.Col([
                dbc.Card([ # card 03
                    dcc.Upload(
                        dmc.Tooltip(
                            label="upload a different project to compare",
                            transition="pop",
                            transitionDuration=300,
                            transitionTimingFunction="ease",
                            children=[
                                    dmc.Button(
                                        html.I(className="bi bi-cloud-upload"),
                                        radius="xl",
                                        size="md",
                                        class_name="shadow-sm",
                                        id=""
                                    )                             
                            ], class_name='position-absolute translate-middle',
                            style={'zIndex':'5', 'left':'98%', 'top':'10%'}
                        ),
                        id="upload_card03" 
                    ),
                        html.P("Add Another Project you want to compare with", className="text-center"),
                        html.Div(id="test-card03")
                ], class_name='shadow p-4')
            ], width=4,),
        ])
    ], fluid=True)
], id="comp-div")

@callback(
Output('comp_title', 'children'),
Input('project_name', 'modified_timestamp'), 
State('project_name', 'data')
)
def card1_title_update(mts, data):
    if data is None or mts is None:
        return html.H3([
                "No Name Project", 
                html.P([
                    "Give it a name in the Dashboard."
                    ], className="fs-5 mt-3")
                    ], 
                    className="display-5")
    else: 
        if data == "":
            return html.H3([
                "No Name Project", 
                html.P([
                    "Give it a name in the Dashboard."
                    ], className="fs-5 mt-3")
                    ], 
                    className="display-5")
        else:
            return html.H3(data, className="display-5")
    