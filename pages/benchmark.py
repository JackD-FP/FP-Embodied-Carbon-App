import json

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from src.firebase_init import bucket, db

radio_option = [
    ["all", "ALL"],
    ["ftp", "Footprint Co. Benchmarks"],
    ["leti", "LETI 2030 Benchmark"],
]


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
    dmc.Text("Select benchmark", size="sm", weight=500),
    dmc.Text(
        "Select benchmark guidelines to show or hide",
        size="sm",
        color="gray",
    ),
    dmc.SegmentedControl(
        data=[
            {"value": "all", "label": "All"},
            {"value": "ftp", "label": "Footprint Co."},
            {"value": "leti", "label": "LETI 2030"},
            {"value": "none", "label": "None"},
        ],
        id="segment_bmark",
        value="all",
        size="sm",
    ),
    dmc.Text(
        "* Data taken from Footprint Company Green Book database. Based off 5 Star ratings",
        size="xs",
        color="gray",
    ),
    dmc.Text(
        "** Data taken from ICE database",
        size="xs",
        color="gray",
        style={"marginBottom": "2rem"},
    ),
    dmc.MultiSelect(
        label="Select a project",
        description="Select projects to view the benchmark. Press refresh to update selection",
        placeholder="One Shelley Street",
        searchable=True,
        nothingFound="No project found",
        maxSelectedValues=5,
        style={"width": 400},
        id="multiselect_project",
    ),
    dmc.Table(
        striped=False,
        highlightOnHover=True,
        id="bmark_table",
    ),
    # dcc.Graph(
    #     id="epic-benchmark-graph",
    # ),
    # dcc.Graph(
    #     id="ice-benchmark-graph",
    # ),
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


@callback(
    Output("multiselect_project", "data"),
    Input("benchmark_storage", "data"),
)
def update_multiselect(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        return [{"label": i, "value": i} for i in df["project_name"].unique()]


def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


@callback(
    Output("bmark_table", "children"),
    Input("multiselect_project", "value"),
    Input("benchmark_storage", "data"),
)
def update_bmark_table(value, data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df = df[
            [
                "project_name",
                "variation_name",
                "greenbook",
                "epic",
                "ice",
            ]
        ]
        df = df.rename(
            {"Project": "project_name", "Varaition": "variation_name"}, axis=1
        )
        if value is None or value == []:
            return create_table(df.head(10))
        else:
            return create_table(df[df["project_name"].isin(value)])


# This is for the refresh button to update the data
# and get the latest data from the firebase


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


# This part is purely for the benchmark graph ui.
# all interactions and ui elements related to the graph


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


def hline(
    fig,
    val,
    annot_text,
    annot_font_size,
    line_width,
    annot_pos="top right",
    line_color="gray",
):
    return fig.add_hline(
        y=val,
        line_dash="dash",
        annotation_text=annot_text,
        annotation_position=annot_pos,
        annotation_font_size=annot_font_size,
        line_width=line_width,
    )


def graph_lines(segment, fig, bmark):
    """add lines to the graph if segment == total. If not then do nothing

    Args:
        segment (__str__): dmc.segment data
        fig ( plotly graph): plotly graph.
        bmark (__str__): dmc.bmark data
    """
    if segment == "Total" and bmark == "all":

        hline(fig, 350, "LETI 2030 Design Targe Office**", 10, 1)
        hline(
            fig,
            300,
            "LETI 2030 Design Targe Residential, Education, & Retail**",
            # "bottom left",
            10,
            1,
        )
        hline(fig, 900, "Class 5 Office - Premium*", 10, 1)
        hline(fig, 600, "Class 5 Office - A Grade*", 10, 1)

    elif segment == "Total" and bmark == "ftp":
        hline(fig, 900, "Class 5 Office - Premium*", 10, 1)
        hline(fig, 600, "Class 5 Office - A Grade*", 10, 1)
        hline(fig, 590, "Class 2 Multi-Residential*", 10, 1, "bottom right")
    elif segment == "Total" and bmark == "leti":
        hline(fig, 350, "LETI 2030 Design Targe Office**", 10, 1)
        hline(
            fig,
            300,
            "LETI 2030 Design Targe Residential, Education, & Retail**",
            10,
            1,
        )

    else:
        pass


@callback(
    Output("gb-benchmark-graph", "figure"),
    Output("gb-benchmark-graph", "config"),
    Input("bmark_segment", "value"),
    Input("benchmark_storage", "data"),
    Input("segment_bmark", "value"),
    Input("config_id", "data"),
)
def update_gb_bmark(segment, data, bmark_segment, config):  # TODO: fix this
    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                name="Green Book",
                mode="markers",
                x=df["project_name"],
                y=df["{}greenbook".format(graphing.get(segment))],
                text=df["variation_name"],
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e/m²",
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
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e/m²",
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
                hovertemplate="<b>Project: %{x}</b><br>Variation: %{text}<br>%{y:,2f} kgCO2e/m²",
                marker=dict(
                    color="#52A9D1",
                    size=12,
                    symbol="cross",
                ),
            )
        )

        graph_lines(segment, fig, bmark_segment)

        fig.update_layout(
            title="Upfront Carbon Benchmark",
            xaxis_title="Projects",
            yaxis_title="kgCO2e",
        )
        return fig, config
