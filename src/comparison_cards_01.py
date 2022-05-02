# This generates cards for the comparison page
#   - cards: cards01, cards02, cards03
#   - each cards has the ability to generate analysis from greenbook, epic and ice

import re
from operator import index

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config import graph_colors
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from src import epic_options, funcs, greenbook_options, ice_options, material_table

card01 = html.Div([html.Div(id="card01_table")])


@callback(
    Output("card01_table", "children"),
    Input("gfa_store", "modified_timestamp"),
    State("main_store", "data"),
    State("gfa_store", "data"),
)
def update_div(gfa_mts, main_data, gfa_data):
    if main_data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(main_data, orient="split")

        mat, vol, mass, floor, layer, gb_ec, epic_ec, ice_ec = funcs.mat_interpreter(df)
        df_calc = pd.DataFrame(
            {
                "materials": mat,
                "volume": vol,
                "mass": mass,
                "floor": floor,
                "layer": layer,
                "ec": gb_ec,
            }
        )
        _df = df_calc.groupby(by=["materials"], as_index=False).sum()

        # rounds the values to 2 decimal places
        tmp = _df.select_dtypes(include=["float64"])
        _df.loc[:, tmp.columns] = np.around(tmp, 2)
        _df = _df.filter(items=["materials", "mass", "volume"])

        if gfa_mts is None or gfa_mts == "":
            gfa = 0
        else:
            gfa = gfa_data

        table_out = [
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
            html.H5(["GFA in m", html.Sup(2)]),
            dbc.Input(
                id="comp_card01_gfa",
                placeholder="What's the project Name?",
                value=gfa,
                className="w-25",
                type="text",
                debounce=True,
                persistence=True,
                persistence_type="session",
                required=True,
            ),
            dmc.Divider(class_name="my-3"),
            # ----------- green book comparison for card 01 -----------
            html.H3("Green Book DB", className="mb-3"),
            dmc.Accordion(
                [
                    dmc.AccordionItem(
                        material_table.table_gen(
                            dbc.Select(
                                options=greenbook_options.concrete,
                                id="gb_comp_concrete",
                                value=643,
                            ),
                            html.P(id="gb_comp_concrete_val"),
                            dbc.Select(
                                options=greenbook_options.rebar,
                                id="gb_comp_rebar",
                                value=2.9,
                            ),
                            html.P(id="gb_comp_rebar_val"),
                            dbc.Select(
                                options=greenbook_options.steel,
                                id="gb_comp_steel",
                                value=2.61,
                            ),
                            html.P(id="gb_comp_steel_val"),
                            dbc.Select(
                                options=greenbook_options.timber,
                                id="gb_comp_timber",
                                value=718,
                            ),
                            html.P(id="gb_comp_timber_val"),
                        ),
                        label="Green Book DB Material Options ▼",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3(id="gb_comp_total", className="text-center"),
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
                            html.H3(id="gb_comp_gfa", className="text-center"),
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
                class_name="my-5",
            ),
            html.Div(id="gb_pie"),
            html.Div(
                id="gb_bars"
            ),  # there is provision for bar graphs but will add that later
            dmc.Divider(class_name="my-3"),
            # ---------- EPIC comparison for card 01 -----------
            html.H3("EPiC DB", className="mb-3"),
            dmc.Accordion(
                [
                    dmc.AccordionItem(
                        material_table.table_gen(
                            dbc.Select(
                                options=epic_options.concrete,
                                id="epic_comp_concrete",
                                value=600,
                            ),
                            html.P(id="epic_comp_concrete_val"),
                            dbc.Select(
                                options=epic_options.rebar,
                                id="epic_comp_rebar",
                                value=2.9,
                            ),
                            html.P(id="epic_comp_rebar_val"),
                            dbc.Select(
                                options=epic_options.steel,
                                id="epic_comp_steel",
                                value=2.9,
                            ),
                            html.P(id="epic_comp_steel_val"),
                            dbc.Select(
                                options=epic_options.timber,
                                id="epic_comp_timber",
                                value=1718,
                            ),
                            html.P(id="epic_comp_timber_val"),
                        ),
                        label="EPiC DB Material Options ▼",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3(id="epic_comp_total", className="text-center"),
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
                            html.H3(id="epic_comp_gfa", className="text-center"),
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
                class_name="my-5",
            ),
            html.Div(id="epic_pie"),
            dmc.Divider(class_name="my-3"),
            # ---------- Ice comparison for card 01 -----------
            html.H3("ICE DB", className="mb-3"),
            dmc.Accordion(
                [
                    dmc.AccordionItem(
                        material_table.table_gen(
                            dbc.Select(
                                options=ice_options.concrete,
                                id="ice_comp_concrete",
                                value=413.4943,
                            ),
                            html.P(id="ice_comp_concrete_val"),
                            dbc.Select(
                                options=ice_options.rebar,
                                id="ice_comp_rebar",
                                value=1.99,
                            ),
                            html.P(id="ice_comp_rebar_val"),
                            dbc.Select(
                                options=ice_options.steel,
                                id="ice_comp_steel",
                                value=1.55,
                            ),
                            html.P(id="ice_comp_steel_val"),
                            dbc.Select(
                                options=ice_options.timber,
                                id="ice_comp_timber",
                                value=0.51,
                            ),
                            html.P(id="ice_comp_timber_val"),
                        ),
                        label="ICE DB Material Options ▼",
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3(id="ice_comp_total", className="text-center"),
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
                            html.H3(id="ice_comp_gfa", className="text-center"),
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
                class_name="my-4",
            ),
            html.Div(id="ice_pie"),
        ]
        return table_out


#
#     @TODO: refactor the code below to be one callback function
#     There is a lot of repetition in these callbacks. There is a possibility to refactor this into a callback.

# ---------------- GREENBOOK CALLBACK ----------------
@callback(
    Output("gb_comp_concrete_val", "children"),
    Output("gb_comp_rebar_val", "children"),
    Output("gb_comp_steel_val", "children"),
    Output("gb_comp_timber_val", "children"),
    Output("gb_comp_total", "children"),
    Output("gb_comp_gfa", "children"),
    Output("gb_pie", "children"),
    Input("gb_comp_concrete", "value"),
    Input("gb_comp_rebar", "value"),
    Input("gb_comp_steel", "value"),
    Input("gb_comp_timber", "value"),
    Input("comp_card01_gfa", "value"),
    State("main_store", "data"),
)
def definition(conc_val, rebar_val, steel_val, timber_val, gfa, data):
    if data is None:
        raise PreventUpdate
    else:
        if gfa is None:
            raise PreventUpdate
        else:
            df = pd.read_json(data, orient="split")
            mat, vol, mass, floor, layer, ec = funcs.ec_calculator(
                df,
                float(conc_val),
                float(rebar_val),
                float(timber_val),
                float(steel_val),
                if_ice=False,
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

            fig = go.Figure(
                data=[
                    go.Pie(labels=df_calc["materials"], values=df_calc["ec"], hole=0.5)
                ]
            )
            fig.update_layout(
                title_text="Structure Embodied Carbon",
                annotations=[
                    dict(text="Green Book", x=0.5, y=0.5, font_size=16, showarrow=False)
                ],
            )
            fig.update_traces(
                hoverinfo="label+percent+value",
                textinfo="percent",
                marker=dict(
                    colors=graph_colors,
                ),
            )

            return (
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "Concrete", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "Reinforcement Bar", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "STEEL - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "TIMBER - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                total,
                gfa_calc,
                dcc.Graph(figure=fig),
            )


# ---------------- EPIC CALLBACK ----------------
@callback(
    Output("epic_comp_concrete_val", "children"),
    Output("epic_comp_rebar_val", "children"),
    Output("epic_comp_steel_val", "children"),
    Output("epic_comp_timber_val", "children"),
    Output("epic_comp_total", "children"),
    Output("epic_comp_gfa", "children"),
    Output("epic_pie", "children"),
    Input("epic_comp_concrete", "value"),
    Input("epic_comp_rebar", "value"),
    Input("epic_comp_steel", "value"),
    Input("epic_comp_timber", "value"),
    Input("comp_card01_gfa", "value"),
    State("main_store", "data"),
)
def definition(conc_val, rebar_val, steel_val, timber_val, gfa, data):
    if data is None:
        raise PreventUpdate
    else:
        if gfa is None:
            raise PreventUpdate
        else:
            df = pd.read_json(data, orient="split")
            mat, vol, mass, floor, layer, ec = funcs.ec_calculator(
                df,
                float(conc_val),
                float(rebar_val),
                float(timber_val),
                float(steel_val),
                if_ice=False,
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

            fig = go.Figure(
                data=[
                    go.Pie(labels=df_calc["materials"], values=df_calc["ec"], hole=0.5)
                ]
            )
            fig.update_layout(
                title_text="Structure Embodied Carbon",
                annotations=[
                    dict(text="EPiC DB", x=0.5, y=0.5, font_size=16, showarrow=False)
                ],
            )
            fig.update_traces(
                hoverinfo="label+percent+value",
                textinfo="percent",
                marker=dict(
                    colors=graph_colors,
                ),
            )

            return (
                html.P(
                    "{:,.2f}".format(
                        funcs.none_check(
                            df_grouped.loc[
                                df_grouped["materials"] == "Concrete", "ec"
                            ].values[0]
                        )
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "Reinforcement Bar", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "STEEL - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "TIMBER - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                total,
                gfa_calc,
                dcc.Graph(figure=fig),
            )


# ---------------- ICE CALLBACK ----------------
@callback(
    Output("ice_comp_concrete_val", "children"),
    Output("ice_comp_rebar_val", "children"),
    Output("ice_comp_steel_val", "children"),
    Output("ice_comp_timber_val", "children"),
    Output("ice_comp_total", "children"),
    Output("ice_comp_gfa", "children"),
    Output("ice_pie", "children"),
    Input("ice_comp_concrete", "value"),
    Input("ice_comp_rebar", "value"),
    Input("ice_comp_steel", "value"),
    Input("ice_comp_timber", "value"),
    Input("comp_card01_gfa", "value"),
    State("main_store", "data"),
)
def definition(conc_val, rebar_val, steel_val, timber_val, gfa, data):
    if data is None:
        raise PreventUpdate
    else:
        if gfa is None:
            raise PreventUpdate
        else:
            df = pd.read_json(data, orient="split")
            mat, vol, mass, floor, layer, ec = funcs.ec_calculator(
                df,
                float(conc_val),
                float(rebar_val),
                float(timber_val),
                float(steel_val),
                if_ice=True,
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

            fig = go.Figure(
                data=[
                    go.Pie(labels=df_calc["materials"], values=df_calc["ec"], hole=0.5)
                ]
            )
            fig.update_layout(
                title_text="Structure Embodied Carbon",
                annotations=[
                    dict(text="ICE DB", x=0.5, y=0.5, font_size=16, showarrow=False)
                ],
            )
            fig.update_traces(
                hoverinfo="label+percent+value",
                textinfo="percent",
                marker=dict(
                    colors=graph_colors,
                ),
            )

            return (
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "Concrete", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "Reinforcement Bar", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "STEEL - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                html.P(
                    "{:,.2f}".format(
                        df_grouped.loc[
                            df_grouped["materials"] == "TIMBER - STRUCTURAL", "ec"
                        ].values[0]
                    ),
                    className="text-center",
                ),
                total,
                gfa_calc,
                dcc.Graph(figure=fig),
            )
