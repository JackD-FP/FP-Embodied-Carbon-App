import dash_mantine_components as dmc
from dash import Input, Output, State, dcc, html
from dash_iconify import DashIconify

save_modal = html.Div(
    children=[
        dmc.Modal(
            "potato",
        ),
    ]
)
