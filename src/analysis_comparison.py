import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from config import config
from src import greenbook_options


# callback for analysis comparison
# kinda confusing but the callback is to generate graphs
# if => prevents update
# elif => updates green book graphs and use proc store for the rest
# else => updates all db with data, this requires users to open all the pages
@callback(
    [
        Output("gb_analysis_comp_pie", "figure"),
        Output("gb_analysis_comp_bar", "figure"),
        Output("epic_analysis_comp_pie", "figure"),
        Output("epic_analysis_comp_bar", "figure"),
        Output("ice_analysis_comp_pie", "figure"),
        Output("ice_analysis_comp_bar", "figure"),
        Output("gb_analysis_comp_pie", "config"),
        Output("gb_analysis_comp_bar", "config"),
        Output("epic_analysis_comp_pie", "config"),
        Output("epic_analysis_comp_bar", "config"),
        Output("ice_analysis_comp_pie", "config"),
        Output("ice_analysis_comp_bar", "config"),
    ],
    Input("analysis_store", "data"),
    Input("config_id", "data"),
)
def definition(data, config_data):
    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        gb_df = df.filter(
            items=["Green Book Material", "Green Book EC", "Floor Level", "Element"]
        )
        gb_df_grouped = df.groupby(
            ["Green Book Material", "Colors"], as_index=False
        ).sum()
        gb_vals = gb_df_grouped["Green Book Material"].to_list()
        gb_colors = gb_df_grouped["Colors"].to_list()
        # print(gb_vals, "\n\n", gb_colors, "\n\n", gb_df_grouped, "\n\n")
        gb_color_dict = dict(zip(gb_vals, gb_colors))

        epic_df = df.filter(
            items=["EPiC Material", "EPiC EC", "Floor Level", "Element"]
        )
        epic_df_grouped = df.groupby(["EPiC Material", "Colors"], as_index=False).sum()
        epic_vals = epic_df_grouped["EPiC Material"].to_list()
        epic_colors = epic_df_grouped["Colors"].to_list()
        epic_color_dict = dict(zip(epic_vals, epic_colors))

        ice_df = df.filter(items=["ICE Material", "ICE EC", "Floor Level", "Element"])
        ice_df_grouped = df.groupby(["ICE Material", "Colors"], as_index=False).sum()
        ice_vals = ice_df_grouped["ICE Material"].to_list()
        ice_colors = ice_df_grouped["Colors"].to_list()
        ice_color_dict = dict(zip(ice_vals, ice_colors))
        # ice_color_names = ice_df_grouped["ICE Material"].unique().tolist()

        gb_fig_pie = px.pie(
            gb_df_grouped,
            values="Green Book EC",
            color="Green Book Material",
            names="Green Book Material",
            color_discrete_map=gb_color_dict,
        )
        gb_fig_bar = px.histogram(
            gb_df,
            x="Floor Level",
            y="Green Book EC",
            color="Green Book Material",
            color_discrete_map=gb_color_dict,
        )
        epic_fig_pie = px.pie(
            epic_df_grouped,
            values="EPiC EC",
            color="EPiC Material",
            names="EPiC Material",
            color_discrete_map=epic_color_dict,
        )
        epic_fig_bar = px.histogram(
            epic_df,
            x="Floor Level",
            y="EPiC EC",
            color="EPiC Material",
            color_discrete_map=epic_color_dict,
        )
        ice_fig_pie = px.pie(
            ice_df_grouped,
            values="ICE EC",
            color="ICE Material",
            names="ICE Material",
            color_discrete_map=ice_color_dict,
        )
        ice_fig_bar = px.histogram(
            ice_df,
            x="Floor Level",
            y="ICE EC",
            color="ICE Material",
            color_discrete_map=ice_color_dict,
        )

        # update figures
        gb_fig_bar.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": 1.3,
                "xanchor": "center",
                "x": 0.5,
            }
        )
        epic_fig_bar.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": 1.3,
                "xanchor": "center",
                "x": 0.5,
            }
        )
        ice_fig_bar.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": 1.3,
                "xanchor": "center",
                "x": 0.5,
            }
        )
        return (
            gb_fig_pie,
            gb_fig_bar,
            epic_fig_pie,
            epic_fig_bar,
            ice_fig_pie,
            ice_fig_bar,
            config_data,
            config_data,
            config_data,
            config_data,
            config_data,
            config_data,
        )


@callback(
    [
        Output("gb_analysis_comp_total", "children"),
        Output("gb_analysis_comp_benchmark", "children"),
        Output("epic_analysis_comp_total", "children"),
        Output("epic_analysis_comp_benchmark", "children"),  # TODO: add benchmark
        Output("ice_analysis_comp_total", "children"),
        Output("ice_analysis_comp_benchmark", "children"),
    ],
    [
        Input("analysis_store", "data"),
    ],
    [
        State("nla_store", "data"),
        State("gia_store", "data"),
    ],
)
def totals_benchmark_update(data, nla, gia):
    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")

        return (
            "{:,.2f}".format(gb_total := df["Green Book EC"].sum()),
            "{:,.2f}".format(gb_total / nla),
            "{:,.2f}".format(epic_total := df["EPiC EC"].sum()),
            "{:,.2f}".format(epic_total / nla),
            "{:,.2f}".format(ice_total := df["ICE EC"].sum()),
            "{:,.2f}".format(ice_total / gia),
        )


comparison = html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Analysis Comparison", className="mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    "Green Book DB",
                                    className="mt-3 mb-5",
                                    style={"text-align": "center"},
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="gb_analysis_comp_total",
                                                            className="m-0",
                                                        ),
                                                        html.Strong(" kgCO₂e"),
                                                        html.P("Total EC"),
                                                    ],
                                                ),
                                            ],
                                            class_name="text-center",
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="gb_analysis_comp_benchmark",
                                                            className="m-0",
                                                        ),
                                                        html.Strong(" kgCO₂e/m²"),
                                                        html.P("Benchmark per NLA"),
                                                    ]
                                                ),
                                            ],
                                            class_name="text-center",
                                        ),
                                    ],
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(id="gb_analysis_comp_pie", config=config),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(id="gb_analysis_comp_bar", config=config),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                            ],
                            xxl=4,
                            md=12,
                        ),
                        dbc.Col(
                            [
                                html.H3(
                                    "EPiC DB",
                                    className="mt-3 mb-5",
                                    style={"text-align": "center"},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="epic_analysis_comp_total",
                                                            className="m-0",
                                                        ),
                                                        html.Strong("kgCO₂e"),
                                                        html.P("Total EC"),
                                                    ]
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="epic_analysis_comp_benchmark",
                                                            className="m-0",
                                                        ),
                                                        html.Strong(" kgCO₂e/m²"),
                                                        html.P("Benchmark per GIA"),
                                                    ]
                                                ),
                                            ],
                                            class_name="text-center",
                                        ),
                                    ]
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="epic_analysis_comp_pie", config=config
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="epic_analysis_comp_bar", config=config
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                            ],
                            xxl=4,
                            md=12,
                        ),
                        dbc.Col(
                            [
                                html.H3(
                                    "ICE DB",
                                    className="mt-3 mb-5",
                                    style={"text-align": "center"},
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="ice_analysis_comp_total",
                                                            className="m-0",
                                                        ),
                                                        html.Strong(" kgCO₂e"),
                                                        html.P("Total EC"),
                                                    ]
                                                ),
                                            ],
                                            class_name="text-center",
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Calculating...",
                                                            id="ice_analysis_comp_benchmark",
                                                            className="m-0",
                                                        ),
                                                        html.Strong(" kgCO₂e/m²"),
                                                        html.P("Benchmark per GIA"),
                                                    ]
                                                ),
                                            ],
                                            class_name="text-center",
                                        ),
                                    ],
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="ice_analysis_comp_pie", config=config
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                                dmc.LoadingOverlay(
                                    dcc.Graph(
                                        id="ice_analysis_comp_bar", config=config
                                    ),
                                    loaderProps={
                                        "color": "blue",
                                        "variant": "oval",
                                    },
                                ),
                            ],
                            xxl=4,
                            md=12,
                        ),
                    ]
                ),
            ]
        ),
    ]
)
