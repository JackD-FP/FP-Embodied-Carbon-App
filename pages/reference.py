from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc



layout = html.Div([
    html.H1("Reference", className="display-2 mb-5 "),
    html.Hr(),
    html.P("opsies usually occur with 2 things wrong file input the table format does not have the right headers"),
    dbc.Button("Test")
])

