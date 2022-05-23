# # @TODO:
# # * I think it's better if we used pattern matching for the 3 diffrent card table menu thingy
# # keeps the code smaller and efficient(?).
# # * I also think we can refactor the cards into a functions... not sure if callbacks like it
# # or if it would make things more complicated. cuz you gotta consider different units of different
# # databases... at the moment everything is good. (till it's not)


# import re

# import dash_bootstrap_components as dbc
# import dash_mantine_components as dmc
# import numpy as np
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from config import config, graph_colors
# from dash import Input, Output, State, callback, dcc, html
# from dash.exceptions import PreventUpdate

# from src import (
#     analysis_lib,
#     analysis_more_info,
#     epic_options,
#     funcs,
#     greenbook_options,
#     ice_options,
# )

# # from pages.dashboard import em_calc, gfa_calc


# gb_df = pd.read_csv("src/Greenbook _reduced.csv")
# epic_df = pd.read_csv("src/epic _reduced.csv")
# ice_df = pd.read_csv("src/ice _reduced.csv")

# # ------------------------------Green Book Card--------------------------------------
# table_header = [
#     html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))
# ]
# row1 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         html.P("Concrete Selection:"),
#                         width=3,
#                     ),
#                     dbc.Col(
#                         dbc.Select(
#                             options=greenbook_options.concrete,
#                             id="row_concrete",
#                             value=643,
#                         ),
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(
#             html.Div(
#                 id="row_concrete_value",
#             )
#         ),
#     ]
# )
# row2 = html.Tr(
#     [
#         html.Td(
#             [
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             html.P("Reinforcement Bar:"),
#                             width=3,
#                         ),
#                         dbc.Col(
#                             dbc.Select(
#                                 options=greenbook_options.rebar,
#                                 id="row_rebar",
#                                 value=2.900,
#                             )
#                         ),
#                     ]
#                 ),
#             ]
#         ),
#         html.Td(id="row_rebar_value"),
#     ]
# )
# row3 = html.Tr(
#     [
#         html.Td(
#             [
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             [
#                                 html.P("Structural Steel :"),
#                             ],
#                             width=3,
#                         ),
#                         dbc.Col(
#                             [
#                                 dbc.Select(
#                                     options=greenbook_options.steel,
#                                     id="row_steel",
#                                     value=2.61,
#                                 )
#                             ]
#                         ),
#                     ]
#                 ),
#             ],
#             # dbc.Select(options=greenbook_options.steel, id="row_steel", value=2.61)
#         ),
#         html.Td(id="row_steel_value"),
#     ]
# )
# row4 = html.Tr(
#     [
#         html.Td(
#             [
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             [
#                                 html.P("Structural Timber :"),
#                             ],
#                             width=3,
#                         ),
#                         dbc.Col(
#                             [
#                                 dbc.Select(
#                                     options=greenbook_options.timber,
#                                     id="row_timber",
#                                     value=718,
#                                 )
#                             ]
#                         ),
#                     ]
#                 ),
#             ],
#             # dbc.Select(options=greenbook_options.timber, id="row_timber", value=718)
#         ),
#         html.Td(id="row_timber_value"),
#     ]
# )

# table_body = [html.Tbody([row1, row2, row3, row4])]
# # row = analysis_class.analysis_rows(mat_id="row_timber_value")
# # table_body = [html.Tbody(row.row_generate())]

# greenbook_card = dbc.Card(
#     [
#         html.H3("Green Book Database", className="mb-3 display-5"),
#         html.Hr(),
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     html.Div(
#                                         id="gb_analysis_total", className="text-center"
#                                     )
#                                 ),
#                                 dbc.Col(
#                                     html.Div(
#                                         id="gb_analysis_gfa", className="text-center"
#                                     )
#                                 ),
#                             ],
#                             className="mb-3",
#                         ),
#                         dbc.Table(
#                             table_header + table_body,
#                             striped=True,
#                             bordered=True,
#                             hover=True,
#                         ),
#                     ],
#                     style={"width": "75%"},
#                 ),
#                 dcc.Graph(id="gb_pie", config=config),
#             ],
#             className="hstack",
#         ),
#         dmc.Accordion(
#             [
#                 dmc.AccordionItem(
#                     children=analysis_more_info.gb_more_info,
#                     label="More Information and Analysis",
#                 )
#             ],
#             id="gb_accordion",
#             state={"0": False},
#         ),
#     ],
#     class_name="my-5 p-4 shadow",
# )


# @callback(
#     Output("row_concrete_value", "children"),
#     Output("row_rebar_value", "children"),
#     Output("row_steel_value", "children"),
#     Output("row_timber_value", "children"),
#     Output("gb_analysis_total", "children"),
#     Output("gb_analysis_gfa", "children"),
#     Output("gb_pie", "figure"),
#     Input("row_concrete", "value"),
#     Input("row_rebar", "value"),
#     Input("row_steel", "value"),
#     Input("row_timber", "value"),
#     State("main_store", "data"),
#     State("gfa_store", "data"),
# )
# def gb_row_update(concrete, rebar, steel, timber, data, gfa):
#     return analysis_cards_layout(
#         concrete, rebar, steel, timber, data, gfa, is_ice=False
#     )


# # ------------------------------EPiC Card--------------------------------------
# table_header = [
#     html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))
# ]
# row1 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Concrete Selection:"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=epic_options.concrete,
#                             id="epic_row_concrete",
#                             value=600,
#                         )
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(
#             html.Div(
#                 id="epic_row_concrete_value",
#             )
#         ),
#     ]
# )
# row2 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Reinforcement Bar:"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=epic_options.rebar,
#                             id="epic_row_rebar",
#                             value=2.9,
#                         )
#                     ),
#                 ]
#             )
#         ),
#         html.Td(id="epic_row_rebar_value"),
#     ]
# )
# row3 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Structural Steel :"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=epic_options.steel,
#                             id="epic_row_steel",
#                             value=2.9,
#                         )
#                     ),
#                 ]
#             )
#         ),
#         html.Td(id="epic_row_steel_value"),
#     ]
# )
# row4 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Structural Timber :"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=epic_options.timber,
#                             id="epic_row_timber",
#                             value=1718,
#                         )
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(id="epic_row_timber_value"),
#     ]
# )


# table_body = [html.Tbody([row1, row2, row3, row4])]

# epic_card = dbc.Card(
#     [
#         html.H3("EPiC Database", className="mb-3 display-5"),
#         html.Hr(),
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     html.Div(
#                                         id="epic_analysis_total",
#                                         className="text-center",
#                                     )
#                                 ),
#                                 dbc.Col(
#                                     html.Div(
#                                         id="epic_analysis_gfa", className="text-center"
#                                     )
#                                 ),
#                             ],
#                             className="mb-3",
#                         ),
#                         dbc.Table(
#                             table_header + table_body,
#                             striped=True,
#                             bordered=True,
#                             hover=True,
#                         ),
#                     ],
#                     style={"width": "75%"},
#                 ),
#                 dcc.Graph(id="epic_pie", config=config),
#             ],
#             className="hstack",
#         ),
#         dmc.Accordion(
#             [
#                 dmc.AccordionItem(
#                     children=analysis_more_info.epic_more_info,
#                     label="More Information and Analysis",
#                 )
#             ],
#             id="gb_accordion",
#             state={"0": False},
#         ),
#     ],
#     class_name="my-5 p-4 shadow",
# )


# @callback(
#     Output("epic_row_concrete_value", "children"),
#     Output("epic_row_rebar_value", "children"),
#     Output("epic_row_steel_value", "children"),
#     Output("epic_row_timber_value", "children"),
#     Output("epic_analysis_total", "children"),
#     Output("epic_analysis_gfa", "children"),
#     Output("epic_pie", "figure"),
#     Input("epic_row_concrete", "value"),
#     Input("epic_row_rebar", "value"),
#     Input("epic_row_steel", "value"),
#     Input("epic_row_timber", "value"),
#     State("main_store", "data"),
#     State("gfa_store", "data"),
# )
# def epic_row_update(concrete, rebar, steel, timber, data, gfa):
#     return analysis_cards_layout(
#         concrete, rebar, steel, timber, data, gfa, is_ice=False
#     )


# # ------------------------------ice database Card--------------------------------------

# table_header = [
#     html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))
# ]
# row1 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Concrete Selection:"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=ice_options.concrete,
#                             id="ice_row_concrete",
#                             value=413.4943,
#                         )
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(
#             html.Div(
#                 id="ice_row_concrete_value",
#             )
#         ),
#     ]
# )
# row2 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Reinforcement Bar:"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=ice_options.rebar,
#                             id="ice_row_rebar",
#                             value=1.99,
#                         )
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(
#             html.Div(
#                 id="ice_row_rebar_value",
#             )
#         ),
#     ]
# )
# row3 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Structural Steel :"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=ice_options.steel,
#                             id="ice_row_steel",
#                             value=1.55,
#                         )
#                     ),
#                 ]
#             )
#         ),
#         html.Td(id="ice_row_steel_value"),
#     ]
# )
# row4 = html.Tr(
#     [
#         html.Td(
#             dbc.Row(
#                 [
#                     dbc.Col(html.P("Structural Timber :"), width=3),
#                     dbc.Col(
#                         dbc.Select(
#                             options=ice_options.timber,
#                             id="ice_row_timber",
#                             value=0.51,
#                         )
#                     ),
#                 ]
#             ),
#         ),
#         html.Td(id="ice_row_timber_value"),
#     ]
# )
# table_body = [html.Tbody([row1, row2, row3, row4])]

# ice_card = dbc.Card(
#     [
#         html.H3("ICE Database", className="mb-3 display-5"),
#         html.Hr(),
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     html.Div(
#                                         id="ice_analysis_total", className="text-center"
#                                     )
#                                 ),
#                                 dbc.Col(
#                                     html.Div(
#                                         id="ice_analysis_gfa", className="text-center"
#                                     )
#                                 ),
#                             ],
#                             className="mb-3",
#                         ),
#                         dbc.Table(
#                             table_header + table_body,
#                             striped=True,
#                             bordered=True,
#                             hover=True,
#                         ),
#                     ],
#                     style={"width": "75%"},
#                 ),
#                 dcc.Graph(id="ice_pie", config=config),
#             ],
#             className="hstack",
#         ),
#         dmc.Accordion(
#             [
#                 dmc.AccordionItem(
#                     children=analysis_more_info.ice_more_info,
#                     label="More Information and Analysis",
#                 )
#             ],
#             id="gb_accordion",
#             state={"0": False},
#         ),
#     ],
#     class_name="my-5 p-4 shadow",
# )


# @callback(
#     Output("ice_row_concrete_value", "children"),
#     Output("ice_row_rebar_value", "children"),
#     Output("ice_row_steel_value", "children"),
#     Output("ice_row_timber_value", "children"),
#     Output("ice_analysis_total", "children"),
#     Output("ice_analysis_gfa", "children"),
#     Output("ice_pie", "figure"),
#     Input("ice_row_concrete", "value"),
#     Input("ice_row_rebar", "value"),
#     Input("ice_row_steel", "value"),
#     Input("ice_row_timber", "value"),
#     State("main_store", "data"),
#     State("gfa_store", "data"),
# )
# def ice_row_update(concrete, rebar, steel, timber, data, gfa):
#     return analysis_cards_layout(concrete, rebar, steel, timber, data, gfa, is_ice=True)


# def analysis_cards_layout(concrete, rebar, steel, timber, data, gfa, is_ice=False):
#     if gfa is not None or gfa != 0:
#         df = pd.read_json(data, orient="split")

#         mat, vol, mass, floor, layer, ec = funcs.ec_calculator(
#             df,
#             float(concrete),
#             float(rebar),
#             float(timber),
#             float(steel),
#             if_ice=is_ice,
#         )
#         df_calc = pd.DataFrame(
#             {
#                 "materials": mat,
#                 "volume": vol,
#                 "mass": mass,
#                 "floor": floor,
#                 "layer": layer,
#                 "ec": ec,
#             }
#         )
#         df_grouped = df_calc.groupby(by=["materials"], as_index=False).sum()

#         total = html.Div(
#             [
#                 html.H3("{:,.2f}".format(df_grouped["ec"].sum())),
#                 html.P([html.Span("kgCO2e ", className="fs-4"), "Total EC"]),
#             ],
#             style={"display": "block"},
#         )

#         gfa_calc = html.Div(
#             [
#                 html.H3(["{:,.2f}".format(np.around(sum(ec) / gfa, 2))]),
#                 html.P([html.Span("kgCO2e/m² ", className="fs-4"), "EC per m²"]),
#             ],
#             style={"display": "block"},
#         )

#         fig = px.pie(
#             df_calc,
#             values=df_calc["ec"],
#             names=df_calc["materials"],
#             color=df_calc["materials"],
#             hole=0.5,
#             color_discrete_map={
#                 "Concrete": "#5463ff",
#                 "Reinforcement Bar": "#ffc300",
#                 "STEEL - STRUCTURAL": "#79b159",
#                 "TIMBER - STRUCTURAL": "#74d7f7",
#             },
#         )

#         return (
#             html.P(
#                 "{:,.2f}".format(
#                     funcs.none_check(
#                         df_grouped.loc[
#                             df_grouped["materials"] == "Concrete", "ec"
#                         ]  # .values[0]
#                     )
#                 ),
#                 className="text-center",
#             ),
#             html.P(
#                 "{:,.2f}".format(
#                     funcs.none_check(
#                         df_grouped.loc[
#                             df_grouped["materials"] == "Reinforcement Bar", "ec"
#                         ]  # .values[0]
#                     )
#                 ),
#                 className="text-center",
#             ),
#             html.P(
#                 "{:,.2f}".format(
#                     funcs.none_check(
#                         df_grouped.loc[
#                             df_grouped["materials"] == "STEEL - STRUCTURAL", "ec"
#                         ]  # .values[0]
#                     )
#                 ),
#                 className="text-center",
#             ),
#             html.P(
#                 "{:,.2f}".format(
#                     funcs.none_check(
#                         df_grouped.loc[
#                             df_grouped["materials"] == "TIMBER - STRUCTURAL", "ec"
#                         ]  # .values[0]
#                     )
#                 ),
#                 className="text-center",
#             ),
#             total,
#             gfa_calc,
#             fig,
#         )
#     else:
#         raise PreventUpdate
