import datetime

import dash_mantine_components as dmc
import requests
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from src import firebase_init, save_file

load_layout = html.Div(
    children=[
        dmc.Center(
            children=[
                dmc.Group(
                    children=[
                        dmc.Select(
                            label="Project name:",
                            id="load-project-name",
                            description="Select a project to load",
                            placeholder="Select a project",
                            searchable=True,
                        ),
                        dmc.Select(
                            label="Variation name:",
                            id="load-variation-name",
                            description="Select a variation to load",
                            disabled=True,
                            placeholder="Select a variation",
                            data=[
                                {"value": "react", "label": "React"},
                                {"value": "ng", "label": "Angular"},
                                {"value": "svelte", "label": "Svelte"},
                                {"value": "vue", "label": "Vue"},
                            ],
                        ),
                    ],
                    direction="column",
                )
            ],
        ),
        dmc.Button(
            "Load",
            id="load-data-button",
        ),
        html.Div(id="test-div"),
        dcc.Store(id="load-data-store"),
    ]
)

load_modal = html.Div(
    children=[
        dmc.Modal(
            load_layout,
            id="load-modal",
        ),
    ]
)

# ----- Enable/disable vation selection -----
@callback(
    Output("load-variation-name", "disabled"),
    Input("load-project-name", "value"),
    prevent_initial_call=True,
)
def update_variation_disable(val):
    if val is not None:
        return False
    else:
        return True


# ----- enable/disable load button -----
@callback(
    Output("load-data-button", "disabled"),
    Input("load-variation-name", "value"),
    State("load-project-name", "value"),
    prevent_initial_call=True,
)
def update_load_button_disable(val1, val2):
    if val1 is not None and val2 is not None:
        return False
    else:
        return True


# ----- project name select data update -----
@callback(
    Output("load-project-name", "data"),
    Input("load-button", "n_clicks"),
    State("firebase_storage", "data"),
    prevent_initial_call=True,
)
def update_project_name_select_data(n_clicks, data):
    return save_file.data_to_key_options(data)


# ----- variation name select data update -----
@callback(
    Output("load-variation-name", "data"),
    Input("load-project-name", "value"),
    State("firebase_storage", "data"),
    prevent_initial_call=True,
)
def update_variation_name_select_data(val, data):
    variations = []
    if data is not None:
        for items in data[val]:
            variations.append({"value": items, "label": items})
        return variations
    else:
        raise PreventUpdate


# # ----- loading logic -----
# @callback(
#     Output("main_store", "data"),
#     Input("load-data-button", "n_clicks"),
#     State("load-project-name", "value"),
#     State("load-variation-name", "value"),
#     prevent_initial_call=True,
# )
# def load_data(n_clicks, project_name, variation_name):
#     blob = firebase_init.bucket.blob("{}+{}.json".format(project_name, variation_name))
#     link = blob.generate_signed_url(datetime.timedelta(seconds=300), method="GET")
#     data = requests.get(link).json()
#     return data
