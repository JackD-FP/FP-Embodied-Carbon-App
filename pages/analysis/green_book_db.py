# import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# import dash_mantine_components as dmc
# from dash import Input, Output, callback, dcc, html, State
# from dash.exceptions import PreventUpdate
# import plotly.express as px
# from src import funcs, greenbook_options
# import re
# from config import config

# # ---- object instantiate ----
# # also generates the material & embodied carbon tables\

# beams = funcs.table(
#     id="beams",
#     concrete_options=greenbook_options.concrete,
#     rebar_options=greenbook_options.rebar,
#     steel_options=greenbook_options.steel,
#     timber_options=greenbook_options.timber,
#     db_name="gb",
#     concrete=643,
#     rebar=1.733,
#     steel=2.9,
#     timber=718,
# )
# columns = funcs.table(
#     id="Columns",
#     concrete_options=greenbook_options.concrete,
#     rebar_options=greenbook_options.rebar,
#     steel_options=greenbook_options.steel,
#     timber_options=greenbook_options.timber,
#     db_name="gb",
#     concrete=643,
#     rebar=1.733,
#     steel=2.9,
#     timber=718,
# )
# slabs = funcs.table(
#     id="Slabs",
#     concrete_options=greenbook_options.concrete,
#     rebar_options=greenbook_options.rebar,
#     steel_options=greenbook_options.steel,
#     timber_options=greenbook_options.timber,
#     db_name="gb",
#     concrete=643,
#     rebar=1.733,
#     steel=2.9,
#     timber=718,
# )
# walls = funcs.table(
#     id="Walls",
#     concrete_options=greenbook_options.concrete,
#     rebar_options=greenbook_options.rebar,
#     steel_options=greenbook_options.steel,
#     timber_options=greenbook_options.timber,
#     db_name="gb",
#     concrete=643,
#     rebar=1.733,
#     steel=2.9,
#     timber=718,
# )
# stairs = funcs.table(
#     id="Stairs",
#     concrete_options=greenbook_options.concrete,
#     rebar_options=greenbook_options.rebar,
#     steel_options=greenbook_options.steel,
#     timber_options=greenbook_options.timber,
#     db_name="gb",
#     concrete=643,
#     rebar=1.733,
#     steel=2.9,
#     timber=718,
# )

# # ----  Callbacks ----

# # god all mighty callback! that does all the work!
# # █████████████████████
# # ████████(⓿_⓿)████████
# # █████████████████████
# @callback(
#     [
#         Output("gb-val-custom-beams-Concrete", "children"),
#         Output("gb-val-custom-beams-Reinforcement-Bar", "children"),
#         Output("gb-val-custom-beams-Structural-Steel", "children"),
#         Output("gb-val-custom-beams-Structural-Timber", "children"),
#         Output("gb-val-custom-Columns-Concrete", "children"),
#         Output("gb-val-custom-Columns-Reinforcement-Bar", "children"),
#         Output("gb-val-custom-Columns-Structural-Steel", "children"),
#         Output("gb-val-custom-Columns-Structural-Timber", "children"),
#         Output("gb-val-custom-Slabs-Concrete", "children"),
#         Output("gb-val-custom-Slabs-Reinforcement-Bar", "children"),
#         Output("gb-val-custom-Slabs-Structural-Steel", "children"),
#         Output("gb-val-custom-Slabs-Structural-Timber", "children"),
#         Output("gb-val-custom-Walls-Concrete", "children"),
#         Output("gb-val-custom-Walls-Reinforcement-Bar", "children"),
#         Output("gb-val-custom-Walls-Structural-Steel", "children"),
#         Output("gb-val-custom-Walls-Structural-Timber", "children"),
#         Output("gb-val-custom-Stairs-Concrete", "children"),
#         Output("gb-val-custom-Stairs-Reinforcement-Bar", "children"),
#         Output("gb-val-custom-Stairs-Structural-Steel", "children"),
#         Output("gb-val-custom-Stairs-Structural-Timber", "children"),
#         Output("gb_analysis_total", "children"),
#         Output("gb_analysis_benchmark", "children"),
#         Output("gb_analysis_pie", "figure"),
#         Output("gb_analysis_bar", "figure"),
#         # Output("gb_analysis_store", "data"),
#     ],
#     [
#         Input("sel-custom-gb-beams-Concrete", "value"),
#         Input("sel-custom-gb-beams-Reinforcement-Bar", "value"),
#         Input("sel-custom-gb-beams-Structural-Steel", "value"),
#         Input("sel-custom-gb-beams-Structural-Timber", "value"),
#         Input("sel-custom-gb-Columns-Concrete", "value"),
#         Input("sel-custom-gb-Columns-Reinforcement-Bar", "value"),
#         Input("sel-custom-gb-Columns-Structural-Steel", "value"),
#         Input("sel-custom-gb-Columns-Structural-Timber", "value"),
#         Input("sel-custom-gb-Slabs-Concrete", "value"),
#         Input("sel-custom-gb-Slabs-Reinforcement-Bar", "value"),
#         Input("sel-custom-gb-Slabs-Structural-Steel", "value"),
#         Input("sel-custom-gb-Slabs-Structural-Timber", "value"),
#         Input("sel-custom-gb-Walls-Concrete", "value"),
#         Input("sel-custom-gb-Walls-Reinforcement-Bar", "value"),
#         Input("sel-custom-gb-Walls-Structural-Steel", "value"),
#         Input("sel-custom-gb-Walls-Structural-Timber", "value"),
#         Input("sel-custom-gb-Stairs-Concrete", "value"),
#         Input("sel-custom-gb-Stairs-Reinforcement-Bar", "value"),
#         Input("sel-custom-gb-Stairs-Structural-Steel", "value"),
#         Input("sel-custom-gb-Stairs-Structural-Timber", "value"),
#         State("analysis_store", "data"),
#         State("nla_store", "data"),
#     ],
# )
# def cards_update(
#     beam_conc,
#     beam_rebar,
#     beam_steel,
#     beam_timber,
#     col_conc,
#     col_rebar,
#     col_steel,
#     col_timber,
#     slab_conc,
#     slab_rebar,
#     slab_steel,
#     slab_timber,
#     wall_conc,
#     wall_rebar,
#     wall_steel,
#     wall_timber,
#     stair_conc,
#     stair_rebar,
#     stair_steel,
#     stair_timber,
#     data,
#     nla,
# ):
#     if data is None:
#         raise PreventUpdate
#     else:
#         df = pd.read_json(data, orient="split")
#         # df.drop(columns=["Green Book EC", "EPiC EC", "ICE EC"], inplace=True)

#         # create list of submaterials and embodied carbon values to be appended to df
#         # creates a whole new df for easier calculation
#         sub_materials = []
#         ec_values = []
#         colors = []
#         for i, row in df.iterrows():
#             if row["Element"] == "Beam":
#                 material_dict = {
#                     "Concrete": funcs.concrete(
#                         beam_conc, row["Volume"], source=beams.concrete_options
#                     ),
#                     "Reinforcement Bar": funcs.rebar(
#                         beam_rebar, row["Mass"], source=beams.rebar_options
#                     ),
#                     "Structural Steel": funcs.steel(
#                         beam_steel, row["Mass"], source=beams.steel_options
#                     ),
#                     "Structural Timber": funcs.timber(
#                         beam_timber,
#                         row["Mass"],
#                         row["Volume"],
#                         source=beams.timber_options,
#                     ),
#                 }
#                 sub_materials.append(
#                     material_dict.get(row["Materials"])[0]
#                 )  # sub_materials
#                 ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
#                 colors.append(material_dict.get(row["Materials"])[2])

#             elif row["Element"] == "Column":
#                 material_dict = {
#                     "Concrete": funcs.concrete(
#                         col_conc, row["Volume"], source=columns.concrete_options
#                     ),
#                     "Reinforcement Bar": funcs.rebar(
#                         col_rebar, row["Mass"], source=columns.rebar_options
#                     ),
#                     "Structural Steel": funcs.steel(
#                         col_steel, row["Mass"], source=columns.steel_options
#                     ),
#                     "Structural Timber": funcs.timber(
#                         col_timber,
#                         row["Mass"],
#                         row["Volume"],
#                         source=columns.timber_options,
#                     ),
#                 }
#                 sub_materials.append(
#                     material_dict.get(row["Materials"])[0]
#                 )  # sub_materials
#                 ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
#                 colors.append(material_dict.get(row["Materials"])[2])

#             elif row["Element"] == "Slab":
#                 material_dict = {
#                     "Concrete": funcs.concrete(
#                         slab_conc, row["Volume"], source=slabs.concrete_options
#                     ),
#                     "Reinforcement Bar": funcs.rebar(
#                         slab_rebar, row["Mass"], source=slabs.rebar_options
#                     ),
#                     "Structural Steel": funcs.steel(
#                         slab_steel, row["Mass"], source=slabs.steel_options
#                     ),
#                     "Structural Timber": funcs.timber(
#                         slab_timber,
#                         row["Mass"],
#                         row["Volume"],
#                         source=slabs.timber_options,
#                     ),
#                 }
#                 sub_materials.append(
#                     material_dict.get(row["Materials"])[0]
#                 )  # sub_materials
#                 ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
#                 colors.append(material_dict.get(row["Materials"])[2])

#             elif row["Element"] == "Wall":
#                 material_dict = {
#                     "Concrete": funcs.concrete(
#                         wall_conc, row["Volume"], source=walls.concrete_options
#                     ),
#                     "Reinforcement Bar": funcs.rebar(
#                         wall_rebar, row["Mass"], source=walls.rebar_options
#                     ),
#                     "Structural Steel": funcs.steel(
#                         wall_steel, row["Mass"], source=walls.steel_options
#                     ),
#                     "Structural Timber": funcs.timber(
#                         wall_timber,
#                         row["Mass"],
#                         row["Volume"],
#                         source=walls.timber_options,
#                     ),
#                 }
#                 sub_materials.append(material_dict.get(row["Materials"])[0])
#                 ec_values.append(material_dict.get(row["Materials"])[1])  # ec_values
#                 colors.append(material_dict.get(row["Materials"])[2])

#             elif row["Element"] == "Stairs":
#                 material_dict = {
#                     "Concrete": funcs.concrete(
#                         stair_conc, row["Volume"], source=stairs.concrete_options
#                     ),
#                     "Reinforcement Bar": funcs.rebar(
#                         stair_rebar, row["Mass"], source=stairs.rebar_options
#                     ),
#                     "Structural Steel": funcs.steel(
#                         stair_steel, row["Mass"], source=stairs.steel_options
#                     ),
#                     "Structural Timber": funcs.timber(
#                         stair_timber,
#                         row["Mass"],
#                         row["Volume"],
#                         source=stairs.timber_options,
#                     ),
#                 }
#                 sub_materials.append(material_dict.get(row["Materials"])[0])
#                 ec_values.append(material_dict.get(row["Materials"])[1])
#                 colors.append(material_dict.get(row["Materials"])[2])

#         df.insert(loc=0, column="Sub-Material", value=sub_materials)
#         df.insert(loc=0, column="EC Value", value=ec_values)
#         df.insert(loc=0, column="GB Colors", value=colors)

#         df_grouped = df.groupby(["Sub-Material", "GB Colors"], as_index=False).sum()
#         # df.to_excel("test.xlsx")
#         # print(colors)
#         color_names = df["Sub-Material"].unique().tolist()
#         colour_values = df["GB Colors"].unique().tolist()

#         color_dict = dict(zip(color_names, colour_values))

#         # generate pie and bar figs
#         fig_pie = px.pie(
#             df_grouped,
#             values="EC Value",
#             color="Sub-Material",
#             names="Sub-Material",
#             title="Embodied Carbon",
#             color_discrete_map=color_dict,
#         )
#         fig_bar = px.histogram(
#             df,
#             x="Floor Level",
#             y="EC Value",
#             color="Sub-Material",
#             title="Embodied Carbon",
#             color_discrete_map=color_dict,
#         )

#         # send the new df to storage
#         df_json = df.to_json(orient="split")

#         return (
#             # Beam materials
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Beam") & (df["Materials"] == "Concrete"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Beam")
#                     & (df["Materials"] == "Reinforcement Bar"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Beam") & (df["Materials"] == "Structural Steel"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Beam")
#                     & (df["Materials"] == "Structural Timber"),
#                     "EC Value",
#                 ].sum()
#             ),
#             # column materials
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Column") & (df["Materials"] == "Concrete"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Column")
#                     & (df["Materials"] == "Reinforcement Bar"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Column")
#                     & (df["Materials"] == "Structural Steel"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Column")
#                     & (df["Materials"] == "Structural Timber"),
#                     "EC Value",
#                 ].sum()
#             ),
#             # slab materials
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Slab") & (df["Materials"] == "Concrete"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Slab")
#                     & (df["Materials"] == "Reinforcement Bar"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Slab") & (df["Materials"] == "Structural Steel"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Slab")
#                     & (df["Materials"] == "Structural Timber"),
#                     "EC Value",
#                 ].sum()
#             ),
#             # wall materials
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Wall") & (df["Materials"] == "Concrete"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Wall")
#                     & (df["Materials"] == "Reinforcement Bar"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Wall") & (df["Materials"] == "Structural Steel"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Wall")
#                     & (df["Materials"] == "Structural Timber"),
#                     "EC Value",
#                 ].sum()
#             ),
#             # stairs materials
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Stairs") & (df["Materials"] == "Concrete"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Stairs")
#                     & (df["Materials"] == "Reinforcement Bar"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Stairs")
#                     & (df["Materials"] == "Structural Steel"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(
#                 df.loc[
#                     (df["Element"] == "Stairs")
#                     & (df["Materials"] == "Structural Timber"),
#                     "EC Value",
#                 ].sum()
#             ),
#             "{:,.2f}".format(total := sum(ec_values)),
#             "{:,.2f}".format(total / nla),
#             fig_pie,
#             fig_bar,
#             # df_json,
#         )


# # ---- layout of the website ----
# gb_layout = html.Div(
#     children=[
#         dbc.Row(
#             [
#                 dbc.Col(
#                     children=[
#                         # Beam card
#                         dmc.Paper(
#                             children=[
#                                 html.H3("Beam"),
#                                 dmc.Divider(class_name="mb-3"),
#                                 beams.table_gen(),
#                             ],
#                             class_name="p-5 m-5 ",
#                             shadow="sm",
#                             radius="md",
#                             withBorder=True,
#                         ),
#                         # column card
#                         dmc.Paper(
#                             children=[
#                                 html.H3("Column"),
#                                 dmc.Divider(class_name="mb-3"),
#                                 columns.table_gen(),
#                             ],
#                             class_name="p-5 m-5 ",
#                             shadow="sm",
#                             radius="md",
#                             withBorder=True,
#                         ),
#                         # slab card
#                         dmc.Paper(
#                             children=[
#                                 html.H3("Slab"),
#                                 dmc.Divider(class_name="mb-3"),
#                                 slabs.table_gen(),
#                             ],
#                             class_name="p-5 m-5 ",
#                             shadow="sm",
#                             radius="md",
#                             withBorder=True,
#                         ),
#                         # wall card
#                         dmc.Paper(
#                             children=[
#                                 html.H3("Wall"),
#                                 dmc.Divider(class_name="mb-3"),
#                                 walls.table_gen(),
#                             ],
#                             class_name="p-5 m-5 ",
#                             shadow="sm",
#                             radius="md",
#                             withBorder=True,
#                         ),
#                         # stairs card
#                         dmc.Paper(
#                             children=[
#                                 html.H3("Stair"),
#                                 dmc.Divider(class_name="mb-3"),
#                                 stairs.table_gen(),
#                             ],
#                             class_name="p-5 m-5 ",
#                             shadow="sm",
#                             radius="md",
#                             withBorder=True,
#                         ),
#                     ]
#                 ),
#                 dbc.Col(
#                     children=[
#                         html.Div(
#                             children=[
#                                 dbc.Row(
#                                     children=[
#                                         dbc.Col(
#                                             children=[
#                                                 html.H3(
#                                                     children=["Calculating..."],
#                                                     id="gb_analysis_total",
#                                                     className="text-center",
#                                                 ),
#                                                 html.P(
#                                                     [
#                                                         html.Strong("kgCO₂e"),
#                                                         dmc.Text(
#                                                             "Total EC", color="gray"
#                                                         ),
#                                                     ],
#                                                     className="text-center",
#                                                 ),
#                                             ]
#                                         ),
#                                         dbc.Col(
#                                             children=[
#                                                 html.H3(
#                                                     children=["Calculating..."],
#                                                     id="gb_analysis_benchmark",
#                                                     className="text-center",
#                                                 ),
#                                                 html.P(
#                                                     [
#                                                         html.Strong("kgCO₂e/m²"),
#                                                         dmc.Text(
#                                                             "Benchmark per NLA",
#                                                             color="gray",
#                                                         ),
#                                                     ],
#                                                     className="text-center mb-5",
#                                                 ),
#                                             ]
#                                         ),
#                                     ]
#                                 ),
#                                 dmc.LoadingOverlay(
#                                     dcc.Graph(
#                                         id="gb_analysis_pie",
#                                         className="h-50",
#                                         config=config,
#                                     ),
#                                     loaderProps={
#                                         "color": "blue",
#                                         "variant": "oval",
#                                     },
#                                 ),
#                                 dmc.LoadingOverlay(
#                                     dcc.Graph(
#                                         id="gb_analysis_bar",
#                                         className="h-50",
#                                         config=config,
#                                     ),
#                                     loaderProps={
#                                         "color": "blue",
#                                         "variant": "oval",
#                                     },
#                                 ),
#                             ],
#                             className="py-5 sticky-top",
#                         ),
#                     ]
#                 ),  # column for the results of the edits
#             ]
#         ),
#     ]
# )
