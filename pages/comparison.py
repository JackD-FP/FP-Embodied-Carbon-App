from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from plotly.subplots import make_subplots
import  plotly.graph_objects as go

from src import comparison_cards

layout = html.Div([
    html.H1("Comparison", className="display-2 mb-5 "),
    html.Hr(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div(id='comp_title', className='my-3'),
                    dmc.Divider(variant="solid", class_name="mb-3"),
                    comparison_cards.card01
                ], 
                class_name='shadow p-3',)
            ], width=4,),
            dbc.Col([
                dbc.Card([
                    html.P("test test test")
                ], class_name='shadow p-3')
            ], width=4,),
            dbc.Col([
                dbc.Card([
                    html.P("test test test")
                ], class_name='shadow p-3')
            ], width=4,),
        ])
    ], fluid=True)
], id="comp-div")

@callback(
Output('comp_title', 'children'),
Input('project_name', 'modified_timestamp'), 
State('project_name', 'data'),
)
def title_update(ts, data):
    val = [html.H3("Unknown"), html.P("You can give it a name in the dashboard", className="text-secondary")]
    if ts is None: 
        return val
    else:
        if data == "":
            return val
        else: return html.H3(data)