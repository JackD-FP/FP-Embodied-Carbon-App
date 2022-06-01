import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from src import greenbook_options
import re
from config import config
from dash_iconify import DashIconify

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
    ],
    Input("gb_analysis_store", "data"),
    State("epic_analysis_store", "data"),
    State("ice_analysis_store", "data"),
    State("proc_store", "data"),
)
def definition(gb, epic, ice, proc):
    if proc is None:
        raise PreventUpdate
    elif epic is None or ice is None:
        df = pd.read_json(proc, orient="split")
        df_grouped = df.groupby(["Materials"], as_index=False).sum()
        df_mat = df["Materials"].unique()
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
        color_dict = dict(zip(df_mat, colors))
        epic_fig_pie = px.pie(
            df_grouped,
            values="EPiC EC",
            color="Materials",
            names="Materials",
            color_discrete_map=color_dict,
        )
        epic_fig_bar = px.histogram(
            df,
            x="Floor Level",
            y="EPiC EC",
            color="Materials",
            title="Embodied Carbon",
            color_discrete_map=color_dict,
        )

        ice_fig_pie = px.pie(
            df_grouped,
            values="ICE EC",
            color="Materials",
            names="Materials",
            color_discrete_map=color_dict,
        )
        ice_fig_bar = px.histogram(
            df,
            x="Floor Level",
            y="ICE EC",
            color="Materials",
            title="Embodied Carbon",
            color_discrete_map=color_dict,
        )

        gb_df = pd.read_json(gb, orient="split")
        gb_df_grouped = gb_df.groupby(["Sub-Material"], as_index=False).sum()
        color_names = gb_df["Sub-Material"].unique().tolist()

        gb_color_dict = dict(zip(color_names, colors))

        # generate green book pie and bar figs
        gb_fig_pie = px.pie(
            gb_df_grouped,
            values="EC Value",
            color="Sub-Material",
            names="Sub-Material",
            color_discrete_map=gb_color_dict,
        )
        gb_fig_bar = px.histogram(
            gb_df,
            x="Floor Level",
            y="EC Value",
            color="Sub-Material",
            color_discrete_map=gb_color_dict,
        )

        return (
            gb_fig_pie,
            gb_fig_bar,
            epic_fig_pie,
            epic_fig_bar,
            ice_fig_pie,
            ice_fig_bar,
        )
    else:
        gb_df = pd.read_json(gb, orient="split")
        gb_df_grouped = gb_df.groupby(["Sub-Material"], as_index=False).sum()
        gb_color_names = gb_df["Sub-Material"].unique().tolist()

        epic_df = pd.read_json(epic, orient="split")
        epic_df_grouped = epic_df.groupby(["Sub-Material"], as_index=False).sum()
        epic_color_names = epic_df["Sub-Material"].unique().tolist()

        ice_df = pd.read_json(ice, orient="split")
        ice_df_grouped = ice_df.groupby(["Sub-Material"], as_index=False).sum()
        ice_color_names = ice_df["Sub-Material"].unique().tolist()
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
        gb_color_dict = dict(zip(gb_color_names, colors))
        epic_color_dict = dict(zip(epic_color_names, colors))
        ice_color_dict = dict(zip(ice_color_names, colors))

        gb_fig_pie = px.pie(
            gb_df_grouped,
            values="EC Value",
            color="Sub-Material",
            names="Sub-Material",
            color_discrete_map=gb_color_dict,
        )
        gb_fig_bar = px.histogram(
            gb_df,
            x="Floor Level",
            y="EC Value",
            color="Sub-Material",
            color_discrete_map=gb_color_dict,
        )
        epic_fig_pie = px.pie(
            epic_df_grouped,
            values="EC Value",
            color="Sub-Material",
            names="Sub-Material",
            color_discrete_map=epic_color_dict,
        )
        epic_fig_bar = px.histogram(
            epic_df,
            x="Floor Level",
            y="EC Value",
            color="Sub-Material",
            color_discrete_map=epic_color_dict,
        )
        ice_fig_pie = px.pie(
            ice_df_grouped,
            values="EC Value",
            color="Sub-Material",
            names="Sub-Material",
            color_discrete_map=ice_color_dict,
        )
        ice_fig_bar = px.histogram(
            ice_df,
            x="Floor Level",
            y="EC Value",
            color="Sub-Material",
            color_discrete_map=ice_color_dict,
        )

        # update figures
        gb_fig_pie.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": 1.3,
                "xanchor": "center",
                "x": 0.5,
            }
        )
        gb_fig_bar.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": 1.3,
                "xanchor": "center",
                "x": 0.5,
            }
        )
        epic_fig_pie.update_layout(
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
        ice_fig_pie.update_layout(
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
        )


@callback(
    [
        Output("gb_analysis_comp_total", "children"),
        Output("gb_analysis_comp_benchmark", "children"),
        Output("epic_analysis_comp_total", "children"),
        Output("ice_analysis_comp_total", "children"),
        Output("ice_analysis_comp_benchmark", "children"),
    ],
    [
        Input("proc_store", "data"),
    ],
    [
        State("gb_analysis_store", "data"),
        State("epic_analysis_store", "data"),
        State("ice_analysis_store", "data"),
        State("nla_store", "data"),
        State("gia_store", "data"),
    ],
)
def totals_benchmark_update(
    proc_data, gb_data, epic_data, ice_data, nla_data, gia_data
):
    if proc_data is None:
        raise PreventUpdate
    else:
        gb_df = pd.read_json(gb_data, orient="split")
        epic_df = pd.read_json(epic_data, orient="split")
        ice_df = pd.read_json(ice_data, orient="split")

        return (
            "{:,.2f}".format(gb_total := gb_df["EC Value"].sum()),
            "{:,.2f}".format(gb_total / nla_data),
            "{:,.2f}".format(epic_df["EC Value"].sum()),
            "{:,.2f}".format(ice_total := ice_df["EC Value"].sum()),
            "{:,.2f}".format(ice_total / gia_data),
        )


comparison = html.Div(
    children=[
        dmc.Divider(class_name="my-5"),
        html.Div(
            children=[
                html.H5("Analysis Comparison", className="mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("Green Book DB", className="mt-3 mb-5"),
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
                            md=4,
                        ),
                        dbc.Col(
                            [
                                html.H3("EPiC DB", className="mt-3 mb-5"),
                                html.Div(
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
                            md=4,
                        ),
                        dbc.Col(
                            [
                                html.H3("ICE DB", className="mt-3 mb-5"),
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
                            md=4,
                        ),
                    ]
                ),
            ]
        ),
    ]
)
