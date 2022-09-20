import dash_mantine_components as dmc
from dash import Input, Output, State, dcc, html
from dash_iconify import DashIconify

load_modal = html.Div(
    children=[
        dmc.Modal(
            ["apsoidufaspodif"],
            id="load-modal",
        ),
    ]
)
