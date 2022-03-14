from gc import callbacks
from click import option
from dash import Input, Output, State, dcc, html, dash_table, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go 
import pandas as pd
#from index import app, config
from pages import dashboard
#from src import db_loader
import json

layout = html.Div([
    dcc.Store(id="page_storage", storage_type="session"),
    html.H1("Analysis", className="display-2 mb-5 "),
    html.Hr(),
    html.Div(id="table_div"),
    dbc.Button("make H1", id="make_H1"),
], id="analysis_div")

@callback(
Output('table_div', 'children'),
Input('main_store', 'data'), 
)
def definition(data):
    if data is not None:
        df = pd.read_json(data, orient="split")
        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()

        return html.Div([
            html.H3("Structure Schedule"),
            dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size= 15,
            ),
            greenbook_card
        ])


    elif data is None: dbc.Alert(
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

stuff=[
    {"label": "Option 1", "value": "1"},
    {"label": "Option 2", "value": "2"},
    {"label": "Option 3", "value": "3"},
    {"label": "Option 4", "value": "4"},
]

table_header = [html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon")]))]
row1 = html.Tr([
    html.Td(
        dbc.Select(options=stuff, value="1")
    ), 
    html.Td("Dent")
    ])
row2 = html.Tr([
    html.Td(
        dbc.Select(options=stuff, value="2")
    ), 
    html.Td("Prefect")
    ])
row3 = html.Tr([
    html.Td(dbc.Select(options=stuff, value="1")), 
    html.Td("Beeblebrox")
    ])
table_body = [html.Tbody([row1, row2, row3])]

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

greenbook_card = dbc.Card([
    html.H3("Green Book Database", className="mb-3"),
    html.Div([
        dbc.Table(
            table_header + table_body, 
            striped=True, 
            bordered=True, 
            hover=True,
            style = {"width": "75%"}
            ),
        dcc.Graph(figure = fig)
    ], className="hstack"),
],
class_name="my-5 p-4 shadow"
)
