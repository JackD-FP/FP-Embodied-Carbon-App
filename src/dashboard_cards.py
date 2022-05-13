import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate

from src import building_type_option, funcs

# ---- Green Book DB side of thing ----
gb_sum = 12313123.0
epic_sum = 112312312.0
ice_sum = 13490409.0


def generate_table(sum, name="Green Book DB"):
    return html.Div(
        [
            # Green Book Column
            html.H5(
                children=name,
                className="my-4 display-6",
                style={"textAlign": "center"},
            ),
            dmc.Divider(
                style={
                    "marginLeft": "2rem",
                    "marginRight": "2rem",
                }
            ),
            html.Div(
                [
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Div(
                                [
                                    html.H3(
                                        "{:,}".format(np.around(sum, 2)),
                                        className="display-6, fs-4",
                                    ),
                                    html.P(
                                        ["kgCO²e", html.Span(" Total EC")],
                                    ),
                                ],
                                style={"textAlign": "center"},
                            ),
                        ],
                    )
                ],
                style={
                    "marginTop": "3rem",
                    "marginBottom": "3rem",
                },
            ),
            dmc.Divider(
                style={
                    "marginLeft": "2rem",
                    "marginRight": "2rem",
                }
            ),
            # GFA calc for green book
        ]
    )


cards = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        generate_table(gb_sum, "Green Book DB"),
                    ],
                    span=3,
                    class_name="bg-light",
                ),
                dmc.Col(generate_table(epic_sum, "Epic DB"), span=3),
                dmc.Col(
                    [generate_table(ice_sum, "ICE DB")],
                    span=3,
                    class_name="bg-light",
                ),
            ],
            gutter="xl",
            class_name="my-5",
            grow=True,
        )
    ]
)
