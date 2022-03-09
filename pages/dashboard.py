from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
from server import app
import index




dashboard = html.Div([
    html.H1("Dashboard", className="display-2 mb-5 "),
    html.Hr(),
    html.P("opsies usually occur with 2 things wrong file input the table format does not have the right headers"),
    dbc.Button("Test")
], id="dashboard-div")

@app.callback(
    Output("dashboard-div", 'children'),
    Input("test-button", "n_clicks")
)
def test_callback(n):
    if n > 0:
        return html.H1("test works!!!")
