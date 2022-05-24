import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
from src import ice_options
from analysis_card_gb import table

epic_layout = [
    dbc.Card(
        [
            dcc.Store(id="epic_store"),
            html.H3("EPiC DB"),
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
                                            html.H4(  # total
                                                id="epic_analysis_total",
                                                # "{:,}".format(total),
                                                className="text-center",
                                            ),
                                            html.P(
                                                [
                                                    "kgCO₂e",
                                                    dmc.Text("Total EC", color="gray"),
                                                ],
                                                className="text-center",
                                            ),
                                        ]
                                    ),
                                    dmc.Col(
                                        children=[
                                            html.H4(  # Benchmarks
                                                id="epic_analysis_benchmark",
                                                # "{:,}".format(benchmark),
                                                className="text-center",
                                            ),
                                            html.P(
                                                [
                                                    "kgCO₂e per m²",
                                                    dmc.Text(
                                                        "Building Benchmark",
                                                        color="gray",
                                                    ),
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
                            dbc.Tabs(
                                id="epic_tabs",
                                active_tab="Beams",
                                children=[
                                    dbc.Tab(label="Beams", tab_id="Beams"),
                                    dbc.Tab(label="Columns", tab_id="Columns"),
                                    dbc.Tab(label="Slabs", tab_id="Slabs"),
                                    dbc.Tab(label="Walls", tab_id="Walls"),
                                    dbc.Tab(label="Stairs", tab_id="Stairs"),
                                ],
                            ),
                            # content for tab divs
                            html.Div(id="epic_tab_content", className="p-5"),
                            # tab_div(self.tab_content),
                        ]
                    ),
                    dmc.Col(html.Div("potato")),
                ],
            ),
        ],
        class_name="my-5 p-4 shadow",
    )
]
