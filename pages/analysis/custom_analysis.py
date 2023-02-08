import json
import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from flask import g
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from src import analysis_comparison, funcs, material_options

from pages.analysis import epic_db, green_book_db, ice_db

layout = html.Div(
    children=[
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    label="Green Book DB",
                    children=[
                        green_book_db.gb_layout,
                    ],
                ),
                dmc.AccordionItem(
                    label="EPiC DB",
                    children=[
                        epic_db.epic_layout,
                    ],
                ),
                dmc.AccordionItem(
                    label="ICE DB",
                    children=[
                        ice_db.ice_layout,
                    ],
                ),
            ]
        ),
    ]
)
