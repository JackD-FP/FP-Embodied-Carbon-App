# saving this because of the ^3 (m³)
import re
from collections import Counter

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# import numpy as np
import openpyxl  # just so excel upload works
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, ctx, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from config import config
from src import dashboard_cards, funcs, uploader

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

layout = html.Div(
    [
        html.H1("Dashboard", className="display-2 mb-5 "),
        html.Hr(),
        html.P(
            "The Embodied Carbon App is built to help architects and designers make informed in order to design a more sustainable building. \
        It is obvious to us that timber is far less carbon intense than concrete and steel. However, when it comes to actual buildings where mixtures of materials are necessary for structural stability, \
        the answer is less obvious. We should all strive to minimise our design's embodied carbon, however, not compromise with structural stability and design excellence.\
        The App can help identify which material is carbon intense and check if there are alternatives less carbon intense to the later. \
        It can also help identify what floor is causing the issue if a redesign or alteration is required.\
        This app free and open source for anyone. At Fitzpatrick and Partners, \
        we believe this is the way to help our industry move forward and achieve a better and sustainable tomorrow."
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                [
                    dbc.Button(
                        [
                            html.I(className="bi bi-upload", style={"width": "2rem"}),
                            html.P("Drag and Drop or Schedule File"),
                        ],
                        color="light",
                        className="align-center position-absolute top-50 start-50 translate-middle w-100 h-100",
                        id="upload_btn",
                    ),
                ],
                id="uploader_ui",
                style={"height": "10rem", "width": "50%", "margin": "auto"},
            ),
            style={
                "height": "10rem",
                "width": "50%",
                "lineHeight": "60px",
                "textAlign": "center",
                "margin": "auto",
                "marginTop": "2rem",
            },
            className="text-center mb-5 border border-2 rounded-3 shadow-sm bg-light",
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="error-display"),
        html.Div(id="display-table"),
        html.Div(
            id="dashboard_graph"
        ),  # could just check but idk ceebs not elegant(?)...no thing is elegant (╯▔皿▔)╯
    ]
)


@callback(
    Output("display-table", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            uploader.parse_contents(c, n, d, "temp-df-store", "name_1")
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)  # type: ignore
        ]
        return children


def layer_check(layer_list: list):
    for item in layer_list:
        if re.search(r"beam|slab|column|wall|stair", item, re.IGNORECASE):
            yield None
        else:
            yield item


def header_checker(dataColumn):
    for item in dataColumn:
        if re.search(r"Levels|Layer|Materials|Mass|Volume", item, re.IGNORECASE):
            yield None
        else:
            yield item


def error_handler(error_list: list) -> str:
    if not error_list:
        return "None"
    else:
        return ", ".join(error_list)


def data_check(df):
    correct_headers = ["Levels", "Layer", "Materials", "Mass", "Volume"]
    header_list = df.columns.tolist()

    layer_value = pd.unique(df["Layer"])
    layer_error = list(layer_check(list(layer_value)))
    res = list(filter(lambda item: item is not None, layer_error))
    if sorted(header_list) != sorted(correct_headers) or res:
        return True
    else:
        return False


@callback(
    Output("dashboard_graph", "children"),
    [
        Input("url", "pathname"),
        Input("beam_slider", "value"),
        Input("column_slider", "value"),
        Input("slab_slider", "value"),
        Input("wall_slider", "value"),
        Input("stair_slider", "value"),
        Input("main_store", "data"),
    ],
    #    prevent_initial_call=True,
)
def make_graphs(
    url, beam_slider, column_slider, slab_slider, wall_slider, stair_slider, data
):
    try:
        df = pd.read_json(data, orient="split")
    except:
        raise PreventUpdate

    if data_check(df):
        header_error = list(header_checker(df.columns.to_list()))
        layer_value = df.loc[:, "Layer"].values

        layer_error = list(layer_check(list(layer_value)))
        res_header = list(set(filter(lambda item: item is not None, header_error)))
        res_layer = list(set(filter(lambda item: item is not None, layer_error)))
        return dmc.Alert(
            title="SCHEDULE DATA ERROR",
            children=[
                dmc.Group(
                    children=[
                        "Check following headers for errors:",
                        dmc.Text(error_handler(res_header), weight=700, color="red"),
                    ],
                    direction="row",
                    spacing="md",
                ),
                dmc.Text(
                    "Column names should be: Levels, Layer, Materials, Mass, Volume",
                    size="sm",
                    color="gray",
                ),
                dmc.Space(h="md"),
                dmc.Group(
                    children=[
                        "Check following Layers for errors:",
                        dmc.Text(error_handler(res_layer), weight=700, color="red"),
                    ],
                    direction="row",
                    spacing="md",
                ),
                dmc.Text(
                    "Layer should contain at least: beam, slab, column, wall, stair",
                    size="sm",
                    color="gray",
                ),
            ],
            color="red",
        )

    elif url == "/pages/dashboard":
        df_ = pd.read_json(data, orient="split")
        df_o = df_.sort_values(by=["Levels"]).reset_index()

        mat, vol, mass, floor, element, gbec, epicec, iceec = funcs.mat_interpreter(
            df_o, beam_slider, column_slider, slab_slider, wall_slider, stair_slider
        )
        df_new = pd.DataFrame(
            {
                "Floor Level": floor,
                "Element": element,
                "Materials": mat,
                "Mass": mass,
                "Volume": vol,
                "Green Book EC": gbec,
                "EPiC EC": epicec,
                "ICE EC": iceec,
            }
        )
        # df_new.to_csv(".testing/df_new.csv")  # FIXME: for testing purposes

        colour_list = ["#064789", "#F8CC0D", "#FB3640", "#35A746"]

        gb_sum = df_new["Green Book EC"].sum()
        epic_sum = df_new["EPiC EC"].sum()
        ice_sum = df_new["ICE EC"].sum()

        df_new_grouped = df_new.groupby(
            by=["Element", "Materials"],
            as_index=False,
        ).sum()
        # there should be a better way to do this
        # TODO: make this one line or something
        df_new_grouped.loc[:, "Mass"] = df_new_grouped["Mass"].map("{:,.2f}".format)
        df_new_grouped.loc[:, "Volume"] = df_new_grouped["Volume"].map("{:,.2f}".format)
        df_new_grouped.loc[:, "Green Book EC"] = df_new_grouped["Green Book EC"].map(
            "{:,.2f}".format
        )
        df_new_grouped.loc[:, "EPiC EC"] = df_new_grouped["EPiC EC"].map(
            "{:,.2f}".format
        )
        df_new_grouped.loc[:, "ICE EC"] = df_new_grouped["ICE EC"].map("{:,.2f}".format)

        fig = make_subplots(
            rows=1,
            cols=3,
            specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
        )
        # subplot for greenbook
        fig.add_trace(
            go.Pie(
                labels=mat,
                values=gbec,
                # values=val_colour,
                name="Green Book DB",
                hole=0.5,
                scalegroup="dashboard_pie",
            ),
            1,
            1,
        )
        fig.add_trace(
            go.Pie(
                labels=mat,
                values=epicec,
                name="EPiC DB",
                hole=0.5,
                scalegroup="dashboard_pie",
            ),
            1,
            2,
        )
        # subplot for greenbookW
        fig.add_trace(
            go.Pie(
                labels=mat,
                values=iceec,
                name="ICE DB",
                hole=0.5,
                scalegroup="dashboard_pie",
            ),
            1,
            3,
        )
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            annotations=[
                dict(text="Greenbook", x=0.12, y=0.50, font_size=16, showarrow=False),
                dict(
                    text="{:,.2f} kgCO₂e".format(gb_sum),
                    x=0.1,
                    y=0.45,
                    font_size=12,
                    showarrow=False,
                ),
                dict(text="EPiC", x=0.50, y=0.50, font_size=16, showarrow=False),
                dict(
                    text="{:,.2f} kgCO₂e".format(epic_sum),
                    x=0.5,
                    y=0.45,
                    font_size=12,
                    showarrow=False,
                ),
                dict(text="ICE", x=0.87, y=0.50, font_size=16, showarrow=False),
                dict(
                    text="{:,.2f} kgCO₂e".format(ice_sum),
                    x=0.90,
                    y=0.45,
                    font_size=12,
                    showarrow=False,
                ),
            ],
        ),  # type: ignore
        fig.update_traces(
            hoverinfo="label+value",
            textinfo="percent",
        )
        # drop embodied carbon if it exist
        if "Embodied Carbon" in df.columns:
            df = df.drop(["Embodied Carbon"], axis=1)
        else:
            pass

        return html.Div(
            [  # consolidated table..
                dcc.Store(id="temp_proc_store", data=df_new.to_json(orient="split")),
                html.H3(
                    [
                        "Uploaded File: ",
                        html.Span(id="file_name", className="display-5"),
                    ],
                    className="my-3",
                ),
                html.P(
                    "Review your uploaded file with the table below. See if there are any errors or missing data.",
                    className="my-3",
                ),
                # html.Div(id="error_check"),
                dash_table.DataTable(
                    df_o.to_dict("records"),
                    [{"name": i, "id": i} for i in df_o.columns],
                    page_size=15,
                    style_data_conditional=(
                        [
                            {
                                "if": {
                                    "filter_query": "{{{}}} is blank".format(col),
                                    "column_id": col,
                                },
                                "backgroundColor": "rgb(254,111,94)",
                            }
                            for col in df_o.columns
                        ]
                    ),
                    style_header={"fontWeight": "bold"},
                ),
                dbc.Card(
                    [
                        html.H3("Embodied Carbon (EC) calculation"),
                        dmc.Table(
                            funcs.create_table(df_new_grouped),
                            highlightOnHover=True,
                        ),
                        dashboard_cards.cards,
                        dcc.Graph(
                            figure=fig,
                            style={"height": "50vh"},
                            className="mt-3",
                            config=config,
                        ),
                    ],
                    class_name="my-5 shadow",
                    style={"padding": "4rem"},
                ),
            ]
        )


@callback(
    Output("file_name", "children"),
    Input("project_name", "data"),
)
def filename_update(data):
    return data


# ----- check for errors in the uploaded file -----


# def header_check(df):
#     # check if the header is correct
#     for col in df.columns:
#         if col in ["Levels", "Layer", "Materials", "Mass", "Volume"]:
#             return False, None
#         else:
#             return True, col


def material_check(df):
    # check if the materials are in the database
    error_index = []
    for i, mat in enumerate(df["Materials"].items()):
        if re.search(
            r"(concrete)|(conc)|(steel)|(Reinforcement Bar)|(rebar)|(reo)|(timber)",
            str(mat),
            re.IGNORECASE,
        ):
            error_index.append(i)
    if len(error_index) > 0:
        return False, None
    else:
        return True, error_index
