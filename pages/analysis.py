from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
#from index import app, config
from pages import dashboard

layout = html.Div([
    html.H1("Analysis", className="display-2 mb-5 "),
    html.Hr(),
    html.P("opsies usually occur with 2 things wrong file input the table format does not have the right headers"),
    html.Div(id="analysis_test")
])

# @app.callback(
# Output('analysis_test', 'children'),
# Input('dashboard_store', ''), 
# State('id_1', 'id_1_prop'))
# def definition(input):
#     return