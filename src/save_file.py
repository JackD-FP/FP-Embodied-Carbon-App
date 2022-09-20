import dash_mantine_components as dmc
import firebase_admin
from dash import Input, Output, State, dcc, html
from dash_iconify import DashIconify
from firebase_admin import credentials, firestore

new_project = dmc.Tab(
    label="New Project",
)
existing_project = dmc.Tab(
    label="Existing Project",
)

save_modal = html.Div(
    children=[
        dmc.Modal(
            [
                dmc.Tabs(
                    color="blue",
                    orientation="horizontal",
                    children=[new_project, existing_project],
                )
            ],
            id="save-modal",
        ),
    ]
)
