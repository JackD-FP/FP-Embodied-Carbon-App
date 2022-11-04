import dash
from dash import Input, Output, State, callback, dcc, html
import dash_mantine_components as dmc
from src import firebase_init

layout = html.Div(
    [
        html.H1("Benchmark", className="display-2 mb-5 "),
        html.Hr(className="mb-5"),
        html.Div(),
    ]
)
