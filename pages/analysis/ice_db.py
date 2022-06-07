import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from config import config
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from src import funcs, ice_options

# class table:
#     def __init__(
#         self,
#         id,
#         concrete_options,
#         rebar_options,
#         steel_options,
#         timber_options,
#         concrete=0,
#         rebar=0,
#         steel=0,
#         timber=0,
#     ):
#         self.id = id
#         self.concrete_options = concrete_options
#         self.rebar_options = rebar_options
#         self.steel_options = steel_options
#         self.timber_options = timber_options
#         self.conc_val = concrete
#         self.rebar_val = rebar
#         self.steel_val = steel
#         self.timber_val = timber

#     def table_gen(self):
#         table_head = [
#             html.Thead(
#                 html.Tr(
#                     [
#                         html.Th("Materials"),
#                         html.Th("Embodied Carbon"),
#                     ]
#                 )
#             )
#         ]
#         options = [
#             self.concrete_options,
#             self.rebar_options,
#             self.steel_options,
#             self.timber_options,
#         ]
#         mat_val = [
#             self.conc_val,
#             self.rebar_val,
#             self.steel_val,
#             self.timber_val,
#         ]
#         labels = [
#             {"name": "Concrete", "value": 413.4943},
#             {"name": "Reinforcement Bar", "value": 1.99},
#             {"name": "Structural Steel", "value": 1.55},
#             {"name": "Structural Timber", "value": 0.51},
#         ]
#         rows = []

#         for i, options in enumerate(options):
#             mat_row = html.Tr(
#                 [
#                     html.Td(
#                         dbc.Row(
#                             [
#                                 dbc.Col(children=dmc.Text(labels[i]["name"])),
#                                 dbc.Col(
#                                     children=dbc.Select(
#                                         id="sel-ice-{}-{}".format(
#                                             self.id, labels[i]["name"].replace(" ", "-")
#                                         ),
#                                         options=options,
#                                         value=labels[i]["value"],
#                                         persistence=True,
#                                     )
#                                 ),
#                             ]
#                         )
#                     ),
#                     html.Td(
#                         mat_val[i],
#                         id="val-ice-{}-{}".format(
#                             self.id, labels[i]["name"].replace(" ", "-")
#                         ),
#                     ),
#                 ]
#             )

#             rows.append(mat_row)
#         return dbc.Table(table_head + [html.Tbody(rows, className="w-75")])


# ---- object instantiate ----
# also generates the material & embodied carbon tables
beams = funcs.table(
    id="beams",
    concrete_options=ice_options.concrete,
    rebar_options=ice_options.rebar,
    steel_options=ice_options.steel,
    timber_options=ice_options.timber,
    db_name="ice",
    concrete=413.4943,
    rebar=1.99,
    steel=1.55,
    timber=0.51,
)
columns = funcs.table(
    id="Columns",
    concrete_options=ice_options.concrete,
    rebar_options=ice_options.rebar,
    steel_options=ice_options.steel,
    timber_options=ice_options.timber,
    db_name="ice",
    concrete=413.4943,
    rebar=1.99,
    steel=1.55,
    timber=0.51,
)
slabs = funcs.table(
    id="Slabs",
    concrete_options=ice_options.concrete,
    rebar_options=ice_options.rebar,
    steel_options=ice_options.steel,
    timber_options=ice_options.timber,
    db_name="ice",
    concrete=413.4943,
    rebar=1.99,
    steel=1.55,
    timber=0.51,
)
walls = funcs.table(
    id="Walls",
    concrete_options=ice_options.concrete,
    rebar_options=ice_options.rebar,
    steel_options=ice_options.steel,
    timber_options=ice_options.timber,
    db_name="ice",
    concrete=413.4943,
    rebar=1.99,
    steel=1.55,
    timber=0.51,
)
stairs = funcs.table(
    id="Stairs",
    concrete_options=ice_options.concrete,
    rebar_options=ice_options.rebar,
    steel_options=ice_options.steel,
    timber_options=ice_options.timber,
    db_name="ice",
    concrete=413.4943,
    rebar=1.99,
    steel=1.55,
    timber=0.51,
)

# ----  Callbacks ----

# god all mighty callback! that does all the work!
# ████████(⓿_⓿)████████
# █████████████████████
@callback(
    [
        Output("ice-val-custom-beams-Concrete", "children"),
        Output("ice-val-custom-beams-Reinforcement-Bar", "children"),
        Output("ice-val-custom-beams-Structural-Steel", "children"),
        Output("ice-val-custom-beams-Structural-Timber", "children"),
        Output("ice-val-custom-Columns-Concrete", "children"),
        Output("ice-val-custom-Columns-Reinforcement-Bar", "children"),
        Output("ice-val-custom-Columns-Structural-Steel", "children"),
        Output("ice-val-custom-Columns-Structural-Timber", "children"),
        Output("ice-val-custom-Slabs-Concrete", "children"),
        Output("ice-val-custom-Slabs-Reinforcement-Bar", "children"),
        Output("ice-val-custom-Slabs-Structural-Steel", "children"),
        Output("ice-val-custom-Slabs-Structural-Timber", "children"),
        Output("ice-val-custom-Walls-Concrete", "children"),
        Output("ice-val-custom-Walls-Reinforcement-Bar", "children"),
        Output("ice-val-custom-Walls-Structural-Steel", "children"),
        Output("ice-val-custom-Walls-Structural-Timber", "children"),
        Output("ice-val-custom-Stairs-Concrete", "children"),
        Output("ice-val-custom-Stairs-Reinforcement-Bar", "children"),
        Output("ice-val-custom-Stairs-Structural-Steel", "children"),
        Output("ice-val-custom-Stairs-Structural-Timber", "children"),
        Output("ice_analysis_total", "children"),
        Output("ice_analysis_benchmark", "children"),
        Output("ice_analysis_pie", "figure"),
        Output("ice_analysis_bar", "figure"),
        # Output("ice_analysis_store", "data"),
    ],
    [
        Input("sel-custom-ice-beams-Concrete", "value"),
        Input("sel-custom-ice-beams-Reinforcement-Bar", "value"),
        Input("sel-custom-ice-beams-Structural-Steel", "value"),
        Input("sel-custom-ice-beams-Structural-Timber", "value"),
        Input("sel-custom-ice-Columns-Concrete", "value"),
        Input("sel-custom-ice-Columns-Reinforcement-Bar", "value"),
        Input("sel-custom-ice-Columns-Structural-Steel", "value"),
        Input("sel-custom-ice-Columns-Structural-Timber", "value"),
        Input("sel-custom-ice-Slabs-Concrete", "value"),
        Input("sel-custom-ice-Slabs-Reinforcement-Bar", "value"),
        Input("sel-custom-ice-Slabs-Structural-Steel", "value"),
        Input("sel-custom-ice-Slabs-Structural-Timber", "value"),
        Input("sel-custom-ice-Walls-Concrete", "value"),
        Input("sel-custom-ice-Walls-Reinforcement-Bar", "value"),
        Input("sel-custom-ice-Walls-Structural-Steel", "value"),
        Input("sel-custom-ice-Walls-Structural-Timber", "value"),
        Input("sel-custom-ice-Stairs-Concrete", "value"),
        Input("sel-custom-ice-Stairs-Reinforcement-Bar", "value"),
        Input("sel-custom-ice-Stairs-Structural-Steel", "value"),
        Input("sel-custom-ice-Stairs-Structural-Timber", "value"),
        State("analysis_store", "data"),
        State("gia_store", "data"),
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
    gia,
):
    df = pd.read_json(data, orient="split")
    df.drop(columns=["Green Book EC", "EPiC EC", "ICE EC"], inplace=True)

    # create list of submaterials and embodied carbon values to be appended to df
    # creates a whole new df for easier calculation
    sub_materials = []
    ec_values = []
    colors = []
    for i, row in df.iterrows():
        if row["Element"] == "Beam":
            material_dict = {
                "Concrete": funcs.concrete(
                    beam_conc, row["Volume"], source=beams.concrete_options
                ),
                "Reinforcement Bar": funcs.rebar(
                    beam_rebar, row["Mass"], source=beams.rebar_options
                ),
                "Structural Steel": funcs.steel(
                    beam_steel, row["Mass"], source=beams.steel_options
                ),
                "Structural Timber": funcs.timber(
                    beam_timber,
                    row["Mass"],
                    row["Volume"],
                    source=beams.timber_options,
                    ice=True,
                ),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
            colors.append(material_dict.get(row["Materials"])[2])  # colors

        elif row["Element"] == "Column":
            material_dict = {
                "Concrete": funcs.concrete(
                    col_conc, row["Volume"], source=columns.concrete_options
                ),
                "Reinforcement Bar": funcs.rebar(
                    col_rebar, row["Mass"], source=columns.rebar_options
                ),
                "Structural Steel": funcs.steel(
                    col_steel, row["Mass"], source=columns.steel_options
                ),
                "Structural Timber": funcs.timber(
                    col_timber,
                    row["Mass"],
                    row["Volume"],
                    source=columns.timber_options,
                    ice=True,
                ),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
            colors.append(material_dict.get(row["Materials"])[2])  # colors

        elif row["Element"] == "Slab":
            material_dict = {
                "Concrete": funcs.concrete(
                    slab_conc, row["Volume"], source=slabs.concrete_options
                ),
                "Reinforcement Bar": funcs.rebar(
                    slab_rebar, row["Mass"], source=slabs.rebar_options
                ),
                "Structural Steel": funcs.steel(
                    slab_steel, row["Mass"], source=slabs.steel_options
                ),
                "Structural Timber": funcs.timber(
                    slab_timber,
                    row["Mass"],
                    row["Volume"],
                    source=slabs.timber_options,
                    ice=True,
                ),
            }
            sub_materials.append(
                material_dict.get(row["Materials"])[0]
            )  # sub_materials
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
            colors.append(material_dict.get(row["Materials"])[2])  # colors

        elif row["Element"] == "Wall":
            material_dict = {
                "Concrete": funcs.concrete(
                    wall_conc, row["Volume"], source=walls.concrete_options
                ),
                "Reinforcement Bar": funcs.rebar(
                    wall_rebar, row["Mass"], source=walls.rebar_options
                ),
                "Structural Steel": funcs.steel(
                    wall_steel, row["Mass"], source=walls.steel_options
                ),
                "Structural Timber": funcs.timber(
                    wall_timber,
                    row["Mass"],
                    row["Volume"],
                    source=walls.timber_options,
                    ice=True,
                ),
            }
            sub_materials.append(material_dict.get(row["Materials"])[0])
            ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
            colors.append(material_dict.get(row["Materials"])[2])  # colors

        elif row["Element"] == "Stairs":
            material_dict = {
                "Concrete": funcs.concrete(
                    stair_conc, row["Volume"], source=stairs.concrete_options
                ),
                "Reinforcement Bar": funcs.rebar(
                    stair_rebar, row["Mass"], source=stairs.rebar_options
                ),
                "Structural Steel": funcs.steel(
                    stair_steel, row["Mass"], source=stairs.steel_options
                ),
                "Structural Timber": funcs.timber(
                    stair_timber,
                    row["Mass"],
                    row["Volume"],
                    source=stairs.timber_options,
                    ice=True,
                ),
            }
            sub_materials.append(material_dict.get(row["Materials"])[0])
            ec_values.append(material_dict.get(row["Materials"])[1])
            colors.append(material_dict.get(row["Materials"])[2])
    df.insert(loc=0, column="ICE Submaterialss", value=sub_materials)
    df.insert(loc=0, column="ICE EC Values", value=ec_values)
    df.insert(loc=0, column="ICE Colors", value=colors)

    df_grouped = df.groupby(["ICE Submaterialss", "ICE Colors"], as_index=False).sum()
    color_names = df["ICE Submaterialss"].unique().tolist()
    colour_values = df["ICE Colors"].unique().tolist()

    color_dict = dict(zip(color_names, colour_values))

    # color_names = df["ICE Submaterialss"].unique().tolist()
    # colors = [
    #     "#FF595E",
    #     "#36949D",
    #     "#FF924C",
    #     "#1982C4",
    #     "#FFCA3A",
    #     "#4267AC",
    #     "#C5CA30",
    #     "#565AA0",
    #     "#8AC926",
    #     "#6A4C93",
    # ]
    # color_dict = dict(zip(color_names, colors))

    # generate pie and bar figs
    fig_pie = px.pie(
        df_grouped,
        values="ICE EC Values",
        color="ICE Submaterialss",
        names="ICE Submaterialss",
        title="Embodied Carbon",
        color_discrete_map=color_dict,
    )
    fig_bar = px.histogram(
        df,
        x="Floor Level",
        y="ICE EC Values",
        color="ICE Submaterialss",
        title="Embodied Carbon",
        color_discrete_map=color_dict,
    )
    ice_df = df.to_json(orient="split")

    return (
        # Beam materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Concrete"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Reinforcement Bar"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Structural Steel"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Beam") & (df["Materials"] == "Structural Timber"),
                "ICE EC Values",
            ].sum()
        ),
        # column materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Concrete"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Reinforcement Bar"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Structural Steel"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Column") & (df["Materials"] == "Structural Timber"),
                "ICE EC Values",
            ].sum()
        ),
        # slab materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Concrete"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Reinforcement Bar"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Structural Steel"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Slab") & (df["Materials"] == "Structural Timber"),
                "ICE EC Values",
            ].sum()
        ),
        # wall materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Concrete"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Reinforcement Bar"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Structural Steel"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Wall") & (df["Materials"] == "Structural Timber"),
                "ICE EC Values",
            ].sum()
        ),
        # stairs materials
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Concrete"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Reinforcement Bar"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Structural Steel"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(
            df.loc[
                (df["Element"] == "Stairs") & (df["Materials"] == "Structural Timber"),
                "ICE EC Values",
            ].sum()
        ),
        "{:,.2f}".format(total := sum(ec_values)),
        "{:,.2f}".format(total / gia),
        fig_pie,
        fig_bar,
    )


# ---- layout of the website ----
ice_layout = html.Div(
    children=[
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
                                dmc.Text(
                                    "*Reinforcement Bar options have the same value at 1.99 kgCO₂e per kg",
                                    size="xs",
                                    color="gray",
                                ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # column card
                        dbc.Card(
                            children=[
                                html.H3("Column"),
                                dmc.Divider(class_name="mb-3"),
                                columns.table_gen(),
                                dmc.Text(
                                    "*Reinforcement Bar options have the same value at 1.99 kgCO₂e per kg",
                                    size="xs",
                                    color="gray",
                                ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # slab card
                        dbc.Card(
                            children=[
                                html.H3("Slab"),
                                dmc.Divider(class_name="mb-3"),
                                slabs.table_gen(),
                                dmc.Text(
                                    "*Reinforcement Bar options have the same value at 1.99 kgCO₂e per kg",
                                    size="xs",
                                    color="gray",
                                ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # wall card
                        dbc.Card(
                            children=[
                                html.H3("Wall"),
                                dmc.Divider(class_name="mb-3"),
                                walls.table_gen(),
                                dmc.Text(
                                    "*Reinforcement Bar options have the same value at 1.99 kgCO₂e per kg",
                                    size="xs",
                                    color="gray",
                                ),
                            ],
                            class_name="p-5 m-5 shadow rounded",
                        ),
                        # stairs card
                        dbc.Card(
                            children=[
                                html.H3("Stair"),
                                dmc.Divider(class_name="mb-3"),
                                stairs.table_gen(),
                                dmc.Text(
                                    "*Reinforcement Bar options have the same value at 1.99 kgCO₂e per kg",
                                    size="xs",
                                    color="gray",
                                ),
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
                                                    children=["Calculating..."],
                                                    id="ice_analysis_total",
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
                                                    children=["Calculating..."],
                                                    id="ice_analysis_benchmark",
                                                    className="text-center",
                                                ),
                                                html.P(
                                                    [
                                                        html.Strong("kgCO₂e/m²"),
                                                        dmc.Text(
                                                            "Benchmark per GIA",
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
                                        id="ice_analysis_pie",
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
                                        id="ice_analysis_bar",
                                        className="h-50",
                                        config=config,
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                            ],
                            className="pt-5 sticky-top",
                        ),
                    ]
                ),  # column for the results of the edits
            ]
        ),
        # analysis_comparison.comparison,
    ]
)
