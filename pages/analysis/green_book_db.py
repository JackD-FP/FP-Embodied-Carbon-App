import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
from src import greenbook_options


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

    def table_gen(self):
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
            self.concrete_options,
            self.rebar_options,
            self.steel_options,
            self.timber_options,
        ]
        mat_val = [
            self.conc_val,
            self.rebar_val,
            self.steel_val,
            self.timber_val,
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
                                            self.id, labels[i]["name"].replace(" ", "-")
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
                        id="val-{}-{}".format(
                            self.id, labels[i]["name"].replace(" ", "-")
                        ),
                    ),
                ]
            )

            rows.append(mat_row)
        return dbc.Table(table_head + [html.Tbody(rows, className="w-75")])


# ---- object instantiate ----
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

# ----  Callbacks ----

# god all mighty callback! that does all the work!
# ████████(⓿_⓿)████████
# █████████████████████
def append_ec(df, options, value):
    for i, row in df.iterrows():
        mat_subclass = []
        ec_calc = []
        if row["Layer"] == "Beam" and row["Materials"] == "Concrete":
            mat_subclass.append(
                [x["label"] for x in options if x["value"] == int(value)][0]
            )
            ec_calc.append(row["Volume"] * float(value))
        # TODO: and then do this for the rest of the variation.
        # TODO: please use dictionary instead of long ifs.

    pass


@callback(
    [
        Output("val-beams-Concrete", "children"),
        Output("val-beams-Reinforcement-Bar", "children"),
        Output("val-beams-Structural-Steel", "children"),
        Output("val-beams-Structural-Timber", "children"),
    ],
    [
        Input("sel-beams-Concrete", "value"),
        Input("sel-beams-Reinforcement-Bar", "value"),
        Input("sel-beams-Structural-Steel", "value"),
        Input("sel-beams-Structural-Timber", "value"),
    ],
    [State("proc_store", "data"), State("sel-beams-Concrete", "options")],
)
def cards_update(beam_conc, beam_rebar, beam_steel, beam_timber, data, beam_conc_opts):
    df = pd.read_json(data, orient="split")
    df.drop(columns=["Green Book EC", "EPiC EC", "ICE EC"], inplace=True)
    # the_label = [
    #     x["label"] for x in greenbook_options.concrete if x["value"] == int(beam_conc)
    # ][0]

    return (
        beam_conc,
        beam_rebar,
        beam_steel,
        beam_timber,
    )


# ---- layout of the website ----
gb_layout = html.Div(
    children=[
        html.H1("Green Book DB - Analysis", className="display-2 mb-5 "),
        html.Hr(className="mb-5"),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        # Beam card
                        dbc.Card(
                            children=[
                                html.H3("Beam"),
                                dmc.Divider(class_name="mb-3"),
                                beams.table_gen(),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # column card
                        dbc.Card(
                            children=[
                                html.H3("Column"),
                                dmc.Divider(class_name="mb-3"),
                                columns.table_gen(),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # slab card
                        dbc.Card(
                            children=[
                                html.H3("Slab"),
                                dmc.Divider(class_name="mb-3"),
                                slabs.table_gen(),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # wall card
                        dbc.Card(
                            children=[
                                html.H3("Wall"),
                                dmc.Divider(class_name="mb-3"),
                                walls.table_gen(),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # stairs card
                        dbc.Card(
                            children=[
                                html.H3("Stair"),
                                dmc.Divider(class_name="mb-3"),
                                stairs.table_gen(),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                    ]
                ),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            children=[
                                                html.H3(
                                                    children=[23234],
                                                    id="gb_total",
                                                    className="text-center",
                                                ),
                                                html.P(
                                                    [
                                                        html.Strong("kgCO₂e"),
                                                        dmc.Text(
                                                            "Total EC", color="gray"
                                                        ),
                                                    ],
                                                    className="text-center",
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            children=[
                                                html.H3(
                                                    children=[5678],
                                                    id="gb_total",
                                                    className="text-center",
                                                ),
                                                html.P(
                                                    [
                                                        html.Strong("kgCO₂e/m²"),
                                                        dmc.Text(
                                                            "Benchmark per NLA",
                                                            color="gray",
                                                        ),
                                                    ],
                                                    className="text-center mb-5",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Graph(id="gb_pie", className="h-50"),
                                dcc.Graph(id="gb_bar", className="h-50"),
                            ],
                            className="pt-5 sticky-top",
                        ),
                    ]
                ),  # column for the results of the edits
            ]
        ),
    ]
)
