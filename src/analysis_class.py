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

from src import analysis_more_info, epic_options, funcs, greenbook_options, ice_options


class analysis_rows:
    """Class to keep track and generate which building element has certain materials in it"""

    def __init__(self, mat_id):
        self.mat_id = mat_id

    def row_generate(self):
        row = [
            html.Tr(
                [
                    html.Td(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Reinforcement Bar:"),
                                        width=3,
                                    ),
                                    dbc.Col(
                                        dbc.Select(
                                            options=greenbook_options.rebar,
                                            id="row_rebar",
                                            value=2.900,
                                        )
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.Td("Carbon"),
                ]
            ),
            html.Td(id=self.mat_id),
        ]
        return row


class element:
    """Class to generate and store building element, materials and embodied carbon of their respective database"""

    def __init__(self, concrete, rebar, steel, timber):
        self.concrete = concrete
        self.rebar = rebar
        self.steel = steel
        self.timber = timber


class cards:
    """class for each cards of each database"""

    def __init__(self, df, db_name):
        self.df = df
        self.db_name = db_name

        # total calc method

    def total_calc(self):
        return np.around(self.df[self.db_name].sum(), 2)
