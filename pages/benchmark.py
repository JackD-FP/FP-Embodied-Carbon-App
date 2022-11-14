import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html

from src import firebase_init

benchmarks = [
    dmc.SegmentedControl(
        id="bmark_segment",
        data=["Total", "Superstructure", "Substructure"],
        style={"position": "sticky", "top": "0"},
    ),
    dcc.Graph(
        id="gb-benchmark-graph",
    ),
    dcc.Graph(
        id="epic-benchmark-graph",
    ),
    dcc.Graph(
        id="ice-benchmark-graph",
    ),
]

layout = html.Div(
    [
        html.H1("Benchmark", className="display-2 mb-5 "),
        html.Hr(className="mb-5"),
        html.Div(children=benchmarks, id="bmark"),
    ]
)
