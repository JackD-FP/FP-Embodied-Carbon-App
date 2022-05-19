import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from src import building_type_option, funcs


def generate_card(name="Green Book DB", id="gb_generate_sum"):
    return html.Div(
        [
            # Green Book Column
            html.H5(
                children=name,
                className="mb-4 display-6",
                style={"textAlign": "center"},
            ),
            dmc.Divider(),
            html.Div(
                [
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Div(
                                style={"textAlign": "center"},
                                id=id,
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
                class_name="mb-4",
            ),
        ]
    )


def sum_layer(x):
    return [
        html.H3(
            "{:,}".format(np.around(x, 2)),
            className="fs-4",
        ),
        html.P(
            ["kgCO₂e", html.Span(" Total EC")],
        ),
    ]


def gb_benchmark_update():
    children = [
        dmc.SimpleGrid(
            [
                dmc.Col(
                    [
                        dmc.NumberInput(
                            label="NLA of the building",
                            description="NLA is the Net Lettable Area of the building",
                            value=10000.0,
                            id="gb_nla",
                        )
                    ],
                ),
                dmc.Col(
                    [
                        dmc.Select(
                            label="BCA Building Type:",
                            description="Classification of the building under NCC",
                            placeholder="Select one",
                            id="gb_building_type",
                            value="5_a_grade",
                            data=building_type_option.building_type,
                        ),
                    ],
                ),
            ],
            cols=2,
            class_name="mb-5",
        ),
        html.H3(id="gb_benchmark", className="fs-4 text-center"),
        html.P(
            ["kgCO₂e per m²"],
            className="text-center mb-0",
        ),
        html.P(" Area in NLA", className="text-center bg-light mb-5"),
        html.Div(id="gb_benchmark_result"),
    ]
    return children


def ice_benchmark_update():
    children = [
        dmc.SimpleGrid(
            [
                dmc.Col(
                    [
                        dmc.NumberInput(
                            label="GIA of the building",
                            description="GIA is the Gross Internal Area of the building",
                            value=10000.0,
                            id="ice_gia",
                        )
                    ],
                ),
                dmc.Col(
                    [
                        dmc.Select(
                            label="LETI Building Type:",
                            description="LETI building type classification",
                            placeholder="Select one",
                            id="ice_building_type",
                            value="co",
                            data=building_type_option.leti_type,
                        ),
                    ],
                ),
            ],
            cols=2,
            class_name="mb-5",
        ),
        html.H3(id="ice_benchmark", className="fs-4 text-center"),
        html.P(
            ["kgCO₂e per m²"],
            className="text-center mb-0",
        ),
        html.P("Area in GIA", className="text-center bg-light mb-5"),
        html.Div(id="ice_benchmark_result"),
    ]
    return children


# ---- Callbacks ----
@callback(
    Output("gb_generate_sum", "children"),
    Output("epic_generate_sum", "children"),
    Output("ice_generate_sum", "children"),
    Output("gb_benchmark_layout", "children"),
    Output("ice_benchmark_layout", "children"),
    Input("proc_store", "data"),
)
def cards_update(data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")

        gb = sum_layer(df["Green Book EC"].sum())
        epic = sum_layer(df["EPiC EC"].sum())
        ice = sum_layer(df["ICE EC"].sum())

        gb_benchmark = gb_benchmark_update()
        ice_benchmark = ice_benchmark_update()

        return gb, epic, ice, gb_benchmark, ice_benchmark


# Green Book callback
@callback(
    Output("gb_nla", "error"),
    Output("gb_benchmark", "children"),
    Output("gb_benchmark_result", "children"),
    Input("gb_nla", "value"),
    Input("gb_building_type", "value"),
    State("gb_building_type", "data"),
    State("proc_store", "data"),
)
def gb_benchmarks_update(gb_nla, gb_value, gb_label, data):
    if gb_nla is None or gb_nla == "" or gb_nla == 0:
        return "NLA cannot be empty or 0", "No Value", "No Value"
    else:
        label = [x["label"] for x in gb_label if x["value"] == gb_value]
        gb_template = [
            html.H3(
                [   
                    "TFC's ",
                    html.Strong("Green Book DB"),
                    " benchmark for ",
                    html.Strong("{}".format(label[0])),
                    ", is",
                ],
                className="display-6 fs-5 mb-5 text-center",
            ),
        ]
        df = pd.read_json(data, orient="split")
        gb_sum = df["Green Book EC"].sum()
        gb_benchmark = gb_sum / gb_nla

        children = gb_template + [
            building_type_option.gb_benchmark_calc(gb_value, gb_benchmark),
            html.P(
                building_type_option.gb_benchmark_optimum(gb_value, gb_benchmark),
                className="display-6 fs-5 text-center my-5",
            ),
        ]
        return (
            False,
            "{:,}".format(np.around(gb_benchmark, 2)),
            children,
        )


# ICE callback
@callback(
    Output("ice_gia", "error"),
    Output("ice_benchmark", "children"),
    Output("ice_benchmark_result", "children"),
    Input("ice_gia", "value"),
    Input("ice_building_type", "value"),
    State("ice_building_type", "data"),
    State("proc_store", "data"),
)
def gb_benchmarks_update(val, val_bld, label_bld, data):
    if val is None or val == "" or val == 0:
        return (
            "NLA cannot be empty or 0",
            "No Value",
            "No Value",
        )
    else:
        label = [x["label"] for x in label_bld if x["value"] == val_bld]
        template = [
            html.H5(
                [html.Strong("LETI"), "'s Climate Emegency Design Guide requires"],
                className="display-6 fs-5 text-center",
            ),
            html.Span(
                [
                    html.H5(
                        [
                            html.Strong("{}".format(label[0])),
                            " to be less than < ",
                            html.Strong(
                                "{}".format(building_type_option.leti(val_bld))
                            ),
                        ],
                        className="display-6 fs-5 text-center mb-5",
                    )
                ]
            ),
        ]

        df = pd.read_json(data, orient="split")
        ice_sum = df["ICE EC"].sum()
        ice_benchmark = ice_sum / val

        if ice_benchmark < building_type_option.leti(
            val_bld
        ):  # if ice_benchmark is less than leti
            message = "Your benchmark is lower than the LETI's Climate Emergency Design Guide requirement"
            child = [
                dmc.Alert(
                    message,
                    title="Success!",
                    color="green",
                    icon=[
                        DashIconify(
                            icon="mdi:check-circle-outline", color="green", width=30
                        )
                    ],
                )
            ]
            return (False, "{:,}".format(np.around(ice_benchmark, 2)), template + child)
        else:  # if ice_benchmark is MORE than leti
            message = "Your benchmark is greater than the LETI benchmark"
            child = [
                dmc.Alert(
                    message,
                    title="Alert!",
                    color="yellow",
                    icon=[
                        DashIconify(
                            icon="mdi:alert-circle-outline", color="red", width=30
                        )
                    ],
                )
            ]
            return (False, "{:,}".format(np.around(ice_benchmark, 2)), template + child)


# ---- Generate The Cards for Dashboard ----
cards = html.Div(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        generate_card("Green Book DB"),
                        html.Div(id="gb_benchmark_layout"),
                    ],
                    span=3,
                    class_name="bg-light p-5",
                ),
                dmc.Col(
                    [
                        generate_card("Epic DB", id="epic_generate_sum"),
                        html.H3(
                            "No Benchmark Data", className="display-6 fs-5 text-center"
                        ),
                    ],
                    span=3,
                    class_name="p-5",
                ),
                dmc.Col(
                    [
                        generate_card("ICE DB", id="ice_generate_sum"),
                        html.Div(id="ice_benchmark_layout"),
                    ],
                    span=3,
                    class_name="bg-light p-5",
                ),
            ],
            gutter="xl",
            class_name="my-5",
            grow=True,
        )
    ],
)
