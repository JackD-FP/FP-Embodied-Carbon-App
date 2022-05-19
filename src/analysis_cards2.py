import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config, graph_colors
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from src import (
    analysis_more_info,
    epic_options,
    funcs,
    greenbook_options,
    ice_options,
    analysis_class,
)

greenbook = analysis_class.analysis_rows("row_timber_value")


greenbook_layout = dbc.Card(
    [
        html.H3("Green Book Database"),
        dmc.Divider(class_name="my-5"),
        html.Div(id="test_table"),
        # dmc.SimpleGrid([dmc.Table([html.Tbody(greenbook.row_generate())])], cols=2),
    ],
    class_name="my-5 p-4 shadow",
)


@callback(
    Output("test_table", "children"),
    Input("proc_store", "modified_timestamp"),
    State("proc_store", "data"),
)
def definition(mts, data):
    if mts is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        gb = analysis_class.cards(df, "Green Book EC")

        return gb.total_calc()
