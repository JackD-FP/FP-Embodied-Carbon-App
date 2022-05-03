import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from config import config
from dash import Input, Output, State, callback, dash_table, dcc, html
from src import funcs
from dash.exceptions import PreventUpdate

from src import funcs

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

gb_more_info = [
    html.H3("Embodied Carbon per Floor From Green Book Database"),
    dmc.LoadingOverlay(
        children=dcc.Graph(id="gb_bar", config=config),
        loaderProps={"variant": "dots", "color": "violet", "size": "xl"},
    ),
]

epic_more_info = [
    html.H3("Embodied Carbon per Floor From Epic Database"),
    dmc.LoadingOverlay(
        children=dcc.Graph(id="epic_bar", config=config),
        loaderProps={"variant": "dots", "color": "violet", "size": "xl"},
    ),
]

ice_more_info = [
    html.H3("Embodied Carbon per Floor From Ice Database"),
    dmc.LoadingOverlay(
        children=dcc.Graph(id="ice_bar", config=config),
        loaderProps={"variant": "dots", "color": "violet", "size": "xl"},
    ),
]


@callback(
    Output("gb_bar", "figure"),
    Output("epic_bar", "figure"),
    Output("ice_bar", "figure"),
    Input("row_concrete", "value"),
    Input("row_rebar", "value"),
    Input("row_steel", "value"),
    Input("row_timber", "value"),
    Input("epic_row_concrete", "value"),
    Input("epic_row_rebar", "value"),
    Input("epic_row_steel", "value"),
    Input("epic_row_timber", "value"),
    Input("ice_row_concrete", "value"),
    Input("ice_row_rebar", "value"),
    Input("ice_row_steel", "value"),
    Input("ice_row_timber", "value"),
    State("main_store", "data"),
)
def bar_update(
    gb_conc_value,
    gb_rebar_value,
    gb_steel_value,
    gb_timber_value,
    epic_conc_value,
    epic_rebar_value,
    epic_steel_value,
    epic_timber_value,
    ice_conc_value,
    ice_rebar_value,
    ice_steel_value,
    ice_timber_value,
    data,
):
    if data is not None:
        df = pd.read_json(data, orient="split")
        mat, vol, mass, floor, layer, gb_ec, epic_ec, ice_ec = funcs.mat_interpreter(
            df,
            float(gb_conc_value),
            float(epic_conc_value),
            float(ice_conc_value),
            float(gb_rebar_value),
            float(epic_rebar_value),
            float(ice_rebar_value),
            float(gb_steel_value),
            float(epic_steel_value),
            float(ice_steel_value),
            float(gb_timber_value),
            float(epic_timber_value),
            float(ice_timber_value),
        )
        df_new = pd.DataFrame(
            {
                "Floor Level": floor,
                "Layer": layer,
                "Materials": mat,
                "Mass": mass,
                "Volume": vol,
                "Green Book EC": gb_ec,
                "EPiC EC": epic_ec,
                "ICE EC": ice_ec,
            }
        )

        labels = df_new["Floor Level"].unique()
        df = df_new.groupby(["Floor Level", "Materials"], as_index=False).sum()

        # label_colors = funcs.label_colours_update(labels, "dict")
        label_colors = {
            "Concrete": "#5463ff",
            "Reinforcement Bar": "#ffc300",
            "STEEL - STRUCTURAL": "#79b159",
            "TIMBER - STRUCTURAL": "#74d7f7",
        }

        gb_fig = px.bar(
            df,
            x="Floor Level",
            y="Green Book EC",
            color="Materials",
            color_discrete_map=label_colors,
            labels={
                "Green Book EC": "Embodied Carbon (kgCO2e)",
                "Materials": "Materials",
                "Floor Level": "Level",
            },
        )

        epic_fig = px.bar(
            df,
            x="Floor Level",
            y="EPiC EC",
            color="Materials",
            color_discrete_map=label_colors,
            labels={
                "EPiC EC": "Embodied Carbon (kgCO2e)",
                "Materials": "Materials",
                "Floor Level": "Level",
            },
        )

        ice_fig = px.bar(
            df,
            x="Floor Level",
            y="ICE EC",
            color="Materials",
            color_discrete_map=label_colors,
            labels={
                "ICE EC": "Embodied Carbon (kgCO2e)",
                "Materials": "Materials",
                "Floor Level": "Level",
            },
        )
        # return gb_fig, epic_fig, ice_fig
        return gb_fig, epic_fig, ice_fig
    else:
        raise PreventUpdate


def ec_calc(database, df, conc_value, steel_value, timber_value):
    ec_list = []
    for i, row in df.iterrows():
        if re.search("CONCRETE", row["Materials"], re.IGNORECASE):
            if database == "gb":
                ec = (
                    gb_df.loc[
                        gb_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = (
                    epic_df.loc[
                        epic_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = (
                    ice_df.loc[
                        ice_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            else:
                print("error only gb, epic, ice")

        elif re.search("steel", row["Materials"], re.IGNORECASE):
            if database == "gb":
                ec = (
                    gb_df.loc[
                        gb_df["Sub Category"] == steel_value, "Embodied Carbon"
                    ].values[0]
                    * row["Mass"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = (
                    epic_df.loc[
                        epic_df["Sub Category"] == steel_value, "Embodied Carbon"
                    ].values[0]
                    * row["Mass"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = (
                    ice_df.loc[
                        ice_df["Sub Category"] == steel_value, "Embodied Carbon"
                    ].values[0]
                    * row["Mass"]
                )
                ec_list.append(np.around(ec, 2))
            else:
                print("error only gb, epic, ice")

        elif re.search("timber", row["Materials"], re.IGNORECASE):
            if database == "gb":
                ec = (
                    gb_df.loc[
                        gb_df["Sub Category"] == timber_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = (
                    epic_df.loc[
                        epic_df["Sub Category"] == timber_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = (
                    ice_df.loc[
                        ice_df["Sub Category"] == timber_value, "Embodied Carbon"
                    ].values[0]
                    * row["Mass"]
                )
                ec_list.append(np.around(ec, 2))
            else:
                print("error only gb, epic, ice")

        else:  # if empty or unknown... it just defualts it to concrete
            if database == "gb":
                ec = (
                    gb_df.loc[
                        gb_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = (
                    epic_df.loc[
                        epic_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = (
                    ice_df.loc[
                        ice_df["Sub Category"] == conc_value, "Embodied Carbon"
                    ].values[0]
                    * row["Net Volume"]
                )
                ec_list.append(np.around(ec, 2))
            else:
                print("error only gb, epic, ice")
    return ec_list
