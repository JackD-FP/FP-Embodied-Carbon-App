import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from src import building_type_option

# ---- Callbacks ----


@callback(
    Output("epic_generate_sum", "children"),
    Output("ice_generate_sum", "children"),
    Output("epic_benchmark_layout", "children"),
    Output("ice_benchmark_layout", "children"),
    Input("proc_store", "data"),
)
def cards_update(data):
    def ui(db_name):
        return html.Div(
            [
                html.H3(
                    "{:,}".format(np.around(df[db_name].sum(), 2)),
                    className="fs-4",
                ),
                html.P(
                    ["kgCO₂e", html.Span(" Total EC")],
                ),
            ]
        )

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")

        epic = ui("EPiC EC")
        ice = ui("ICE EC")

        gb_benchmark = html.Div(
            [
                dmc.SimpleGrid(
                    [
                        dmc.Col(
                            [
                                html.Strong("NLA of the Building"),
                                dmc.Text(
                                    "NLA is the Net Lettable Area of the building",
                                    size="xs",
                                    color="dimmed",
                                ),
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    debounce=True,
                                    persistence=True,
                                    value=10000.0,
                                    id="gb_nla",
                                ),
                            ],
                        ),
                        dmc.Col(
                            [
                                html.Strong("BCA Building Type:"),
                                dmc.Text(
                                    "Classification of the building under NCC",
                                    size="xs",
                                    color="dimmed",
                                ),
                                dbc.Select(
                                    id="gb_building_type",
                                    options=building_type_option.building_type,
                                    value="5_a_grade",
                                    persistence=True,
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
        )
        epic_benchmark = html.Div(
            children=[
                dmc.SimpleGrid(
                    [
                        html.Div(
                            [
                                html.Strong("Area"),
                                dmc.Text(
                                    "Total area of the building",
                                    size="xs",
                                    color="dimmed",
                                ),
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    debounce=True,
                                    persistence=True,
                                    value=10000.0,
                                    id="epic_area",
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Strong("No Benchmark Tool Available"),
                                dmc.Text(
                                    "No benchmark framnework that uses the EPiC database is available",
                                    size="xs",
                                    color="dimmed",
                                ),
                            ],
                        ),
                    ],
                    cols=2,
                    class_name="mb-5",
                ),
                html.H3(id="epic_benchmark", className="fs-4 text-center"),
                html.P(
                    ["kgCO₂e per m²"],
                    className="text-center mb-0",
                ),
            ]
        )
        ice_benchmark = html.Div(
            [
                dmc.SimpleGrid(
                    [
                        html.Div(
                            [
                                html.Strong("GIA of the Building"),
                                dmc.Text(
                                    "GIA is the Gross Internal Area of the building",
                                    size="xs",
                                    color="dimmed",
                                ),
                                dbc.Input(
                                    type="number",
                                    min=1,
                                    debounce=True,
                                    persistence=True,
                                    value=10000.0,
                                    id="ice_gia",
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Strong("BCA Building Type:"),
                                dmc.Text(
                                    "LETI building type classification",
                                    size="xs",
                                    color="dimmed",
                                ),
                                dbc.Select(
                                    id="ice_building_type",
                                    options=building_type_option.leti_type,
                                    value="co",
                                    persistence=True,
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
                html.P("Area in GIA", className="text-center mb-5"),
                html.Div(id="ice_benchmark_result"),
            ]
        )
        return epic, ice, epic_benchmark, ice_benchmark


@callback(
    Output("epic_benchmark", "children"),
    Input("epic_area", "value"),
    State("proc_store", "data"),
)
def epic_benchmark_update(area, data):
    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        if area is None:
            raise PreventUpdate
        else:
            area = float(area)
            epic_benchmark = df["EPiC EC"].sum() / area
            return "{:,}".format(np.around(epic_benchmark, 2))


# ICE callback
@callback(
    Output("ice_gia", "error"),
    Output("ice_benchmark", "children"),
    Output("ice_benchmark_result", "children"),
    Input("ice_gia", "value"),
    Input("ice_building_type", "value"),
    State("proc_store", "data"),
)
def gb_benchmarks_update(val, val_bld, data):
    if val is None or val == "" or val == 0:
        return (
            "NLA cannot be empty or 0",
            "No Value",
            "No Value",
        )
    else:
        label = building_type_option.leti_option[val_bld]

        def template(x: str):
            template = [
                dcc.Store(id="temp_ice_gia", data=val),
                html.H5(
                    [html.Strong("LETI"), "'s Climate Emegency Design Guide requires"],
                    className="display-6 fs-5 text-center",
                ),
                html.Span(
                    [
                        html.H5(
                            [
                                html.Strong("{}".format(label)),
                                x,
                                html.Strong(
                                    "{} kgCO₂e per m²".format(
                                        building_type_option.leti(val_bld)
                                    )
                                ),
                                # html.Strong("{}".format(label)),
                            ],
                            className="display-6 fs-5 text-center mb-5",
                        )
                    ]
                ),
            ]
            return template

        df = pd.read_json(data, orient="split")
        ice_sum = df["ICE EC"].sum()
        ice_benchmark = ice_sum / val

        if ice_benchmark < building_type_option.leti(
            val_bld
        ):  # if ice_benchmark is less than leti
            message = "Your benchmark is lower than the LETI's Climate Emergency Design Guide requirement"
            alert = [
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
            return (
                False,
                "{:,}".format(np.around(ice_benchmark, 2)),
                template(" to be less than < ") + alert,
            )
        else:  # if ice_benchmark is MORE than leti
            message = "Your benchmark is greater than the LETI benchmark"
            alert = [
                dmc.Alert(
                    message,
                    title="Alert!",
                    color="yellow",
                    icon=[
                        DashIconify(
                            icon="mdi:alert-circle-outline", color="red", width=30
                        )
                    ],
                ),
            ]
            return (
                False,
                "{:,}".format(np.around(ice_benchmark, 2)),
                template(" to be LESS than < ") + alert,
            )


cards = dmc.SimpleGrid(
    children=[
        dmc.Paper(
            children=[
                html.Div(
                    [
                        html.H5(
                            children="EPiC DB",
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
                                            id="epic_generate_sum",
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
                ),
                html.Div(id="epic_benchmark_layout"),
            ],
            radius="md",
            withBorder=True,
            class_name="p-5",
            style={"border": f"1px solid {dmc.theme.DEFAULT_COLORS['gray'][4]}"},
        ),
        dmc.Paper(
            children=[
                html.Div(
                    [
                        html.H5(
                            children="ICE DB",
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
                                            id="ice_generate_sum",
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
                ),
                html.Div(id="ice_benchmark_layout"),
            ],
            radius="sm",
            withBorder=True,
            class_name="p-5",
            style={"border": f"1px solid {dmc.theme.DEFAULT_COLORS['gray'][4]}"},
        ),
    ],
    cols=2,
    class_name="mt-5",
    breakpoints=[
        {"maxWidth": 1300, "cols": 1},
    ],
)
