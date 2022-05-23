import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html, State
from dash.exceptions import PreventUpdate
from src import greenbook_options

gb_layout = [
    dbc.Card(
        [
            dcc.Store(id="gb_store"),
            html.H3("Green Book DB"),
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
                                                id="gb_analysis_total",
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
                                                id="gb_analysis_benchmark",
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
                                id="gb_tabs",
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
                            html.Div(id="gb_tab_content"),
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


def row(options):
    table_head = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Materials"),
                    html.Th("Embodied Carbon"),
                ]
            )
        )
    ]
    row = html.Tr(
        [
            html.Td(
                dbc.Row(
                    [
                        dbc.Col(children=dmc.Text("Concrete")),
                        dbc.Col(children=options),
                    ]
                )
            ),
            html.Td(1234567890),
        ]
    )
    return dbc.Table(html.Tbody(table_head + [row]))


# rows = [
#     row(dbc.Select(greenbook_options.concrete, persistence=True)),
#     row(dbc.Select(greenbook_options.rebar, persistence=True)),
# ]

# ---- This updates the total and benchmark values on the analysis card ----
@callback(
    Output("gb_analysis_total", "children"),
    Output("gb_analysis_benchmark", "children"),
    Input("gb_store", "modified_timestamp"),
    Input("nla_store", "modified_timestamp"),
    State("gb_store", "data"),
    State("nla_store", "data"),
)
def update_total_benchmark(mts, mts_nla, gb_data, nla):
    if mts is None or mts_nla is None:
        raise PreventUpdate
    else:
        df = pd.read_json(gb_data, orient="split")
        total = df["Green Book EC"].sum()
        benchmark = total / nla
        return "{:,}".format(np.around(total, 2)), "{:,}".format(
            np.around(benchmark, 2)
        )


@callback(
    Output("gb_store", "data"),
    Output("gb_tab_content", "children"),
    Input("gb_tabs", "active_tab"),
    State("proc_store", "data"),
)
def update_layout(tabs, data):
    if data is None:
        raise PreventUpdate
    else:
        # df = pd.read_json(data, orient="split")

        # row_concrete = html.Tr(
        #     [
        #         html.Td(
        #             dbc.Row(
        #                 [
        #                     dbc.Col([dmc.Text("Concrete")]),
        #                     dbc.Col(dbc.Select(greenbook_options.concrete)),
        #                 ]
        #             )
        #         ),
        #         html.Td(1234567890),
        #     ]
        # )

        # beams = dbc.Table(html.Tbody(table_head + [row_concrete]))
        # content = {
        #     "Beams": row(dbc.Select(greenbook_options.concrete)),
        #     "Columns": html.P("asdf"),
        #     "Slabs": html.P("zxcv"),
        #     "Walls": html.P("qwerqwe"),
        #     "Stairs": html.P("tyuityui"),
        # }

        # return data, content.get(tabs, "Error")

        # return content.get(tab)

        if tabs == "Beams":
            return data, row(dbc.Select(options=greenbook_options.concrete))
