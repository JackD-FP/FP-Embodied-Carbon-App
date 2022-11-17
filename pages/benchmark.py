import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html

from src.firebase_init import bucket, db

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
        html.Div(id="bmark_test"),
        dcc.Store(id="temp-bmark", storage_type="session"),
    ]
)


@callback(
    Output("temp-bmark", "data"),
    Input("bmark_segment", "data"),
    # prevent_initial_call=True,
)
def update_benchmark_graphs(loading_state):
    # if loading_state is True:
    #     raise dash.exceptions.PreventUpdate
    # else:
    docs = db.collection("projects").stream()
    project_name = []
    var_name = []
    gb = []
    epic = []
    ice = []
    date = []
    # gb_sub = []
    # epic_sub = []
    # ice_sub = []
    # gb_super = []
    # epic_super = []
    # ice_super = []
    for doc in docs:
        data = doc.to_dict()

        project_name.append(data["project_name"])
        var_name.append(data["variation_name"])
        date.append(data["datetime"])
        gb.append(data["greenbook"])
        epic.append(data["epic"])
        ice.append(data["ice"])
        # TODO: add sub and superstructure

    d = {
        "project_name": project_name,
        "variation_name": var_name,
        "gb": gb,
        "epic": epic,
        "ice": ice,
        "date": date,
    }
    df = pd.DataFrame(d)
    return df.to_json(orient="split")


def scatter_plot(df, db: str, desc: str):
    px.scatter(
        df,
        x="date",
        y=db,
        color="project_name",
        title=desc,
        # labels={"gb": "Greenbook"},
    )


def total(df):
    return (
        scatter_plot(df, "gb", "Greenbook Benchmark"),
        scatter_plot(df, "epic", "EPiC Benchmark"),
        scatter_plot(df, "ice", "ICE Benchmark"),
    )


def superstructure(df):
    pass
    # return (
    #     scatter_plot(df, "gb", "Greenbook Benchmark"),
    #     scatter_plot(df, "epic", "EPiC Benchmark"),
    #     scatter_plot(df, "ice", "ICE Benchmark"),
    # )


def substructure(df):
    pass
    # return (
    #     scatter_plot(df, "gb", "Greenbook Benchmark"),
    #     scatter_plot(df, "epic", "EPiC Benchmark"),
    #     scatter_plot(df, "ice", "ICE Benchmark"),
    # )


graphing = {
    "Total": total,
    "Superstructure": superstructure,
    "Substructure": substructure,
}


@callback(
    Output("gb-benchmark-graph", "figure"),
    Input("bmark_segment", "value"),
    State("temp-bmark", "data"),
)
def update_gb_bmark(data, value):

    if data is None:
        raise dash.exceptions.PreventUpdate
    else:
        print(value)
        df = pd.read_json(data, orient="split")

        return graphing[value](df)[0]
