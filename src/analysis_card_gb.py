import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from src import greenbook_options

gb_layout = [
    dbc.Card(
        [
            dcc.Store(id="gb_store"),
            html.H3("Green Book DB"),
            dmc.Divider(class_name="mb-5"),
            dmc.SimpleGrid(
                cols=2,
                children=[
                    dmc.Col(
                        [
                            dmc.SimpleGrid(
                                children=[
                                    dmc.Col(
                                        children=[
                                            html.H4(  # total
                                                id="gb_analysis_total",
                                                # "{:,}".format(total),
                                                className="text-center",
                                            ),
                                            html.P(
                                                [
                                                    "kgCO₂e",
                                                    dmc.Text("Total EC", color="gray"),
                                                ],
                                                className="text-center",
                                            ),
                                        ]
                                    ),
                                    dmc.Col(
                                        children=[
                                            html.H4(  # Benchmarks
                                                id="gb_analysis_benchmark",
                                                # "{:,}".format(benchmark),
                                                className="text-center",
                                            ),
                                            html.P(
                                                [
                                                    "kgCO₂e per m²",
                                                    dmc.Text(
                                                        "Building Benchmark",
                                                        color="gray",
                                                    ),
                                                ],
                                                className="text-center",
                                            ),
                                        ]
                                    ),
                                ],
                                cols=2,
                                class_name="mb-5",
                            ),
                            # span=6,
                            dbc.Tabs(
                                id="gb_tabs",
                                active_tab="Beams",
                                children=[
                                    dbc.Tab(
                                        label="Beams",
                                        tab_id="Beams",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Columns",
                                        tab_id="Columns",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Slabs",
                                        tab_id="Slabs",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Walls",
                                        tab_id="Walls",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Stairs",
                                        tab_id="Stairs",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                ],
                            ),
                            # content for tab divs
                            html.Div(id="gb_tab_content", className="p-5"),
                            # tab_div(self.tab_content),
                        ]
                    ),
                    dmc.Col(html.Div("potato")),
                ],
            ),
        ],
        class_name="my-5 p-4 shadow",
    )
]


class table:
    def __init__(
        self,
        id,
        concrete_options,
        rebar_options,
        steel_options,
        timber_options,
        concrete=0,
        rebar=0,
        steel=0,
        timber=0,
    ):
        self.id = id
        self.concrete_options = concrete_options
        self.rebar_options = rebar_options
        self.steel_options = steel_options
        self.timber_options = timber_options
        self.conc_val = concrete
        self.rebar_val = rebar
        self.steel_val = steel
        self.timber_val = timber


def table_gen(
    id,
    concrete_options,
    rebar_options,
    steel_options,
    timber_options,
    concrete=0,
    rebar=0,
    steel=0,
    timber=0,
):
    table_head = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Materials"),
                    html.Th("Embodied Carbon"),
                ]
            )
        )
    ]
    options = [
        concrete_options,
        rebar_options,
        steel_options,
        timber_options,
    ]
    mat_val = [
        concrete,
        rebar,
        steel,
        timber,
    ]
    labels = [
        {"name": "Concrete", "value": 643},
        {"name": "Reinforcement Bar", "value": 2.340},
        {"name": "Structural Steel", "value": 2.9},
        {"name": "Structural Timber", "value": 718},
    ]
    rows = []

    for i, options in enumerate(options):
        mat_row = html.Tr(
            [
                html.Td(
                    dbc.Row(
                        [
                            dbc.Col(children=dmc.Text(labels[i]["name"])),
                            dbc.Col(
                                children=dbc.Select(
                                    id="sel-{}-{}".format(
                                        id, labels[i]["name"].replace(" ", "-")
                                    ),
                                    options=options,
                                    value=labels[i]["value"],
                                    persistence=True,
                                )
                            ),
                        ]
                    )
                ),
                html.Td(
                    mat_val[i],
                    id="val-{}-{}".format(id, labels[i]["name"].replace(" ", "-")),
                ),
            ]
        )

        rows.append(mat_row)
    return dbc.Table(table_head + [html.Tbody(rows, className="w-75")])


# ---- Class definition ----
beams = table(
    id="beams",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
columns = table(
    id="Columns",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
slabs = table(
    id="Slabs",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
walls = table(
    id="Walls",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
stairs = table(
    id="Stairs",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)


# ---- This updates the total and benchmark ----
@callback(
    Output("gb_analysis_total", "children"),
    Output("gb_analysis_benchmark", "children"),
    Input("gb_store", "modified_timestamp"),
    Input("nla_store", "modified_timestamp"),
    State("gb_store", "data"),
    State("nla_store", "data"),
)
def update_total_benchmark(mts, mts_nla, gb_data, nla):
    if mts is None or mts_nla is None:
        raise PreventUpdate
    else:
        df = pd.read_json(gb_data, orient="split")
        total = df["Green Book EC"].sum()
        benchmark = total / nla
        return "{:,}".format(np.around(total, 2)), "{:,}".format(
            np.around(benchmark, 2)
        )


# ---- This updates/generates the table ----
@callback(
    Output("gb_tab_content", "children"),
    Input("gb_tabs", "active_tab"),
)
def update_layout(tabs):
    # df = pd.read_json(data, orient="split")
    # id,concrete_options, rebar_options, steel_options, timber_options, concrete=0, rebar=0, steel=0, timber=0
    content = {
        "Beams": table_gen(
            beams.id,
            beams.concrete_options,
            beams.rebar_options,
            beams.steel_options,
            beams.timber_options,
            beams.conc_val,
            beams.rebar_val,
            beams.steel_val,
            beams.timber_val,
        ),
        "Columns": table_gen(
            columns.id,
            columns.concrete_options,
            columns.rebar_options,
            columns.steel_options,
            columns.timber_options,
            columns.conc_val,
            columns.rebar_val,
            columns.steel_val,
            columns.timber_val,
        ),
        "Slabs": table_gen(
            slabs.id,
            slabs.concrete_options,
            slabs.rebar_options,
            slabs.steel_options,
            slabs.timber_options,
            slabs.conc_val,
            slabs.rebar_val,
            slabs.steel_val,
            slabs.timber_val,
        ),
        "Walls": table_gen(
            walls.id,
            walls.concrete_options,
            walls.rebar_options,
            walls.steel_options,
            walls.timber_options,
            walls.conc_val,
            walls.rebar_val,
            walls.steel_val,
            walls.timber_val,
        ),
        "Stairs": table_gen(
            stairs.id,
            stairs.concrete_options,
            stairs.rebar_options,
            stairs.steel_options,
            stairs.timber_options,
            stairs.conc_val,
            stairs.rebar_val,
            stairs.steel_val,
            stairs.timber_val,
        ),
    }

    return content.get(tabs, "Error")


@callback(
    Output("gb_store", "data"),
    Input("proc_store", "data"),
)
def update_gb_store(data):
    if data is None:
        raise PreventUpdate
    else:
        # df = pd.read_json(data, orient="split")
        # df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        # beams.conc_val = conc_val * 1
        # df.to_json(orient="split")
        return data


@callback(
    Output("val-beams-Concrete", "data"),
    Input("sel-beams-Concrete", "value"),
)
def beam_val_update(val):
    return val
