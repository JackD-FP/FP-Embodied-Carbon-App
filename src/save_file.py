import datetime
import json

import dash_mantine_components as dmc
import firebase_admin
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from firebase_admin import credentials, firestore

new_project = dmc.Tab(
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
                    id="framework-select",
                    value="ng",
                    data=[
                        {"value": "react", "label": "React"},
                        {"value": "ng", "label": "Angular"},
                        {"value": "svelte", "label": "Svelte"},
                        {"value": "vue", "label": "Vue"},
                    ],
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
                html.Div(id="save_to_firebase_output"),
            ],
            id="save-modal",
        ),
    ]
)


cred = credentials.Certificate("creds/creds.json")
fp_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# ----- get projects -----
@callback(
    # Output("firebase_store_projectNames", "data"),
    # Output("firebase_store_variationNames", "data"),
    Output("firebase_storage", "data"),
    Input("save-button", "n_clicks"),
    prevent_initial_call=True,
)
def load_firestore_data(n_clicks):
    project_names = []
    variation_names = []
    projects = {}
    docs = db.collection("projects").stream()
    for doc in docs:
        projects[doc.to_dict().get("project_name")] = doc.to_dict().get(
            "variation_name"
        )
        # project_names.append(doc.to_dict().get("project_name"))
        # for i in doc.to_dict().get("variation_name"):
        #     variation_names.append(i)
    # print(project_names)
    # print(variation_names)
    # return json.dumps(projects)
    return projects


# ----- Send Logic -----
@callback(
    Output("save_to_firebase_output", "children"),
    Input("save_to_firebase_btn", "n_clicks"),
    Input("project_name_input", "value"),
    Input("variation_name_input", "value"),
    prevent_initial_call=True,
)
def save_to_firebase(n_clicks, project_name, variation_name):

    if "save_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:
        doc_ref = db.collection("projects").document(project_name)
        doc_ref.set(
            {
                "project_name": project_name,
                "variation_name": [variation_name],
                "date": [datetime.datetime.now(tz=datetime.timezone.utc)],
            }
        )
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
        if value in dictionary[key]:
            return True
    else:
        return False


# ----- error handling for Variation Name text input -----
@callback(
    Output("project_name_input", "error"),
    Output("variation_name_input", "error"),
    Input("project_name_input", "value"),
    Input("variation_name_input", "value"),
    State("firebase_storage", "data"),
)
def project_name_error(project_name, variation_name, fb_storage):
    if variation_name == "" or project_name == "":
        return "Project Name should NOT be empty", "variation name should NOT be empty"
    elif disable_btn(fb_storage, project_name, variation_name):
        return False, "Variation name already exists for this project"
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


@callback(
    Output("save_to_firebase_btn", "disabled"),
    Input("variation_name_input", "value"),
    Input("project_name_input", "value"),
    State("save_to_firebase_btn", "n_clicks"),
    State("firebase_storage", "data"),
    prevent_initial_call=True,
)
def check_input(variation_value, project_value, n_clicks, data):
    if check_input_(variation_value) or check_input_(project_value):
        return True
    elif n_clicks is not None and n_clicks % 2 == 0:
        return True
    elif disable_btn(data, project_value, variation_value):
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


# logic to disable the project name exist in database
# @callback(
#     Output("save_to_firebase_btn", "disabled"),
#     Output("project_name_input", "error"),
#     Input("project_name_input", "value"),
# )

# @callback(
#     Input("save_to_firebase_btn", "n_clicks"),
#     Input("project_name_input", "value"),
#     Input("variation_name_input", "value"),
# )
#         # doc_ref = db.collection("projects").document(project_name)
#         # doc_ref.set(
#         #     {
#         #         "variations": {
#         #             variation_name: {
#         #                 "beam": 39,
#         #                 "column": 41,
#         #                 "slab": 13,
#         #             }
#         #         }
#         #     }
#         # )
