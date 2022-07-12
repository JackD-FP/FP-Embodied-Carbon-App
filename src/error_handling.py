import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash_iconify import DashIconify


# checks column headers if the names are correct
# if its not the names below:
# Level, Layer, Volume, Material, Mass
def head_check(data):
    col_names = list(data.columns)
    print(col_names)
