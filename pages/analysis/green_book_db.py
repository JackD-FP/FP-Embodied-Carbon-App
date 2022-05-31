import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from pages import analysis
from src import greenbook_options, analysis_comparison
import re
from config import config
from dash_iconify import DashIconify


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
# also generates the material & embodied carbon tables
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


def concrete(value, volume):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for concrete

    Args:
        value ( float ): value of the dropdown
        volume ( float ): volume of the row

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    sub_material = [
        x["label"] for x in beams.concrete_options if x["value"] == int(value)
    ][0]
    ec_value = float(value) * volume
    return sub_material, ec_value


def rebar(value, mass):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for rebar

    Args:
        value ( float ): value of the dropdown
        mass ( float ): mass of the row

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    sub_material = [
        x["label"] for x in beams.rebar_options if x["value"] == float(value)
    ][0]
    ec_value = float(value) * mass
    return sub_material, ec_value


def steel(value, mass):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for steel

    Args:
        value ( float ): value of the dropdown
        mass ( float ): mass of the row

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    sub_material = [
        x["label"] for x in beams.steel_options if x["value"] == float(value)
    ][0]
    ec_value = float(value) * mass
    return sub_material, ec_value


def timber(value, volume):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for timber

    Args:
        value ( float ): value of the dropdown
        volume ( float ): volume of the row

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    sub_material = [
        x["label"] for x in beams.timber_options if x["value"] == int(value)
    ][0]
    ec_value = float(value) * volume
    return sub_material, ec_value


# god all mighty callback! that does all the work!
# ████████(⓿_⓿)████████
# █████████████████████
@callback(
    [
        Output("val-beams-Concrete", "children"),
        Output("val-beams-Reinforcement-Bar", "children"),
        Output("val-beams-Structural-Steel", "children"),
        Output("val-beams-Structural-Timber", "children"),
        Output("val-Columns-Concrete", "children"),
        Output("val-Columns-Reinforcement-Bar", "children"),
        Output("val-Columns-Structural-Steel", "children"),
        Output("val-Columns-Structural-Timber", "children"),
        Output("val-Slabs-Concrete", "children"),
        Output("val-Slabs-Reinforcement-Bar", "children"),
        Output("val-Slabs-Structural-Steel", "children"),
        Output("val-Slabs-Structural-Timber", "children"),
        Output("val-Walls-Concrete", "children"),
        Output("val-Walls-Reinforcement-Bar", "children"),
        Output("val-Walls-Structural-Steel", "children"),
        Output("val-Walls-Structural-Timber", "children"),
        Output("val-Stairs-Concrete", "children"),
        Output("val-Stairs-Reinforcement-Bar", "children"),
        Output("val-Stairs-Structural-Steel", "children"),
        Output("val-Stairs-Structural-Timber", "children"),
        Output("gb_analysis_total", "children"),
        Output("gb_analysis_benchmark", "children"),
        Output("gb_analysis_pie", "figure"),
        Output("gb_analysis_bar", "figure"),
        Output("gb_analysis_store", "data"),
    ],
    [
        Input("sel-beams-Concrete", "value"),
        Input("sel-beams-Reinforcement-Bar", "value"),
        Input("sel-beams-Structural-Steel", "value"),
        Input("sel-beams-Structural-Timber", "value"),
        Input("sel-Columns-Concrete", "value"),
        Input("sel-Columns-Reinforcement-Bar", "value"),
        Input("sel-Columns-Structural-Steel", "value"),
        Input("sel-Columns-Structural-Timber", "value"),
        Input("sel-Slabs-Concrete", "value"),
        Input("sel-Slabs-Reinforcement-Bar", "value"),
        Input("sel-Slabs-Structural-Steel", "value"),
        Input("sel-Slabs-Structural-Timber", "value"),
        Input("sel-Walls-Concrete", "value"),
        Input("sel-Walls-Reinforcement-Bar", "value"),
        Input("sel-Walls-Structural-Steel", "value"),
        Input("sel-Walls-Structural-Timber", "value"),
        Input("sel-Stairs-Concrete", "value"),
        Input("sel-Stairs-Reinforcement-Bar", "value"),
        Input("sel-Stairs-Structural-Steel", "value"),
        Input("sel-Stairs-Structural-Timber", "value"),
        State("proc_store", "data"),
        State("nla_store", "data"),
    ],
)
def cards_update(
    beam_conc,
    beam_rebar,
    beam_steel,
    beam_timber,
    col_conc,
    col_rebar,
    col_steel,
    col_timber,
    slab_conc,
    slab_rebar,
    slab_steel,
    slab_timber,
    wall_conc,
    wall_rebar,
    wall_steel,
    wall_timber,
    stair_conc,
    stair_rebar,
    stair_steel,
    stair_timber,
    data,
    nla,
):
    df = pd.read_json(data, orient="split")
    df.drop(columns=["Green Book EC", "EPiC EC", "ICE EC"], inplace=True)

    # create list of submaterials and embodied carbon values to be appended to df
    # creates a whole new df for easier calculation
    sub_materials = []
    ec_values = []
    for i, row in df.iterrows():
        if row["Element"] == "Beam":
            material_dict = {
                "Concrete": concrete(beam_conc, row["Volume"]),
                "Reinforcement Bar": rebar(beam_rebar, row["Mass"]),
                "Structural Steel": steel(beam_steel, row["Mass"]),
                "Structural Timber": timber(beam_timber, row["Volume"]),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values

        elif row["Element"] == "Column":
            material_dict = {
                "Concrete": concrete(col_conc, row["Volume"]),
                "Reinforcement Bar": rebar(col_rebar, row["Mass"]),
                "Structural Steel": steel(col_steel, row["Mass"]),
                "Structural Timber": timber(col_timber, row["Volume"]),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values

        elif row["Element"] == "Slab":
            material_dict = {
                "Concrete": concrete(slab_conc, row["Volume"]),
                "Reinforcement Bar": rebar(slab_rebar, row["Mass"]),
                "Structural Steel": steel(slab_steel, row["Mass"]),
                "Structural Timber": timber(slab_timber, row["Volume"]),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values

        elif row["Element"] == "Wall":
            material_dict = {
                "Concrete": concrete(wall_conc, row["Volume"]),
                "Reinforcement Bar": rebar(wall_rebar, row["Mass"]),
                "Structural Steel": steel(wall_steel, row["Mass"]),
                "Structural Timber": timber(wall_timber, row["Volume"]),
            }
            sub_materials.append(material_dict.get(row["Materials"])[0])
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values

        elif row["Element"] == "Stairs":
            material_dict = {
                "Concrete": concrete(stair_conc, row["Volume"]),
                "Reinforcement Bar": rebar(stair_rebar, row["Mass"]),
                "Structural Steel": steel(stair_steel, row["Mass"]),
                "Structural Timber": timber(stair_timber, row["Volume"]),
            }
            sub_materials.append(material_dict.get(row["Materials"])[0])
            ec_values.append(material_dict.get(row["Materials"])[1])
    df.insert(loc=0, column="Sub-Material", value=sub_materials)
    df.insert(loc=0, column="EC Value", value=ec_values)

    df_grouped = df.groupby(["Sub-Material"], as_index=False).sum()

    color_names = df["Sub-Material"].unique().tolist()
    colors = [
        "#FF595E",
        "#36949D",
        "#FF924C",
        "#1982C4",
        "#FFCA3A",
        "#4267AC",
        "#C5CA30",
        "#565AA0",
        "#8AC926",
        "#6A4C93",
    ]
    color_dict = dict(zip(color_names, colors))

    # generate pie and bar figs
    fig_pie = px.pie(
        df_grouped,
        values="EC Value",
        color="Sub-Material",
        names="Sub-Material",
        title="Embodied Carbon",
        color_discrete_map=color_dict,
    )
    fig_bar = px.histogram(
        df,
        x="Floor Level",
        y="EC Value",
        color="Sub-Material",
        title="Embodied Carbon",
        color_discrete_map=color_dict,
    )

    # send the new df to storage
    df_json = df.to_json(orient="split")

    return (
        # Beam materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Concrete"), "EC Value"
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Reinforcement Bar"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Structural Steel"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Structural Timber"),
                "EC Value",
            ].sum()
        ),
        # column materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Concrete"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Reinforcement Bar"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Structural Steel"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Structural Timber"),
                "EC Value",
            ].sum()
        ),
        # slab materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Concrete"), "EC Value"
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Reinforcement Bar"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Structural Steel"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Structural Timber"),
                "EC Value",
            ].sum()
        ),
        # wall materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Concrete"), "EC Value"
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Reinforcement Bar"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Structural Steel"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Structural Timber"),
                "EC Value",
            ].sum()
        ),
        # stairs materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Concrete"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Reinforcement Bar"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Structural Steel"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Structural Timber"),
                "EC Value",
            ].sum()
        ),
        "{:,.2f}".format(total := sum(ec_values)),
        "{:,.2f}".format(total / nla),
        fig_pie,
        fig_bar,
        df_json,
    )


# Callback provision for reset.

# @callback(
#     [
#         Output("sel-beams-Concrete", "value"),
#         Output("sel-beams-Reinforcement-Bar", "value"),
#         Output("sel-beams-Structural-Steel", "value"),
#         Output("sel-beams-Structural-Timber", "value"),
#     ],
#     [
#         Input("beam_reset", "n_clicks"),
#     ],
# )
# def reset_update(
#     beam_reset,
# ):
#     return 643, 2.340, 2.9, 718


# @callback(
#     [
#         Output("sel-Columns-Concrete", "value"),
#         Output("sel-Columns-Reinforcement-Bar", "value"),
#         Output("sel-Columns-Structural-Steel", "value"),
#         Output("sel-Columns-Structural-Timber", "value"),
#     ],
#     [
#         Input("col_reset", "n_clicks"),
#     ],
# )
# def reset_update(
#     col_reset,
# ):
#     return 643, 2.340, 2.9, 718


# @callback(
#     [
#         Output("sel-Slabs-Concrete", "value"),
#         Output("sel-Slabs-Reinforcement-Bar", "value"),
#         Output("sel-Slabs-Structural-Steel", "value"),
#         Output("sel-Slabs-Structural-Timber", "value"),
#     ],
#     [
#         Input("slab_reset", "n_clicks"),
#     ],
# )
# def reset_update(
#     slab_reset,
# ):
#     return 643, 2.340, 2.9, 718


# @callback(
#     [
#         Output("sel-Walls-Concrete", "value"),
#         Output("sel-Walls-Reinforcement-Bar", "value"),
#         Output("sel-Walls-Structural-Steel", "value"),
#         Output("sel-Walls-Structural-Timber", "value"),
#     ],
#     [
#         Input("wall_reset", "n_clicks"),
#     ],
# )
# def reset_update(
#     wall_reset,
# ):
#     return 643, 2.340, 2.9, 718


# @callback(
#     [
#         Output("sel-Stairs-Concrete", "value"),
#         Output("sel-Stairs-Reinforcement-Bar", "value"),
#         Output("sel-Stairs-Structural-Steel", "value"),
#         Output("sel-Stairs-Structural-Timber", "value"),
#     ],
#     [
#         Input("stair_reset", "n_clicks"),
#     ],
# )
# def reset_update(stair_reset):
#     return 643, 2.340, 2.9, 718


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
                                # html.Div(
                                #     dmc.Button(
                                #         id="beam_reset",
                                #         children="reset",
                                #         variant="outline",
                                #         compact=True,
                                #         leftIcon=[DashIconify(icon="bx:reset")],
                                #     ),
                                # ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # column card
                        dbc.Card(
                            children=[
                                html.H3("Column"),
                                dmc.Divider(class_name="mb-3"),
                                columns.table_gen(),
                                # html.Div(
                                #     dmc.Button(
                                #         id="col_reset",
                                #         children="reset",
                                #         variant="outline",
                                #         compact=True,
                                #         leftIcon=[DashIconify(icon="bx:reset")],
                                #     ),
                                # ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # slab card
                        dbc.Card(
                            children=[
                                html.H3("Slab"),
                                dmc.Divider(class_name="mb-3"),
                                slabs.table_gen(),
                                # html.Div(
                                #     dmc.Button(
                                #         id="slab_reset",
                                #         children="reset",
                                #         variant="outline",
                                #         compact=True,
                                #         leftIcon=[DashIconify(icon="bx:reset")],
                                #     ),
                                # ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # wall card
                        dbc.Card(
                            children=[
                                html.H3("Wall"),
                                dmc.Divider(class_name="mb-3"),
                                walls.table_gen(),
                                # html.Div(
                                #     dmc.Button(
                                #         id="wall_reset",
                                #         children="reset",
                                #         variant="outline",
                                #         compact=True,
                                #         leftIcon=[DashIconify(icon="bx:reset")],
                                #     ),
                                # ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # stairs card
                        dbc.Card(
                            children=[
                                html.H3("Stair"),
                                dmc.Divider(class_name="mb-3"),
                                stairs.table_gen(),
                                # html.Div(
                                #     dmc.Button(
                                #         id="stair_reset",
                                #         children="reset",
                                #         variant="outline",
                                #         compact=True,
                                #         leftIcon=[DashIconify(icon="bx:reset")],
                                #     ),
                                # ),
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
                                                    id="gb_analysis_total",
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
                                                    id="gb_analysis_benchmark",
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
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="gb_analysis_pie",
                                        className="h-50",
                                        config=config,
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="gb_analysis_bar",
                                        className="h-50",
                                        config=config,
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                            ],
                            className="py-5 sticky-top",
                        ),
                    ]
                ),  # column for the results of the edits
            ]
        ),
        analysis_comparison.comparison,
    ]
)
