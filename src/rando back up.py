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
