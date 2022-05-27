# import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# import dash_mantine_components as dmc
# from dash import Input, Output, callback, dcc, html, State
# from dash.exceptions import PreventUpdate
# from src import analysis_card_gb, analysis_cards, greenbook_options

# gb_df = pd.read_csv("src/Greenbook _reduced.csv")

# layout = html.Div(
#     [
#         dcc.Store(id="gb_store"),
#         html.H1("Analysis", className="display-2 mb-5 "),
#         html.Hr(),
#         html.Div(analysis_card_gb.gb_layout),
#         html.Div(id="epic"),
#         html.Div(id="ice"),
#     ],
#     id="analysis_div",
# )


# def cards(name, total, benchmark, tab_id, tab_content_id):
#     return dbc.Card(
#         [
#             html.H3(name, className="display-6"),
#             dmc.Divider(class_name="mb-5"),
#             dmc.SimpleGrid(
#                 cols=2,
#                 children=[
#                     dmc.Col(
#                         [
#                             dmc.SimpleGrid(
#                                 children=[
#                                     dmc.Col(
#                                         children=[
#                                             html.H4(
#                                                 "{:,}".format(total),
#                                                 className="text-center",
#                                             ),
#                                             html.P(
#                                                 [
#                                                     "kgCO₂e",
#                                                     dmc.Text("Total EC", color="gray"),
#                                                 ],
#                                                 className="text-center",
#                                             ),
#                                         ]
#                                     ),
#                                     dmc.Col(
#                                         children=[
#                                             html.H4(
#                                                 "{:,}".format(benchmark),
#                                                 className="text-center",
#                                             ),
#                                             html.P(
#                                                 [
#                                                     "kgCO₂e per m²",
#                                                     dmc.Text(
#                                                         "Building Benchmark",
#                                                         color="gray",
#                                                     ),
#                                                 ],
#                                                 className="text-center",
#                                             ),
#                                         ]
#                                     ),
#                                 ],
#                                 cols=2,
#                                 class_name="mb-5",
#                             ),
#                             # span=6,
#                             dbc.Tabs(
#                                 id=tab_id,
#                                 active_tab="Beams",
#                                 children=[
#                                     dbc.Tab(label="Beams"),
#                                     dbc.Tab(label="Columns"),
#                                     dbc.Tab(label="Slabs"),
#                                     dbc.Tab(label="Walls"),
#                                     dbc.Tab(label="Stairs"),
#                                 ],
#                             ),
#                             # content for tab divs
#                             html.Div(id=tab_content_id),
#                             # tab_div(self.tab_content),
#                         ]
#                     ),
#                     dmc.Col(html.Div("potato")),
#                 ],
#             ),
#         ],
#         class_name="my-5 p-4 shadow",
#     )


# def row_gen(mat_name, value):
#     row = html.Tr(
#         [
#             html.Td(
#                 [
#                     dmc.Grid(
#                         children=[
#                             dmc.Col(
#                                 dmc.Text(
#                                     mat_name,
#                                     weight=500,
#                                     color="gray",
#                                 ),
#                                 span=3,
#                             ),
#                             dmc.Col(
#                                 dbc.Select(
#                                     options=greenbook_options.concrete, persistence=True
#                                 ),
#                                 span=9,
#                             ),
#                         ],
#                         align="center",
#                     ),
#                 ],
#                 className="px-3 w-75",
#             ),
#             html.Td(value, className="px-3 align-middle"),
#         ]
#     )
#     return row


# def tab_contents(value):
#     header = [
#         html.Thead(
#             html.Tr(
#                 [
#                     html.Th("Materials"),
#                     html.Th("Embodied Carbon"),
#                 ]
#             )
#         )
#     ]
#     row1 = row_gen("Concrete", value)
#     return dbc.Tab(header + [row1])


# @callback(
#     Output("gb", "children"),
#     Output("epic", "children"),
#     Output("ice", "children"),
#     Input("proc_store", "modified_timestamp"),
#     Input("nla_store", "modified_timestamp"),
#     Input("gia_store", "modified_timestamp"),
#     State("proc_store", "data"),
#     State("nla_store", "data"),
#     State("gia_store", "data"),
# )
# def gb_update(mts, nla_mts, gia_mts, data, nla_data, gia):
#     if mts is None or nla_mts is None or gia_mts is None:
#         raise PreventUpdate
#     else:
#         df = pd.read_json(data, orient="split")

#         gb_card = cards(
#             name := "Green Book EC",
#             gb_total := np.around(df[name].sum(), 2),
#             np.around(gb_total / nla_data),
#             "gb_tab",
#             "gb_content",
#         )

#         return gb_card, "test", "test"


# @callback(
#     Output("gb_content", "children"),
#     Input("gb_tab", "active_tab"),
#     State("proc_store", "data"),
# )
# def tab_content_update(active, data):
#     if data is None:
#         raise PreventUpdate
#     else:
#         df = pd.read_json(data, orient="split")

#         if active == "Beams":
#             return tab_contents("asdasdasd")
#         elif active == "Columns":
#             return tab_contents("qwerqwe")
#         elif active == "Slabs":
#             return tab_contents("asdfasdf")
#         elif active == "Walls":
#             return tab_contents("zxcvzxcv")
#         elif active == "Stairs":
#             return tab_contents("uiopuio")

#         # content = {
#         #     "Beams": tab_contents(0.6),
#         #     "Columns": html.P("asdf"),
#         #     "Sabs": html.P("zxcv"),
#         #     "Walls": html.P("qwerqwe"),
#         #     "Stairs": html.P("tyuityui"),
#         # }
#         # return content.get(active)
