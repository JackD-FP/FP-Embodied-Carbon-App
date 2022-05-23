import re
from dataclasses import dataclass
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config, graph_colors
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from index import app

from src import analysis_more_info, epic_options, funcs, greenbook_options, ice_options


class cards:
    """class for each cards of each database"""

    def __init__(self, df, db_name):
        self.df = df
        self.db_name = db_name
        self.app = app

        # total calc method

    def __str__(self) -> str:
        return "{:,}".format(np.around(self.df[self.db_name].sum(), 2))


class gen_cards:
    def __init__(self, df, db_name, tab_name, tab_content, area=None):
        self.df = df
        self.db_name = db_name
        self.tab_name = tab_name
        self.tab_content = tab_content
        self.area = area

    def __str__(self) -> str:
        total = "{:,}".format(np.around(self.df[self.db_name].sum(), 2))
        return total

    def benchmark(self):
        if self.area is None:
            return "No Benchmark Available"
        else:
            benchmark = self.df[self.db_name].sum() / self.area
            return np.around(benchmark, 2)

    def card(self):
        return dbc.Card(
            [
                html.H3(self.db_name, className="display-6"),
                dmc.Divider(class_name="mb-5"),
                dmc.SimpleGrid(
                    cols=2,
                    children=[
                        dmc.Col(
                            [
                                dmc.SimpleGrid(
                                    children=[
                                        dmc.Col(
                                            children=[
                                                html.H4(
                                                    self.__str__(),
                                                    className="text-center",
                                                ),
                                                html.P(
                                                    ["kgCO₂e", html.P("Total EC")],
                                                    className="text-center",
                                                ),
                                            ]
                                        ),
                                        dmc.Col(
                                            children=[
                                                html.H4(
                                                    self.benchmark(),
                                                    className="text-center",
                                                ),
                                                html.P(
                                                    [
                                                        "kgCO₂e per m²",
                                                        html.P("Building Benchmark"),
                                                    ],
                                                    className="text-center",
                                                ),
                                            ]
                                        ),
                                    ],
                                    cols=2,
                                    class_name="mb-5",
                                ),
                                # span=6,
                                dmc.Tabs(
                                    id=self.tab_name,
                                    grow=False,
                                    active=0,
                                    children=[
                                        dmc.Tab(label="Beams"),
                                        dmc.Tab(label="Columns"),
                                        dmc.Tab(label="Slabs"),
                                        dmc.Tab(label="Walls"),
                                        dmc.Tab(label="Stairs"),
                                    ],
                                ),
                                # content for tab divs
                                html.Div(id=self.tab_content),
                                # tab_div(self.tab_content),
                            ]
                        ),
                        dmc.Col(html.Div("potato")),
                    ],
                ),
            ],
            class_name="my-5 p-4 shadow",
        )


class tab_content:
    def __init__(self, active) -> None:
        self.active = active
        # self.df = df

    def tab(self):
        content = {
            0: html.P("asdasdasd"),
            1: html.P("asdf"),
            2: html.P("zxcv"),
            3: html.P("qwerqwe"),
            4: html.P("tyuityui"),
        }
        return content.get(self.active)


# ---- Callbacks -----
# we can refactor these callbacks to parent class gen_cards
# however we may need to refactor the whole APP and properly use classes
# to instantiate server, app and layout... ugghhh


@callback(
    Output("gb_content", "children"),
    Input("gb_tab", "active"),
)
def update_tab(x):
    return tab_content(x).tab()


@callback(
    Output("epic_content", "children"),
    Input("epic_tab", "active"),
)
def update_tab(x):
    return tab_content(x).tab()


@callback(
    Output("ice_content", "children"),
    Input("ice_tab", "active"),
)
def update_tab(x):
    return tab_content(x).tab()
