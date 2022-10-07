import datetime

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

# ----- Send Logic -----
cred = credentials.Certificate("creds/creds.json")
fp_app = firebase_admin.initialize_app(cred)
db = firestore.client()


@callback(
    Output("save_to_firebase_output", "children"),
    Input("save_to_firebase_btn", "n_clicks"),
    Input("project_name_input", "value"),
    Input("variation_name_input", "value"),
    prevent_initial_call=True,
)
def save_to_firebase(n_clicks, project_name, variation_name):
    doc_list = []
    docs = db.collection(str("projects")).stream()
    for doc in docs:
        doc_list.append(doc.to_dict())
    print(doc_list)
    if "save_to_firebase_btn" == ctx.triggered[0]["prop_id"].split(".")[0]:
        doc_ref = db.collection("projects").document(project_name)
        doc_ref.set(
            {
                "project_name": project_name,
                "variation_name": variation_name,
                "date": [datetime.datetime.now()],
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


# ----- error handling for Project Name text input -----
@callback(Output("project_name_input", "error"), Input("project_name_input", "value"))
def project_name_error(project_name):
    if project_name == "":
        return "Project name cannot be empty"
    else:
        return False


# ----- error handling for Variation Name text input -----
@callback(
    Output("variation_name_input", "error"), Input("variation_name_input", "value")
)
def project_name_error(variation_name):
    if variation_name == "":
        return "Variation name cannot be empty"
    else:
        return False


# ----- error handling for Save button -----
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
    prevent_initial_call=True,
)
def check_input(variation_value, project_value, n_clicks):

    if check_input_(variation_value) or check_input_(project_value):
        return True
    elif n_clicks is not None and n_clicks % 2 == 0:
        return True
    else:
        return False
