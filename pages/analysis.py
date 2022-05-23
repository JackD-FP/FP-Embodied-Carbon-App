import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
from src import analysis_cards, analysis_cards2, class_Lib

# gb_df = pd.read_csv("src/Greenbook _reduced.csv")

layout = html.Div(
    [
        html.H1("Analysis", className="display-2 mb-5 "),
        html.Hr(),
        html.Div(id="gb"),
        html.Div(id="epic"),
        html.Div(id="ice"),
    ],
    id="analysis_div",
)


@callback(
    Output("gb", "children"),
    Output("epic", "children"),
    Output("ice", "children"),
    Input("proc_store", "modified_timestamp"),
    Input("nla_store", "modified_timestamp"),
    Input("gia_store", "modified_timestamp"),
    State("proc_store", "data"),
    State("nla_store", "data"),
    State("gia_store", "data"),
)
def gb_update(mts, nla_mts, gia_mts, data, nla_data, gia):
    if mts is None or nla_mts is None or gia_mts is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        gb = class_Lib.gen_cards(df, "Green Book EC", "gb_tab", "gb_content", nla_data)
        epic = class_Lib.gen_cards(df, "EPiC EC", "epic_tab", "epic_content")
        ice = class_Lib.gen_cards(df, "ICE EC", "ice_tab", "ice_content", gia)

        return gb.card(), epic.card(), ice.card()


# greenbook_layout = html.Div(id="gb")
# epic_layout = html.Div(id="epic")
# ice_layout = html.Div(id="ice")

# @callback(
#     Output("table_div", "children"),
#     Input("proc_store", "data"),
# )
# def definition(data):
#     if data is not None:
#         df = pd.read_json(data, orient="split")
#         if "Embodied Carbon" in df.columns:
#             df = df.drop(["Embodied Carbon"], axis=1)
#         else:
#             pass

#         df = df.groupby(by=["Materials"], as_index=False).sum()
#         df.loc[:, "Mass"] = df["Mass"].map("{:,.2f}".format)
#         df.loc[:, "Volume"] = df["Volume"].map("{:,.2f}".format)
#         df.loc[:, "Green Book EC"] = df["Green Book EC"].map("{:,.2f}".format)
#         df.loc[:, "EPiC EC"] = df["EPiC EC"].map("{:,.2f}".format)
#         df.loc[:, "ICE EC"] = df["ICE EC"].map("{:,.2f}".format)

#         return html.Div(
#             [
#                 html.H3("Structure Schedule"),
#                 dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
#                 analysis_cards2.greenbook_layout,
#                 analysis_cards2.epic_layout,
#                 analysis_cards2.ice_layout,
#                 # analysis_cards.greenbook_card,
#                 # analysis_cards.epic_card,
#                 # analysis_cards.ice_card,
#             ]
#         )

#     elif data is None:
#         dbc.Alert(  # not sure why this is not working
#             [
#                 html.H1("UPLOAD you schule"),
#                 html.Hr(),
#                 html.P(
#                     "please upload your structure schedule in the dashboard page",
#                     className="h4",
#                 ),
#                 html.P("Happy designing! 😁"),
#             ],
#             is_open=True,
#             dismissable=True,
#         ),
