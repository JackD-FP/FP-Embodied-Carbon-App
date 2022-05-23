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
#     analysis_more_info,
#     class_Lib,
#     epic_options,
#     funcs,
#     greenbook_options,
#     ice_options,
# )

# # greenbook_layout = html.Div(id="gb")
# # epic_layout = html.Div(id="epic")
# # ice_layout = html.Div(id="ice")


# @callback(
#     Output("gb", "children"),
#     Output("epic", "children"),
#     Output("ice", "children"),
#     Input("proc_store", "modified_timestamp"),
#     State("proc_store", "data"),
# )
# def gb_update(mts, data):
#     if mts is None:
#         raise PreventUpdate
#     else:
#         df = pd.read_json(data, orient="split")
#         gb = class_Lib.gen_cards(df, "Green Book EC")
#         epic = class_Lib.gen_cards(df, "EPiC EC")
#         ice = class_Lib.gen_cards(df, "ICE EC")
#         return gb.card(), epic.card(), ice.card()
