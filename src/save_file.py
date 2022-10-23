import datetime
import json

import dash_mantine_components as dmc
import firebase_admin
import pandas as pd
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from firebase_admin import credentials, firestore, storage
from src import firebase_init

# from src import load_file  # need this for load_btn callback

new_project = dmc.Tab(
    id="new-project",
    label="New Project",
    children=[
        dmc.Text(
            "Create a new PROJECT and save your design variation to it.",
            id="null",
            size="sm",
            color="gray",
        ),
        dmc.Group(
            children=[
                dmc.Space(h="xs"),
                dmc.TextInput(
                    label="Project Name",
                    id="project_name_input",
                    style={"width": 200},
                    description="Name of the architecture project that you are working on.",
                    placeholder="Center Georges Poppadom",
                    required=True,
                ),
                dmc.Text(size="xs", id="project_name_error", color="red"),
            ],
            direction="column",
            align="center",
        ),
    ],
)
existing_project = dmc.Tab(
    id="existing-project",
    label="Existing Project",
    children=[
        dmc.Text(
            "Save your design variation to an existing PROJECT.",
            size="sm",
            color="gray",
        ),
        dmc.Group(
            children=[
                dmc.Space(h="xs"),
                dmc.Select(
                    label="Select framework",
                    placeholder="Select one",
                    id="project_select",
                    searchable=True,
                    transition="slide-down",
                    transitionDuration=0.5,
                    maxDropdownHeight=200,
                ),
            ],
            direction="column",
            align="center",
        ),
    ],
)

save_modal = html.Div(
    children=[
        dmc.Modal(
            [
                dmc.Tabs(
                    color="blue",
                    orientation="horizontal",
                    children=[new_project, existing_project],
                ),
                dmc.Space(h="xs"),
                dmc.TextInput(
                    label="Variation Name",
                    id="variation_name_input",
                    style={"width": 200, "margin": "auto"},
                    description="The name of this design variation.",
                    placeholder="All Timber",
                    required=True,
                ),
                dmc.Text(
                    size="xs",
                    id="variation_name_error",
                    color="red",
                    style={"textAlign": "center"},
                ),
                dmc.Space(h="xs"),
                dmc.Button(
                    "Save",
                    id="save_to_firebase_btn",
                    disabled=True,
                ),
                html.Div(id="save_new_project"),
                html.Div(id="save_new_variation"),
            ],
            id="save-modal",
        ),
    ]
)

# ----- disables save btn and load btn if no analysis -----
@callback(
    Output("save-button", "disabled"),
    Output("load-button", "disabled"),
    Input("proc_store", "data"),
    prevent_initial_call=True,
)
def disable_save_btn(data):
    if data is None:
        return True, True
    else:
        return False, False


# ----- get projects -----
# get data from firestore when
# save-button or load-button is clicked
@callback(
    Output("firebase_storage", "data"),
    Input("save-button", "n_clicks"),
    Input("load-button", "n_clicks"),
    prevent_initial_call=True,
)
def load_firestore_data(save, load):
    projects = {}
    docs = firebase_init.db.collection("projects").stream()
    for doc in docs:
        projects[doc.to_dict().get("project_name")] = doc.to_dict().get(
            "variation_name"
        )
    return projects


# ----- ui handling for project_select -----
def data_to_key_options(data):
    """Converts data to options for Select component.

    Args:
        data (_dict_): Dictionary of firestore data.

    Returns:
        _list_: returns list of dictionaries
    """
    options = []
    for key, value in data.items():
        options.append({"value": key, "label": key})
    return options


@callback(
    Output("project_select", "data"),
    Input("save-button", "n_clicks"),
    State("firebase_storage", "data"),
    prevent_initial_call=True,
)
def update_project_select(n_clicks, data):
    if data is None:
        raise PreventUpdate
    else:
        options = data_to_key_options(data)
        return options


# ----- Save Logic -----
# pd.groupby is used to reduce the size of the data that is saved to firestore
def send_data(data, collection, document):
    """Send data to firebase storage.

    Args:
        data ( dataframe ): pandas dataframe of data
        collection ( String ): Collection name
        document ( String ): Document name
    """
    df = pd.read_json(data, orient="split")
    df_ = df.groupby(
        [
            "Floor Level",
            "Element",
            "Green Book Material",
            "EPiC Material",
            "ICE Material",
        ],
        as_index=False,
    ).sum()
    to_send = df_.to_json(orient="split")
    # storing main json database in firebase storage
    firebase_init.bucket.blob(
        "{}+{}.json".format(collection, document)
    ).upload_from_string(
        data=to_send,
        content_type="application/json",
    )


def new_project_(project_name, variation_name):
    """Create new project in firestore.

    Args:
        project_name ( String ): Name of the project
        variation_name ( String ): Name of the variation
    """
    firebase_init.db.collection("projects").document(project_name).set(
        {
            "project_name": project_name,
            "variation_name": [variation_name],
            "datetime": [str(datetime.datetime.now(tz=datetime.timezone.utc).date())],
        }
    )


def append_to_project(project_name, variation_name):
    """Append variation name to project.

    Args:
        project_name ( String ): Name of project
        variation_name ( String ): Name of variation
    """
    doc_ref = firebase_init.db.collection("projects").document(project_name)
    doc_ref.update({"variation_name": firestore.ArrayUnion([variation_name])})
    datetime_string = str(datetime.datetime.now(tz=datetime.timezone.utc).date())
    doc_ref.update({"datetime": firestore.ArrayUnion([datetime_string])})


# saving project with NEW PROJECT NAME
@callback(
    Output("save_new_project", "children"),
    Input("save_to_firebase_btn", "n_clicks"),
    Input("project_name_input", "value"),
    Input("variation_name_input", "value"),
    State("analysis_store", "data"),
    prevent_initial_call=True,
)
def save_to_firebase(n_clicks, project_name, variation_name, data):
    # send_data(data)
    if "save_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:
        new_project_(project_name, variation_name)
        send_data(data, project_name, variation_name)
        return (
            dmc.Notification(
                title="Save Successful",
                id="save_notification",
                action="show",
                message="Your design variation has been saved to the database.",
                icon=[DashIconify(icon="ic:round-celebration")],
                color="green",
            ),
        )

    else:
        raise PreventUpdate


# appending new variation to existing project
@callback(
    Output("save_new_variation", "children"),
    Input("save_to_firebase_btn", "n_clicks"),
    Input("project_select", "value"),
    Input("variation_name_input", "value"),
    State("analysis_store", "data"),
    prevent_initial_call=True,
)
def append_to_firebase(n_clicks, project_name, variation_name, data):
    if "save_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:
        append_to_project(project_name, variation_name)
        send_data(data, project_name, variation_name)
        return (
            dmc.Notification(
                title="Save Successful",
                id="save_notification",
                action="show",
                message="Your design variation called {} has been saved to the {}.".format(
                    variation_name, project_name
                ),
                icon=[DashIconify(icon="ic:round-celebration")],
                color="green",
            ),
        )

    else:
        raise PreventUpdate


# ----- error handling for Variation Name text input -----
@callback(
    Output("project_name_input", "error"),
    Output("variation_name_input", "error"),
    Input("project_name_input", "value"),
    Input("variation_name_input", "value"),
    State("firebase_storage", "data"),
    prevent_initial_call=True,
)
def project_name_error(project_name, variation_name, fb_storage):
    if variation_name == "" or project_name == "":
        return "Project Name should NOT be empty", "variation name should NOT be empty"
    elif disable_btn(fb_storage, project_name, variation_name):
        return (
            "Project name already exists for this project",
            True,
        )
    else:
        return False, False


# ----- error handling -----

# logic for disabling save button
input_dict = {
    None: True,
    "": True,
    True: True,
    0: True,
}


def check_input_(input):
    return input_dict.get(input, False)


# ----- error handling for Project Name text input -----
def disable_btn(dictionary, key, value):
    """Disable the save button if the project name is not unique.

    Args:
        dictionary (_dict_): Dictionary of firestore data.
        key (_str_): project name
        value (_str_): variation name stored under project name

    Returns:
        _bool_: returns if project contains the variation name
    """
    if key in dictionary:
        # if value in dictionary[key]: # if variation name is already in project
        return True
    else:
        return False


def project_check(data, project_name):
    if project_name in data:
        return False
    else:
        return True


def variation_check(data, project_name, variation_name):
    if variation_name in data[project_name]:
        return False
    else:
        return True


def select_check(data, project_select, variation_name):
    for items in data[project_select]:
        if variation_name == items:
            return True


# # disables btn callback
# TODO: add check for existing project.
@callback(
    Output("save_to_firebase_btn", "disabled"),
    Input("variation_name_input", "error"),
    Input("project_name_input", "error"),
    Input("project_select", "value"),
    Input("variation_name_input", "value"),
    State("firebase_storage", "data"),
)
def update_disable_btn(
    variation_name_error, project_name_error, project_select, variation_value, data
):
    # print(str(data))
    if variation_name_error is None or project_name_error is None:
        return True
    elif variation_name_error or project_name_error:
        return True
    elif select_check(data, project_select, variation_value):
        return True
    else:
        return False


# logic to disable the text input if proc_store is empty
@callback(
    Output("project_name_input", "disabled"),
    Output("variation_name_input", "disabled"),
    Output("project_name_error", "children"),
    Output("variation_name_error", "children"),
    Input("proc_store", "data"),
)
def update_project_name_input(proc_data):
    error = "Please upload a project first."
    if proc_data is None:
        return True, True, error, error
    else:
        return False, False, "", ""
