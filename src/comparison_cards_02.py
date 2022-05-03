import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config import graph_colors
from dash import Input, Output, State, callback, dcc, html
import plotly.express as px

from src import (
    epic_options,
    funcs,
    greenbook_options,
    ice_options,
    material_table,
    uploader,
)


card02 = html.Div(
    [
        dcc.Upload(
            id="card2_upload_data",
            children=html.Div(
                [
                    dmc.Tooltip(
                        label="Upload Comparison",
                        transition="fade",
                        transitionDuration=300,
                        transitionTimingFunction="ease",
                        children=[
                            dmc.Button(
                                html.I(className="bi bi-cloud-upload"),
                                radius="xl",
                                size="md",
                                class_name="shadow-sm",
                            )
                        ],
                    )
                ]
            ),
            className="position-absolute translate-middle",
            style={"zIndex": "5", "left": "98%", "top": "0%"},
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="card2_output"),
        html.Div(id="card2_contents"),
    ]
)


@callback(
    Output("card2_output", "children"),
    Input("card2_upload_data", "contents"),
    State("card2_upload_data", "filename"),
    State("card2_upload_data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            uploader.parse_contents(c, n, d, "card2_temp_store", "name_2")
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


@callback(
    Output("card2_contents", "children"),
    Input("card02_store", "modified_timestamp"),
    State("card02_store", "data"),
)
def card2_content_update(
    mts,
    data,
):
    if data is None or mts is None:
        return html.P(
            "Upload another project to compare with!",
            className="display-6 text-center fs-4",
        )
    else:
        df = pd.read_json(data, orient="split")
        mat, vol, mass, floor, layer, gb_ec, epic_ec, ice_ec = funcs.mat_interpreter(df)
        df_calc = pd.DataFrame(
            {
                "materials": mat,
                "volume": vol,
                "mass": mass,
            }
        )
        _df = df_calc.groupby(by=["materials"], as_index=False).sum()
        tmp = _df.select_dtypes(include=["float64"])
        _df.loc[:, tmp.columns] = np.around(tmp, 2)

        return html.Div(
            [
                html.H3("Comparison 2", className="display-5 my-3"),
                dmc.Divider(class_name="mb-3"),
                html.H3("Structure Schedule"),
                dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
                html.H5(["GFA in m", html.Sup(2)]),
                # input for gfa calculation
                dbc.Input(
                    id="comp_card2_gfa",
                    # placeholder="GFA?",
                    value=5000,
                    className="w-25",
                    type="number",
                    debounce=True,
                    persistence=True,
                    persistence_type="session",
                    required=True,
                ),
                dmc.Divider(class_name="my-3"),
                # ----------- Green book comparison for CARD 2 ----------
                html.H3("Green Book DB", className="mb-3"),
                dmc.Accordion(
                    [
                        dmc.AccordionItem(
                            material_table.table_gen(
                                dbc.Select(
                                    options=greenbook_options.concrete,
                                    id="gb_card2_concrete",
                                    value=643,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="gb_card2_concrete_val"),
                                dbc.Select(
                                    options=greenbook_options.rebar,
                                    id="gb_card2_rebar",
                                    value=2.900,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="gb_card2_rebar_val"),
                                dbc.Select(
                                    options=greenbook_options.steel,
                                    id="gb_card2_steel",
                                    value=2.61,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="gb_card2_steel_val"),
                                dbc.Select(
                                    options=greenbook_options.timber,
                                    id="gb_card2_timber",
                                    value=718,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="gb_card2_timber_val"),
                            ),
                            label="Green Book DB Material Options ▼",
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(id="gb_card2_total", className="text-center"),
                                html.P(
                                    [
                                        html.Span(
                                            ["kgCO", html.Sup(2), html.Sub("e")],
                                            className="fs-4",
                                        ),
                                        " Total EC",
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(id="gb_card2_gfa", className="text-center"),
                                html.P(
                                    [
                                        html.Span(
                                            [
                                                "kgCO",
                                                html.Sup(2),
                                                html.Sub("e"),
                                                "/m",
                                                html.Sup(2),
                                            ],
                                            className="fs-4",
                                        ),
                                        " EC per m",
                                        html.Sup(2),
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                    ],
                    className="my-5",
                ),
                html.Div(id="card2_gb_pie"),
                dmc.Divider(class_name="my-3"),
                # ----------- EPiC comparison for CARD 2 ----------
                html.H3("EPiC DB", className="mb-3"),
                dmc.Accordion(
                    [
                        dmc.AccordionItem(
                            material_table.table_gen(
                                dbc.Select(
                                    options=epic_options.concrete,
                                    id="epic_card2_concrete",
                                    value=600,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="epic_card2_concrete_val"),
                                dbc.Select(
                                    options=epic_options.rebar,
                                    id="epic_card2_rebar",
                                    value=2.9,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="epic_card2_rebar_val"),
                                dbc.Select(
                                    options=epic_options.steel,
                                    id="epic_card2_steel",
                                    value=2.9,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="epic_card2_steel_val"),
                                dbc.Select(
                                    options=epic_options.timber,
                                    id="epic_card2_timber",
                                    value=1718,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="epic_card2_timber_val"),
                            ),
                            label="EPiC DB Material Options ▼",
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    id="epic_card2_total", className="text-center"
                                ),
                                html.P(
                                    [
                                        html.Span(
                                            ["kgCO", html.Sup(2), html.Sub("e")],
                                            className="fs-4",
                                        ),
                                        " Total EC",
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(id="epic_card2_gfa", className="text-center"),
                                html.P(
                                    [
                                        html.Span(
                                            [
                                                "kgCO",
                                                html.Sup(2),
                                                html.Sub("e"),
                                                "/m",
                                                html.Sup(2),
                                            ],
                                            className="fs-4",
                                        ),
                                        " EC per m",
                                        html.Sup(2),
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                    ],
                    className="my-5",
                ),
                html.Div(id="card2_epic_pie"),
                dmc.Divider(class_name="my-3"),
                # ----------- ICE comparison for CARD 2 ----------
                html.H3("ICE DB", className="mb-3"),
                dmc.Accordion(
                    [
                        dmc.AccordionItem(
                            material_table.table_gen(
                                dbc.Select(
                                    options=ice_options.concrete,
                                    id="ice_card2_concrete",
                                    value=413.4943,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="ice_card2_concrete_val"),
                                dbc.Select(
                                    options=ice_options.rebar,
                                    id="ice_card2_rebar",
                                    value=1.99,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="ice_card2_rebar_val"),
                                dbc.Select(
                                    options=ice_options.steel,
                                    id="ice_card2_steel",
                                    value=1.55,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="ice_card2_steel_val"),
                                dbc.Select(
                                    options=ice_options.timber,
                                    id="ice_card2_timber",
                                    value=0.51,
                                    persistence=True,
                                    persistence_type="session",
                                ),
                                html.Div(id="ice_card2_timber_val"),
                            ),
                            label="ICE DB Material Options ▼",
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(id="ice_card2_total", className="text-center"),
                                html.P(
                                    [
                                        html.Span(
                                            ["kgCO", html.Sup(2), html.Sub("e")],
                                            className="fs-4",
                                        ),
                                        " Total EC",
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(id="ice_card2_gfa", className="text-center"),
                                html.P(
                                    [
                                        html.Span(
                                            [
                                                "kgCO",
                                                html.Sup(2),
                                                html.Sub("e"),
                                                "/m",
                                                html.Sup(2),
                                            ],
                                            className="fs-4",
                                        ),
                                        " EC per m",
                                        html.Sup(2),
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                    ],
                    className="my-4",
                ),
                html.Div(id="card2_ice_pie"),
            ]
        )  # END OF CARD 2 LIST DON'T DELETE


# ----------------------------- callbacks -----------------------------

# Green Book callback
@callback(
    Output("gb_card2_total", "children"),
    Output("gb_card2_gfa", "children"),
    Output("gb_card2_concrete_val", "children"),
    Output("gb_card2_rebar_val", "children"),
    Output("gb_card2_steel_val", "children"),
    Output("gb_card2_timber_val", "children"),
    Output("card2_gb_pie", "children"),
    Input("comp_card2_gfa", "value"),
    Input("gb_card2_concrete", "value"),
    Input("gb_card2_rebar", "value"),
    Input("gb_card2_steel", "value"),
    Input("gb_card2_timber", "value"),
    State("card02_store", "data"),
)
def card2_total_gfa_update(gfa, conc_val, rebar_val, steel_val, timber_val, data):
    return card2_layout(
        gfa, conc_val, rebar_val, steel_val, timber_val, data, is_ice=False
    )


# # Epic callback
@callback(
    Output("epic_card2_total", "children"),
    Output("epic_card2_gfa", "children"),
    Output("epic_card2_concrete_val", "children"),
    Output("epic_card2_rebar_val", "children"),
    Output("epic_card2_steel_val", "children"),
    Output("epic_card2_timber_val", "children"),
    Output("card2_epic_pie", "children"),
    Input("comp_card2_gfa", "value"),
    Input("epic_card2_concrete", "value"),
    Input("epic_card2_rebar", "value"),
    Input("epic_card2_steel", "value"),
    Input("epic_card2_timber", "value"),
    State("card02_store", "data"),
)
def card2_total_gfa_update(gfa, conc_val, rebar_val, steel_val, timber_val, data):
    return card2_layout(
        gfa, conc_val, rebar_val, steel_val, timber_val, data, is_ice=False
    )


# ice callback
@callback(
    Output("ice_card2_total", "children"),
    Output("ice_card2_gfa", "children"),
    Output("ice_card2_concrete_val", "children"),
    Output("ice_card2_rebar_val", "children"),
    Output("ice_card2_steel_val", "children"),
    Output("ice_card2_timber_val", "children"),
    Output("card2_ice_pie", "children"),
    Input("comp_card2_gfa", "value"),
    Input("ice_card2_concrete", "value"),
    Input("ice_card2_rebar", "value"),
    Input("ice_card2_steel", "value"),
    Input("ice_card2_timber", "value"),
    State("card02_store", "data"),
)
def card2_total_gfa_update(gfa, conc_val, rebar_val, steel_val, timber_val, data):
    return card2_layout(
        gfa, conc_val, rebar_val, steel_val, timber_val, data, is_ice=True
    )


def card2_layout(gfa, conc_val, rebar_val, steel_val, timber_val, data, is_ice=False):
    if gfa is None:
        unknown_total_gfa = html.H3(["Unknown", html.P("Input GFA above")])
        unknown = html.P("Unknown")
        return (
            unknown_total_gfa,
            unknown_total_gfa,
            unknown,
            unknown,
            unknown,
            unknown,
            unknown,
        )
    else:
        df = pd.read_json(data, orient="split")
        mat, vol, mass, floor, layer, ec = funcs.ec_calculator(
            df,
            float(conc_val),
            float(rebar_val),
            float(timber_val),
            float(steel_val),
            if_ice=is_ice,
        )

        df_calc = pd.DataFrame(
            {
                "materials": mat,
                "volume": vol,
                "mass": mass,
                "floor": floor,
                "layer": layer,
                "ec": ec,
            }
        )

        df_grouped = df_calc.groupby(by=["materials"], as_index=False).sum()

        total = html.Div(
            [
                html.H3("{:,.2f}".format(df_grouped["ec"].sum())),
            ],
            style={"display": "block"},
        )

        gfa_calc = html.Div(
            [
                html.H3(["{:,.2f}".format(np.around(sum(ec) / gfa, 2))]),
            ],
            style={"display": "block"},
        )

        # fig = go.Figure(
        #     data=[go.Pie(labels=df_calc["materials"], values=df_calc["ec"], hole=0.5)]
        # )
        # fig.update_layout(
        #     title_text="Structure Embodied Carbon",
        #     annotations=[
        #         dict(text="Green Book", x=0.5, y=0.5, font_size=16, showarrow=False)
        #     ],
        # )
        # fig.update_traces(
        #     hoverinfo="label+percent+value",
        #     textinfo="percent",
        #     marker=dict(
        #         colors=graph_colors,
        #     ),
        # )
        fig = px.pie(
            df_calc,
            values=df_calc["ec"],
            names=df_calc["materials"],
            color=df_calc["materials"],
            hole=0.5,
            color_discrete_map={
                "Concrete": "#5463ff",
                "Reinforcement Bar": "#ffc300",
                "STEEL - STRUCTURAL": "#79b159",
                "TIMBER - STRUCTURAL": "#74d7f7",
            },
        )

        return (
            total,
            gfa_calc,
            html.P(
                "{:,.2f}".format(
                    funcs.none_check(
                        df_grouped.loc[
                            df_grouped["materials"] == "Concrete", "ec"
                        ]  # .values[0]
                    )
                ),
                className="text-center",
            ),
            html.P(
                "{:,.2f}".format(
                    funcs.none_check(
                        df_grouped.loc[
                            df_grouped["materials"] == "Reinforcement Bar", "ec"
                        ]  # .values[0]
                    )
                ),
                className="text-center",
            ),
            html.P(
                "{:,.2f}".format(
                    funcs.none_check(
                        df_grouped.loc[
                            df_grouped["materials"] == "STEEL - STRUCTURAL", "ec"
                        ]  # .values[0]
                    )
                ),
                className="text-center",
            ),
            html.P(
                "{:,.2f}".format(
                    funcs.none_check(
                        df_grouped.loc[
                            df_grouped["materials"] == "TIMBER - STRUCTURAL", "ec"
                        ]  # .values[0]
                    )
                ),
                className="text-center",
            ),
            dcc.Graph(figure=fig),
        )
