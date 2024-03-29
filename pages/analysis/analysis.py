import json
import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from config import config
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from pages.analysis import custom_analysis
from src import analysis_comparison, funcs, material_options, settings


class table:
    """
    This class generates the table and store some values to help in the calculation of the embodied carbon.
    """

    def __init__(
        self,
        id,
        concrete_options,
        rebar_options,
        steel_options,
        timber_options,
        concrete=0,
        rebar=0,
        steel=0,
        timber=0,
    ):
        self.id = id
        self.concrete_options = concrete_options
        self.rebar_options = rebar_options
        self.steel_options = steel_options
        self.timber_options = timber_options
        self.conc_val = concrete
        self.rebar_val = rebar
        self.steel_val = steel
        self.timber_val = timber

    def table_gen(self):
        table_head = [
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            "Material", style={"width": "40%", "textAlign": "Start"}
                        ),
                        html.Th("EPiC", style={"width": "20%", "textAlign": "end"}),
                        html.Th("ICE", style={"width": "20%", "textAlign": "end"}),
                    ]
                )
            )
        ]
        options = [
            self.concrete_options,
            self.rebar_options,
            self.steel_options,
            self.timber_options,
        ]
        mat_val = [
            self.conc_val,
            self.rebar_val,
            self.steel_val,
            self.timber_val,
        ]
        labels = [
            {"name": "Concrete", "value": "50_mpa"},
            {"name": "Rebar", "value": "rebar"},
            {"name": "Structural Steel", "value": "steel_section"},
            {"name": "Structural Timber", "value": "glulam"},
        ]
        rows = []

        for i, options in enumerate(options):
            mat_row = html.Tr(
                [
                    html.Td(
                        dbc.Row(
                            [
                                dmc.Text(
                                    labels[i]["name"],
                                ),
                                dbc.Select(
                                    id="sel-{}-{}".format(
                                        self.id, labels[i]["name"].replace(" ", "-")
                                    ),
                                    options=options,
                                    value=labels[i]["value"],
                                    persistence=True,
                                ),
                            ]
                        )
                    ),
                    html.Td(
                        mat_val[i],
                        id="epic-val-{}-{}".format(
                            self.id, labels[i]["name"].replace(" ", "-")
                        ),
                        style={"verticalAlign": "bottom", "textAlign": "end"},
                    ),
                    html.Td(
                        mat_val[i],
                        id="ice-val-{}-{}".format(
                            self.id, labels[i]["name"].replace(" ", "-")
                        ),
                        style={"verticalAlign": "bottom", "textAlign": "end"},
                    ),
                ]
            )

            rows.append(mat_row)
        return dmc.Table(table_head + [html.Tbody(rows)])


beams = table(
    id="beams",
    concrete_options=material_options.concrete,
    rebar_options=material_options.rebar,
    steel_options=material_options.steel,
    timber_options=material_options.timber,
)
columns = table(
    id="Columns",
    concrete_options=material_options.concrete,
    rebar_options=material_options.rebar,
    steel_options=material_options.steel,
    timber_options=material_options.timber,
)
slabs = table(
    id="Slabs",
    concrete_options=material_options.concrete,
    rebar_options=material_options.rebar,
    steel_options=material_options.steel,
    timber_options=material_options.timber,
)
walls = table(
    id="Walls",
    concrete_options=material_options.concrete,
    rebar_options=material_options.rebar,
    steel_options=material_options.steel,
    timber_options=material_options.timber,
)
stairs = table(
    id="Stairs",
    concrete_options=material_options.concrete,
    rebar_options=material_options.rebar,
    steel_options=material_options.steel,
    timber_options=material_options.timber,
)


# callback that converts all the inputs into a new df
# then output to stores to analysis_store
# lets just accept it is what it is... i hate the massive callback
# but it works for now
@callback(
    [
        Output("epic-val-beams-Concrete", "children"),
        Output("ice-val-beams-Concrete", "children"),
        Output("epic-val-beams-Rebar", "children"),
        Output("ice-val-beams-Rebar", "children"),
        Output("epic-val-beams-Structural-Steel", "children"),
        Output("ice-val-beams-Structural-Steel", "children"),
        Output("epic-val-beams-Structural-Timber", "children"),
        Output("ice-val-beams-Structural-Timber", "children"),
        Output("epic-val-Columns-Concrete", "children"),
        Output("ice-val-Columns-Concrete", "children"),
        Output("epic-val-Columns-Rebar", "children"),
        Output("ice-val-Columns-Rebar", "children"),
        Output("epic-val-Columns-Structural-Steel", "children"),
        Output("ice-val-Columns-Structural-Steel", "children"),
        Output("epic-val-Columns-Structural-Timber", "children"),
        Output("ice-val-Columns-Structural-Timber", "children"),
        Output("epic-val-Slabs-Concrete", "children"),
        Output("ice-val-Slabs-Concrete", "children"),
        Output("epic-val-Slabs-Rebar", "children"),
        Output("ice-val-Slabs-Rebar", "children"),
        Output("epic-val-Slabs-Structural-Steel", "children"),
        Output("ice-val-Slabs-Structural-Steel", "children"),
        Output("epic-val-Slabs-Structural-Timber", "children"),
        Output("ice-val-Slabs-Structural-Timber", "children"),
        Output("epic-val-Walls-Concrete", "children"),
        Output("ice-val-Walls-Concrete", "children"),
        Output("epic-val-Walls-Rebar", "children"),
        Output("ice-val-Walls-Rebar", "children"),
        Output("epic-val-Walls-Structural-Steel", "children"),
        Output("ice-val-Walls-Structural-Steel", "children"),
        Output("epic-val-Walls-Structural-Timber", "children"),
        Output("ice-val-Walls-Structural-Timber", "children"),
        Output("epic-val-Stairs-Concrete", "children"),
        Output("ice-val-Stairs-Concrete", "children"),
        Output("epic-val-Stairs-Rebar", "children"),
        Output("ice-val-Stairs-Rebar", "children"),
        Output("epic-val-Stairs-Structural-Steel", "children"),
        Output("ice-val-Stairs-Structural-Steel", "children"),
        Output("epic-val-Stairs-Structural-Timber", "children"),
        Output("ice-val-Stairs-Structural-Timber", "children"),
        Output("analysis_store", "data"),
        # Output("main_store", "data"),
    ],
    [
        Input("sel-beams-Concrete", "value"),
        Input("sel-beams-Rebar", "value"),
        Input("sel-beams-Structural-Steel", "value"),
        Input("sel-beams-Structural-Timber", "value"),
        Input("sel-Columns-Concrete", "value"),
        Input("sel-Columns-Rebar", "value"),
        Input("sel-Columns-Structural-Steel", "value"),
        Input("sel-Columns-Structural-Timber", "value"),
        Input("sel-Slabs-Concrete", "value"),
        Input("sel-Slabs-Rebar", "value"),
        Input("sel-Slabs-Structural-Steel", "value"),
        Input("sel-Slabs-Structural-Timber", "value"),
        Input("sel-Walls-Concrete", "value"),
        Input("sel-Walls-Rebar", "value"),
        Input("sel-Walls-Structural-Steel", "value"),
        Input("sel-Walls-Structural-Timber", "value"),
        Input("sel-Stairs-Concrete", "value"),
        Input("sel-Stairs-Rebar", "value"),
        Input("sel-Stairs-Structural-Steel", "value"),
        Input("sel-Stairs-Structural-Timber", "value"),
        # Input("beam_slider", "value"),
        # Input("column_slider", "value"),
        # Input("slab_slider", "value"),
        # Input("wall_slider", "value"),
        # Input("stair_slider", "value"),
    ],
    State("main_store", "data"),
    prevent_initial_call=True,
)
def analysis_update(
    beam_conc,
    beam_rebar,
    beam_steel,
    beam_timber,
    col_conc,
    col_rebar,
    col_steel,
    col_timber,
    slab_conc,
    slab_rebar,
    slab_steel,
    slab_timber,
    wall_conc,
    wall_rebar,
    wall_steel,
    wall_timber,
    stair_conc,
    stair_rebar,
    stair_steel,
    stair_timber,
    # beam_slider,
    # column_slider,
    # slab_slider,
    # wall_slider,
    # stair_slider,
    data,
):
    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")

        mat, vol, mass, floor, element, epicec, iceec = funcs.mat_interpreter(
            df,
            39,
            41,
            13,
            11,
            19.5,
            # , beam_slider, column_slider, slab_slider, wall_slider, stair_slider
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
        df_new.drop(columns=["EPiC EC", "ICE EC"], inplace=True)
        # df_new.to_excel("analysis.xlsx") # for debugging

        epic_sub_materials = []
        ice_sub_materials = []

        epic_ec = []
        ice_ec = []

        colors = []

        for i, row in df_new.iterrows():
            if row["Element"] == "Beam":
                material_dict = {
                    "Concrete": funcs.concrete(beam_conc, row["Volume"]),
                    "Reinforcement Bar": funcs.rebar(beam_rebar, row["Mass"]),
                    "Structural Steel": funcs.steel(beam_steel, row["Mass"]),
                    "Structural Timber": funcs.timber(
                        beam_timber, row["Mass"], row["Volume"]
                    ),
                }
                epic_ec.append(material_dict.get(row["Material"])[0])
                epic_sub_materials.append(material_dict.get(row["Material"])[1])
                ice_ec.append(material_dict.get(row["Material"])[2])
                ice_sub_materials.append(material_dict.get(row["Material"])[3])
                colors.append(material_dict.get(row["Material"])[4])

            if row["Element"] == "Column":
                material_dict = {
                    "Concrete": funcs.concrete(col_conc, row["Volume"]),
                    "Reinforcement Bar": funcs.rebar(col_rebar, row["Mass"]),
                    "Structural Steel": funcs.steel(col_steel, row["Mass"]),
                    "Structural Timber": funcs.timber(
                        col_timber, row["Mass"], row["Volume"]
                    ),
                }
                epic_ec.append(material_dict.get(row["Material"])[0])
                epic_sub_materials.append(material_dict.get(row["Material"])[1])
                ice_ec.append(material_dict.get(row["Material"])[2])
                ice_sub_materials.append(material_dict.get(row["Material"])[3])
                colors.append(material_dict.get(row["Material"])[4])

            if row["Element"] == "Slab":
                material_dict = {
                    "Concrete": funcs.concrete(slab_conc, row["Volume"]),
                    "Reinforcement Bar": funcs.rebar(slab_rebar, row["Mass"]),
                    "Structural Steel": funcs.steel(slab_steel, row["Mass"]),
                    "Structural Timber": funcs.timber(
                        slab_timber, row["Mass"], row["Volume"]
                    ),
                }
                epic_ec.append(material_dict.get(row["Material"])[0])
                epic_sub_materials.append(material_dict.get(row["Material"])[1])
                ice_ec.append(material_dict.get(row["Material"])[2])
                ice_sub_materials.append(material_dict.get(row["Material"])[3])
                colors.append(material_dict.get(row["Material"])[4])

            if row["Element"] == "Wall":
                material_dict = {
                    "Concrete": funcs.concrete(wall_conc, row["Volume"]),
                    "Reinforcement Bar": funcs.rebar(wall_rebar, row["Mass"]),
                    "Structural Steel": funcs.steel(wall_steel, row["Mass"]),
                    "Structural Timber": funcs.timber(
                        wall_timber, row["Mass"], row["Volume"]
                    ),
                }
                epic_ec.append(material_dict.get(row["Material"])[0])
                epic_sub_materials.append(material_dict.get(row["Material"])[1])
                ice_ec.append(material_dict.get(row["Material"])[2])
                ice_sub_materials.append(material_dict.get(row["Material"])[3])
                colors.append(material_dict.get(row["Material"])[4])

            if row["Element"] == "Stairs":
                material_dict = {
                    "Concrete": funcs.concrete(stair_conc, row["Volume"]),
                    "Reinforcement Bar": funcs.rebar(stair_rebar, row["Mass"]),
                    "Structural Steel": funcs.steel(stair_steel, row["Mass"]),
                    "Structural Timber": funcs.timber(
                        stair_timber, row["Mass"], row["Volume"]
                    ),
                }
                epic_ec.append(material_dict.get(row["Material"])[0])
                epic_sub_materials.append(material_dict.get(row["Material"])[1])
                ice_ec.append(material_dict.get(row["Material"])[2])
                ice_sub_materials.append(material_dict.get(row["Material"])[3])
                colors.append(material_dict.get(row["Material"])[4])

        df_new.insert(loc=1, column="EPiC Material", value=epic_sub_materials)
        df_new.insert(loc=2, column="ICE Material", value=ice_sub_materials)
        df_new.insert(loc=4, column="EPiC EC", value=epic_ec)
        df_new.insert(loc=5, column="ICE EC", value=ice_ec)
        df_new.insert(loc=6, column="Colors", value=colors)

        # df_new.to_excel("test.xlsx", index=False)

        return (
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam") & (df_new["Material"] == "Concrete"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam") & (df_new["Material"] == "Concrete"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Structural Steel"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Structural Steel"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Structural Timber"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Beam")
                    & (df_new["Material"] == "Structural Timber"),
                    "ICE EC",
                ].sum()
            ),
            # columns
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Concrete"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Concrete"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Structural Steel"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Structural Steel"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Structural Timber"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Column")
                    & (df_new["Material"] == "Structural Timber"),
                    "ICE EC",
                ].sum()
            ),
            # Slab
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab") & (df_new["Material"] == "Concrete"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab") & (df_new["Material"] == "Concrete"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Structural Steel"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Structural Steel"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Structural Timber"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Slab")
                    & (df_new["Material"] == "Structural Timber"),
                    "ICE EC",
                ].sum()
            ),
            # Wall
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall") & (df_new["Material"] == "Concrete"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall") & (df_new["Material"] == "Concrete"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Structural Steel"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Structural Steel"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Structural Timber"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Wall")
                    & (df_new["Material"] == "Structural Timber"),
                    "ICE EC",
                ].sum()
            ),
            # stair
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Concrete"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Concrete"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Reinforcement Bar"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Structural Steel"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Structural Steel"),
                    "ICE EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Structural Timber"),
                    "EPiC EC",
                ].sum()
            ),
            "{:,.2f}".format(
                df_new.loc[
                    (df_new["Element"] == "Stairs")
                    & (df_new["Material"] == "Structural Timber"),
                    "ICE EC",
                ].sum()
            ),
            # analysis_store
            df_new.to_json(orient="split"),
        )


# updates the % difference between old values and new values
@callback(
    [
        Output("epic_analysis_current_total", "children"),
        Output("epic_analysis_prev_total", "children"),
        Output("epic_badge", "children"),
        Output("ice_analysis_current_total", "children"),
        Output("ice_analysis_prev_total", "children"),
        Output("ice_badge", "children"),
        Output("ec_prev", "data"),
    ],
    Input("analysis_store", "data"),
    [
        State("ec_prev", "data"),
    ],
)
def totals_update(analysis_store, ec_prev):
    df = pd.read_json(analysis_store, orient="split")
    epic_total = df["EPiC EC"].sum()
    ice_total = df["ICE EC"].sum()
    tots_2_json = json.dumps(
        {
            "epic": epic_total,
            "ice": ice_total,
        },
        sort_keys=True,
        indent=4,
    )

    if ec_prev is not None:  # if there is a previous ec value
        data = json.loads(ec_prev)  # convert load from json
        epic_percent = funcs.percent_diff(epic_total, data["epic"])
        ice_percent = funcs.percent_diff(ice_total, data["ice"])

        tots_2_json = json.dumps(
            {
                "epic": epic_total,
                "ice": ice_total,
            },
            sort_keys=True,
            indent=4,
        )

        return (
            "{:,.2f} kgCO₂e".format(epic_total),
            "from {:,.2f}".format(data["epic"]),
            epic_percent,
            "{:,.2f} kgCO₂e".format(ice_total),
            "from {:,.2f}".format(data["ice"]),
            ice_percent,
            tots_2_json,
        )
    else:
        return (
            "{:,.2f} kgCO₂e".format(epic_total),
            "",
            "",
            "{:,.2f} kgCO₂e".format(ice_total),
            "",
            "",
            tots_2_json,
        )


# Event driven update. OnClick with download btn will give clients the updated data
@callback(
    Output("analysis_db_download", "data"),
    Input("analysis_btn_download", "n_clicks"),
    State("analysis_store", "data"),
    prevent_initial_call=True,
)
def db_download_update(n_clicks, data):
    df = pd.read_json(data, orient="split")
    return dcc.send_data_frame(df.to_csv, "EC_Analysis_{}.csv".format(n_clicks))


# updates the table with consolidated data
@callback(
    Output("analysis_table", "children"),
    Input("analysis_store", "data"),
)
def table_update(data):
    df = pd.read_json(data, orient="split")
    df_grouped = df.groupby(["Element", "Material"], as_index=False).sum().round(2)
    return dmc.Table(
        funcs.create_table(df_grouped), highlightOnHover=True, class_name="my-5"
    )


totals_ui = [
    dmc.Paper(  # epic
        [
            dmc.Text("EPiC DB:", size="lg", weight="bold"),
            dmc.Group(
                [
                    dmc.Text(
                        "Calculating...",
                        class_name="fs-3",
                        weight="bold",
                        color="blue",
                        id="epic_analysis_current_total",
                    ),
                    html.Div(
                        [
                            dmc.Text(
                                color="gray",
                                id="epic_analysis_prev_total",
                            ),
                            html.Div(id="epic_badge"),
                        ]
                    ),
                ],
                spacing="md",
                direction="row",
            ),
        ],
        withBorder=True,
        shadow="sm",
        class_name="p-3 m-4",
    ),
    dmc.Paper(  # ice
        [
            dmc.Text("ICE DB:", size="lg", weight="bold"),
            dmc.Group(
                [
                    dmc.Text(
                        "Calculating...",
                        class_name="fs-3",
                        weight="bold",
                        color="blue",
                        id="ice_analysis_current_total",
                    ),
                    html.Div(
                        [
                            dmc.Text(
                                color="gray",
                                id="ice_analysis_prev_total",
                            ),
                            html.Div(id="ice_badge"),
                        ]
                    ),
                ],
                spacing="md",
                direction="row",
            ),
        ],
        withBorder=True,
        shadow="sm",
        class_name="p-3 m-4",
    ),
    dcc.Download(id="analysis_db_download"),
    dmc.Button(
        "Download Database",
        leftIcon=[DashIconify(icon="ant-design:download-outlined")],
        id="analysis_btn_download",
        class_name="mx-4",
    ),
]

# create the layout for the cards
# gen_analysis was separated from analysis_layout just to make it cleaner to read
gen_analysis = dbc.Row(
    children=[
        dbc.Col(
            dmc.Paper(
                children=[
                    html.H3("Beams"),
                    dmc.Divider(class_name="mb-3"),
                    beams.table_gen(),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                class_name="p-5",
            ),
            xxl=4,
            xl=12,
        ),
        dbc.Col(
            dmc.Paper(
                children=[
                    html.H3("Columns"),
                    dmc.Divider(class_name="mb-3"),
                    columns.table_gen(),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                class_name="p-5",
            ),
            xxl=4,
            xl=12,
        ),
        dbc.Col(
            dmc.Paper(
                children=[
                    html.H3("Slabs"),
                    dmc.Divider(class_name="mb-3"),
                    slabs.table_gen(),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                class_name="p-5",
            ),
            xxl=4,
            xl=12,
        ),
        dbc.Col(
            dmc.Paper(
                children=[
                    html.H3("Walls"),
                    dmc.Divider(class_name="mb-3"),
                    walls.table_gen(),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                class_name="p-5",
            ),
            xxl=4,
            xl=12,
        ),
        dbc.Col(
            dmc.Paper(
                children=[
                    html.H3("Stairs"),
                    dmc.Divider(class_name="mb-3"),
                    stairs.table_gen(),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                class_name="p-5",
            ),
            xxl=4,
            xl=12,
        ),
        dbc.Col(
            children=[
                dmc.Tabs(
                    children=[
                        dmc.Tab(
                            label="Totals",
                            icon=[DashIconify(icon="iconoir:graph-up")],
                            children=totals_ui,
                        ),
                    ]
                ),
            ],
            xxl=4,
            xl=12,
        ),
    ],
    class_name="g-3",
)
# full page layout
analysis_layout = html.Div(
    [
        dcc.Store(id="ec_prev", storage_type="memory"),
        html.H1("Analysis", className="display-2 mb-5 "),
        html.Hr(className="mb-5"),
        analysis_comparison.comparison,
        html.Div(
            id="analysis_table",
        ),
        dmc.Tabs(
            children=[
                dmc.Tab(
                    children=[
                        gen_analysis,
                    ],
                    label="General Analysis",
                ),
                dmc.Tab(
                    label="Custom Analysis",
                    children=[
                        custom_analysis.layout,
                    ],
                ),
            ],
            color="blue",
            active=0,
        ),
    ]
)
