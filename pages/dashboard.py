# saving this because of the ^3 (m³)
import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import openpyxl  # just so excel upload works
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import config
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from src import dashboard_cards, funcs, uploader

layout = html.Div(
    [
        html.H1("Dashboard", className="display-2 mb-5 "),
        html.Hr(),
        html.P(
            "The Embodied Carbon App is built to help architects and designers make informed in order to design a more sustainable building. \
        It is obvious to us that timber is far less carbon intense than concrete and steel. However, when it comes to actual buildings where mixtures of Material are necessary for structural stability, \
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
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


def percent_check_return(lo, hi):
    if hi == lo:
        return "Lowest total EC"
    else:
        sub = (hi - lo) * 100
        return "+{}% more than lowest".format(np.around(sub / hi, 2))


@callback(
    Output("dashboard_graph", "children"),
    [
        Input("main_store", "data"),
        Input("beam_slider", "value"),
        Input("column_slider", "value"),
        Input("slab_slider", "value"),
        Input("wall_slider", "value"),
        Input("stair_slider", "value"),
    ],
)
def make_graphs(
    data, beam_slider, column_slider, slab_slider, wall_slider, stair_slider
):
    if data is None:
        raise PreventUpdate
    elif data is not None:
        df_ = pd.read_json(data, orient="split")
        df_o = df_.reset_index()
        # df_.to_excel("temp-df-store.xlsx") # just for testing
        df = df_.groupby(by=["Material"], as_index=False).sum()

        # new calculations for carbon intensity
        mat, vol, mass, floor, element, epicec, iceec = funcs.mat_interpreter(
            df_, beam_slider, column_slider, slab_slider, wall_slider, stair_slider
        )
        df_new = pd.DataFrame(
            {
                "Floor Level": floor,
                "Element": element,
                "Material": mat,
                "Mass": mass,
                "Volume": vol,
                "EPiC EC": epicec,
                "ICE EC": iceec,
            }
        )
        # df_new.to_csv(".testing/df_new.csv")  # FIXME: for testing purposes

        colour_list = ["#064789", "#F8CC0D", "#FB3640", "#35A746"]

        epic_sum = df_new["EPiC EC"].sum()
        ice_sum = df_new["ICE EC"].sum()

        df_new_grouped = df_new.groupby(
            by=["Element", "Material"],
            as_index=False,
        ).sum()
        # there should be a better way to do this
        # TODO: make this one line or something
        df_new_grouped.loc[:, "Mass"] = df_new_grouped["Mass"].map("{:,.2f}".format)
        df_new_grouped.loc[:, "Volume"] = df_new_grouped["Volume"].map("{:,.2f}".format)
        df_new_grouped.loc[:, "EPiC EC"] = df_new_grouped["EPiC EC"].map(
            "{:,.2f}".format
        )
        df_new_grouped.loc[:, "ICE EC"] = df_new_grouped["ICE EC"].map("{:,.2f}".format)

        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "pie"}, {"type": "pie"}]],
        )
        # subplot for epic
        fig.add_trace(
            go.Pie(
                labels=mat,
                values=epicec,
                name="EPiC DB",
                hole=0.5,
                scalegroup="dashboard_pie",
            ),
            1,
            1,
        )
        # subplot for ice
        fig.add_trace(
            go.Pie(
                labels=mat,
                values=iceec,
                name="ICE DB",
                hole=0.5,
                scalegroup="dashboard_pie",
            ),
            1,
            2,
        )
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            annotations=[
                dict(text="EPiC", x=0.22, y=0.50, font_size=16, showarrow=False),
                dict(
                    text="{:,.2f} kgCO₂e".format(epic_sum),
                    x=0.18,
                    y=0.45,
                    font_size=12,
                    showarrow=False,
                ),
                dict(text="ICE", x=0.79, y=0.50, font_size=16, showarrow=False),
                dict(
                    text="{:,.2f} kgCO₂e".format(ice_sum),
                    x=0.82,
                    y=0.45,
                    font_size=12,
                    showarrow=False,
                ),
            ],
        ),
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
                html.Div(id="error_check"),
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
