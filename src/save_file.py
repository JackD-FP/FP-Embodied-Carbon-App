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


def variation_input(id: str, text_error: str):
    """Create variation input.

    Args:
        id (str): id of the input
        text_error (str): error message id

    Returns:
        dash component: returns dash component
    """
    input = html.Div(
        children=[
            dmc.Space(h="xs"),
            dmc.TextInput(
                label="Variation Name",
                id=id,
                style={"width": 200, "margin": "auto"},
                description="The name of this design variation.",
                placeholder="All Timber",
                required=True,
            ),
            dmc.Text(
                size="xs",
                id=text_error,
                color="red",
                style={"textAlign": "center"},
            ),
        ]
    )
    return input


new_project = dmc.Tab(
    id="new-project",
    label="New Project",
    children=[
        html.Div(id="save_new_project"),
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
        variation_input(
            "new_project_variation", "new_project_variation_error"
        ),  # TODO:
        dmc.Space(h="xs"),
        dmc.Button(
            "Save",
            id="save_to_firebase_btn",
            disabled=True,
        ),
    ],
)


existing_project = dmc.Tab(
    id="existing-project",
    label="Existing Project",
    children=[
        html.Div(id="save_new_variation"),
        dmc.Text(
            "Save your design variation to an existing project. NOTE: You not overwrite an existing variation but you can give the new variation a different but related name. Such as 'timber var 2' for an existing 'timber' variation.",
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
        variation_input(
            "append_project_variation", "append_project_variation_error"
        ),  # TODO:
        dmc.Space(h="xs"),
        dmc.Button(
            "Save",
            id="append_to_firebase_btn",
            disabled=True,
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


def new_project_(
    project_name: str, variation_name: str, greenbook: float, epic: float, ice: float
):
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
            "greenbook": [greenbook],
            "epic": [epic],
            "ice": [ice],
        }
    )


def append_to_project(
    project_name: str, variation_name: str, greenbook: float, epic: float, ice: float
):
    """Append variation name to project.

    Args:
        project_name ( String ): Name of project
        variation_name ( String ): Name of variation
    """
    doc_ref = firebase_init.db.collection("projects").document(project_name)
    doc_ref.update({"variation_name": firestore.ArrayUnion([variation_name])})
    datetime_string = str(datetime.datetime.now(tz=datetime.timezone.utc).date())
    doc_ref.update({"datetime": firestore.ArrayUnion([datetime_string])})
    doc_ref.update({"greenbook": firestore.ArrayUnion([greenbook])})
    doc_ref.update({"epic": firestore.ArrayUnion([epic])})
    doc_ref.update({"ice": firestore.ArrayUnion([ice])})


def ec_totals(data):
    """Calculate the total of each material type.

    Args:
        data ( dataframe ): pandas dataframe of data

    Returns:
        _dict_: returns dictionary of totals
    """
    df = pd.read_json(data, orient="split")
    gb = df["Green Book EC"].sum()
    epic = df["EPiC EC"].sum()
    ice = df["ICE EC"].sum()
    return {"gb": gb, "epic": epic, "ice": ice}


# saving project with NEW PROJECT NAME
@callback(
    Output("save_new_project", "children"),
    Input("save_to_firebase_btn", "n_clicks"),
    Input("project_name_input", "value"),
    Input("new_project_variation", "value"),
    State("analysis_store", "data"),
    prevent_initial_call=True,
)
def save_to_firebase(n_clicks, project_name, variation_name, data):
    # send_data(data)
    if "save_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:

        ec = ec_totals(data)

        new_project_(project_name, variation_name, ec["gb"], ec["epic"], ec["ice"])
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
    Input("append_to_firebase_btn", "n_clicks"),
    Input("project_select", "value"),
    Input("append_project_variation", "value"),
    State("analysis_store", "data"),
    prevent_initial_call=True,
)
def append_to_firebase(n_clicks, project_name, variation_name, data):
    if "append_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:

        ec = ec_totals(data)

        append_to_project(project_name, variation_name, ec["gb"], ec["epic"], ec["ice"])
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


# ----- error handling for new project name -----
def does_project_exists(project_name):
    """Check if project exists in firestore.

    Args:
        project_name ( String ): Name of project

    Returns:
        _bool_: returns True if project exists
    """
    doc_ref = firebase_init.db.collection("projects").document(project_name)
    doc = doc_ref.get()
    return doc.exists


@callback(
    Output("project_name_input", "error"),
    Output("new_project_variation", "error"),
    Input("project_name_input", "value"),
    prevent_initial_update=True,
)
def update_project_name_error(project_name):
    if project_name is None or project_name == "":
        return "Don't leave me blank!", True
    elif does_project_exists(project_name):
        return "Project already exists!", True
    else:
        return False, False


@callback(
    Output("save_to_firebase_btn", "disabled"),
    Input("project_name_input", "error"),
    Input("new_project_variation", "value"),
    prevent_initial_update=True,
)
def disable_save_button(project_name, variation_name):
    if project_name:
        return True
    elif variation_name is None or variation_name == "":
        return True
    else:
        return False


def does_variation_exist(data, key, value):
    for items in data[key]:
        if items == value:
            return "varaition name already exist!"


# ----- error handling for appending to project -----
@callback(
    Output("append_project_variation", "error"),
    Input("append_project_variation", "value"),
    State("project_select", "value"),
    State("firebase_storage", "data"),
    prevent_initial_update=True,
)
def update_append_variation_error(variation_name, project_name, data):
    if project_name is not None:
        return does_variation_exist(data, project_name, variation_name)
    else:
        return True


def check_variation_error(error: bool, name: str) -> bool:
    """Check if variation name is valid.

    Args:
        error (bool): error state of variation name
        name (str): variation name

    Returns:
        bool: returns True if variation name is valid
    """
    if error:
        return True
    elif name is None or name == "":
        return True
    else:
        return False


@callback(
    Output("append_to_firebase_btn", "disabled"),
    Input("append_project_variation", "error"),
    State("append_project_variation", "value"),
    State("project_select", "value"),
    prevent_initial_update=True,
)
def update_disable_append_button(variation_error, variation_name, project_name):
    if project_name is not None:
        return check_variation_error(variation_error, variation_name)
    else:
        return True
