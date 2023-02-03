import datetime

import dash_mantine_components as dmc
import requests
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from src import firebase_init, save_file

delete_layout = html.Div(
    children=[
        dmc.Center(
            children=[
                dmc.Group(
                    children=[
                        dmc.Select(
                            label="Project name:",
                            id="delete-project-name",
                            description="Select a project to delete",
                            placeholder="Select a project",
                            searchable=True,
                        ),
                        dmc.Select(
                            label="Variation name:",
                            id="delete-variation-name",
                            description="Select a variation to delete",
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
                ),
                dmc.Text(id="delete-text"),
            ],
        ),
        dmc.Button(
            "delete",
            id="delete-data-button",
        ),
        html.Div(id="test-div"),
        dcc.Store(id="delete-data-store"),
    ]
)

delete_modal = html.Div(
    children=[
        dmc.Modal(delete_layout, id="delete-modal"),
        html.Div(id="delete-notification-div"),
    ]
)


def get_ID():
    doc_ref = firebase_init.db.collection("projects").stream()
    for doc in doc_ref:
        yield f"{doc.id}"


def get_doc(doc_name):
    doc_ref = firebase_init.db.collection("projects").document(doc_name).stream()
    for doc in doc_ref:
        yield doc


def delete_doc(doc_name):
    doc_ref = firebase_init.db.collection("projects").document(doc_name).delete()
    return doc_ref


@callback(
    Output("delete-project-name", "data"),
    Input("delete-button", "n_clicks"),
)
def update_delete_text(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        ids = get_ID()
        return list(ids)


@callback(
    Output("delete-notification-div", "children"),
    Input("delete-data-button", "n_clicks"),
    State("delete-project-name", "value"),
)
def update_delete_data(n_clicks, val):
    if n_clicks is None:
        raise PreventUpdate
    else:
        delete_doc(val)
        return dmc.Notification(
            title="Data deleted successfully",
            message="Project: {} has been deleted".format(val),
            action="show",
            id="delete-notification",
            icon=[DashIconify(icon="mdi:trash-can-outline")],
        )


# # ----- Enable/disable vation selection -----
# @callback(
#     Output("delete-variation-name", "disabled"),
#     Input("delete-project-name", "value"),
#     prevent_initial_call=True,
# )
# def update_variation_disable(val):
#     if val is not None:
#         return False
#     else:
#         return True


# # ----- enable/disable delete button -----
# @callback(
#     Output("delete-data-button", "disabled"),
#     Input("delete-variation-name", "value"),
#     State("delete-project-name", "value"),
#     prevent_initial_call=True,
# )
# def update_delete_button_disable(val1, val2):
#     if val1 is not None and val2 is not None:
#         return False
#     else:
#         return True


# # ----- project name select data update -----
# @callback(
#     Output("delete-project-name", "data"),
#     Input("delete-button", "n_clicks"),
#     State("firebase_storage", "data"),
#     prevent_initial_call=True,
# )
# def update_project_name_select_data(n_clicks, data):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         return save_file.data_to_key_options(data)


# # ----- variation name select data update -----
# @callback(
#     Output("delete-variation-name", "data"),
#     Input("delete-project-name", "value"),
#     State("firebase_storage", "data"),
#     prevent_initial_call=True,
# )
# def update_variation_name_select_data(val, data):
#     variations = []
#     if data is not None:
#         for items in data[val]:
#             variations.append({"value": items, "label": items})
#         return variations
#     else:
#         raise PreventUpdate
