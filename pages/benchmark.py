import json

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from src.firebase_init import bucket, db

benchmarks = [
    dmc.SegmentedControl(
        id="bmark_segment",
        data=["Total", "Superstructure", "Substructure"],
        value="Total",
        style={"position": "sticky", "top": "0"},
        disabled=False,
    ),
    dmc.Button(
        id="db_refresh",
        children="Refresh",
        variant="outline",
        leftIcon=[DashIconify(icon="ic:round-refresh")],
        size="xs",
        style={"margin": "0 0 0 1rem"},
        color="dark",
    ),
    html.Div(
        dcc.Graph(id="gb-benchmark-graph", style={"height": "50vh"}),
    ),
    dmc.Text("* Data taken from Footprint Company Greenbook DB"),
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
        html.Div(children=benchmarks),
        html.Div(id="for_refresh"),
        html.Div(id="bmark_test"),
        dcc.Store(id="benchmark_storage", storage_type="local"),
    ]
)


def db_yield():
    docs = db.collection("projects").stream()
    for doc in docs:
        yield doc.to_dict()


@callback(
    Output("benchmark_storage", "data"),
    Output("for_refresh", "children"),
    Input("url", "pathname"),
    Input("db_refresh", "n_clicks"),
    State("benchmark_storage", "data"),
)
def update_benchmark_graphs(url, n, data):
    if data is None:
        df = pd.DataFrame(db_yield())
        return df.to_json(orient="split"), None
    elif n:
        df = pd.DataFrame(db_yield())
        return df.to_json(orient="split"), dcc.Location("/pages/documentation")
    else:
        raise dash.exceptions.PreventUpdate


def scatter_plot(df, db: str, desc: str):
    """reusable function for scatter plot

    Args:
        df (pd.dataframe): dataframe for the graph
        db (str): specific column to plot
        desc (str): description of the graph

    Returns:
        dash component: scatter plot
    """
    return px.scatter(
        df,
        x="datetime",
        y=db,
        color="project_name",
        title=desc,
        # labels={"gb": "Greenbook"},
    )


def graphing_output(df, col_name, title):
    """return scatter plot for total structures

    Args:
        df (pd.dataframe): dataframe for the graph

    Returns:
        tuple: (greenbook, epic, ice)
    """
    return (
        scatter_plot(df, col_name, "Greenbook {} Benchmark".format(title)),
        scatter_plot(df, col_name, "EPiC {} Benchmark".format(title)),
        scatter_plot(df, col_name, "ICE {} Benchmark".format(title)),
    )


graphing = {
    "Total": "",
    "Superstructure": "super_",
    "Substructure": "sub_",
}


@callback(
    Output("gb-benchmark-graph", "figure"),
    Input("bmark_segment", "value"),
    Input("benchmark_storage", "data"),
)
def update_gb_bmark(segment, data):  # TODO: fix this
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                name="Greenbook",
                mode="markers",
                x=df["project_name"],
                y=df["{}greenbook".format(graphing.get(segment))],
                text=df["variation_name"],
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e",
                marker=dict(
                    color="#BDC667",
                    size=12,
                    symbol="circle",
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                name="EPIC",
                mode="markers",
                x=df["project_name"],
                y=df["{}epic".format(graphing.get(segment))],
                text=df["variation_name"],
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e",
                marker=dict(
                    color="#7F6A93",
                    size=12,
                    symbol="square",
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                name="ICE",
                mode="markers",
                x=df["project_name"],
                y=df["{}ice".format(graphing.get(segment))],
                text=df["variation_name"],
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e",
                marker=dict(
                    color="#52A9D1",
                    size=12,
                    symbol="cross",
                ),
            )
        )
        fig.add_hline(
            y=350,
            line_dash="dash",
            annotation_text="LETI 2030 Design Targe Office",
            annotation_position="bottom right",
            annotation_font_size=10,
            line_width=1,
        )

        fig.add_hline(
            y=300,
            line_dash="dash",
            annotation_text="LETI 2030 Design Targe Residential, Education, & Retail*",
            annotation_position="bottom right",
            annotation_font_size=10,
            line_width=1,
        )

        fig.add_hline(
            y=600,
            line_dash="dash",
            annotation_text="Class 5 Office - Premium*",
            annotation_position="bottom right",
            annotation_font_size=10,
            line_width=1,
        )

        fig.add_hline(
            y=900,
            line_dash="dash",
            annotation_text="Class 5 Office - A Grade*",
            annotation_position="bottom right",
            annotation_font_size=10,
            line_width=1,
            # line_color = "#BDC667"
        )

        fig.update_layout(
            title="Embodied Carbon Benchmark",
            xaxis_title="Projects",
            yaxis_title="kgCO2e",
        )
        return fig


@callback(
    Output("epic-benchmark-graph", "figure"),
    Input("bmark_segment", "value"),
    Input("benchmark_storage", "data"),
)
def update_epic_bmark(segment, data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        return graphing_output(df, "{}epic".format(graphing.get(segment)), segment)[1]


@callback(
    Output("ice-benchmark-graph", "figure"),
    Input("bmark_segment", "value"),
    Input("benchmark_storage", "data"),
)
def update_ice_bmark(segment, data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        return graphing_output(df, "{}ice".format(graphing.get(segment)), segment)[2]
