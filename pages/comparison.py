from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from plotly.subplots import make_subplots
import  plotly.graph_objects as go

from src import comparison_cards_01, comparison_cards_02

layout = html.Div([
    html.H1("Comparison", className="display-2 mb-5 "),
    html.Hr(),
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
                    dmc.Tooltip(
                        label="upload a different project to compare",
                        transition="pop",
                        transitionDuration=300,
                        transitionTimingFunction="ease",
                        children=[
                            dcc.Upload([
                                dmc.Button(
                                    html.I(className="bi bi-cloud-upload"),
                                    radius="xl",
                                    size="md",
                                    class_name="shadow-sm",
                                    id="card02_upload"
                                ) 
                            ], id="upload_card02"),
                            
                        ], class_name='position-absolute translate-middle',
                        style={'zIndex':'5', 'left':'98%', 'top':'10%'}
                    ),  
                    comparison_cards_02.card02
                    ],
                    class_name='shadow p-4')
            ], width=4, class_name="h-25"),

            # ---------- card 03 -----------
            dbc.Col([
                dbc.Card([ # card 03
                    dmc.Tooltip(
                        label="upload a different project to compare",
                        transition="pop",
                        transitionDuration=300,
                        transitionTimingFunction="ease",
                        children=[
                            dcc.Upload([
                                dmc.Button(
                                    html.I(className="bi bi-cloud-upload"),
                                    radius="xl",
                                    size="md",
                                    class_name="shadow-sm",
                                    id="card03_upload"
                                ) 
                            ], id="upload_card02"),
                            
                        ], class_name='position-absolute translate-middle',
                        style={'zIndex':'5', 'left':'98%', 'top':'10%'}
                    ), 
                        html.P("Add Another Project you want to compare with", className="text-center")
                ], class_name='shadow p-4')
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
        else: return html.H3(data, className="display-5 mb-3")

@callback(
Output('card02_store', 'data'),
Input('card02_upload', 'n_clicks'), 
)
def upload_card01(n):
    return