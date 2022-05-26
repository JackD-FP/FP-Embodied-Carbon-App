"""
TODO:
    - Classes have been implemented incase there is a need for extra functionality
        - There is a possibility for to add a sum() for each beam/column/slab/wall/stairs element
    
"""

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from src import greenbook_options

gb_layout = [
    dbc.Card(
        [
            dcc.Store(id="gb_store", storage_type="session"),
            dcc.Store(id="beam_store", storage_type="session"),
            dcc.Store(id="col_store", storage_type="session"),
            dcc.Store(id="slab_store", storage_type="session"),
            dcc.Store(id="wall_store", storage_type="session"),
            dcc.Store(id="stair_store", storage_type="session"),
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
                                    dbc.Tab(
                                        label="Beams",
                                        tab_id="Beams",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Columns",
                                        tab_id="Columns",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Slabs",
                                        tab_id="Slabs",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Walls",
                                        tab_id="Walls",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                    dbc.Tab(
                                        label="Stairs",
                                        tab_id="Stairs",
                                        active_label_class_name="fw-bold text-primary",
                                        label_class_name="text-dark",
                                    ),
                                ],
                            ),
                            # content for tab divs
                            html.Div(id="gb_tab_content", className="m-5"),
                        ]
                    ),
                    dmc.Col(html.Div(id="gb_analysis_pie")),
                ],
            ),
        ],
        class_name="my-5 p-4 shadow",
    )
]


class table:
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
                        html.Th("Materials"),
                        html.Th("Embodied Carbon"),
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
            {"name": "Concrete", "value": 643},
            {"name": "Reinforcement Bar", "value": 2.340},
            {"name": "Structural Steel", "value": 2.9},
            {"name": "Structural Timber", "value": 718},
        ]
        rows = []

        for i, options in enumerate(options):
            mat_row = html.Tr(
                [
                    html.Td(
                        dbc.Row(
                            [
                                dbc.Col(children=dmc.Text(labels[i]["name"])),
                                dbc.Col(
                                    children=dbc.Select(
                                        id="sel-{}-{}".format(
                                            self.id, labels[i]["name"].replace(" ", "-")
                                        ),
                                        options=options,
                                        value=labels[i]["value"],
                                        persistence=True,
                                    )
                                ),
                            ]
                        )
                    ),
                    html.Td(
                        mat_val[i],
                        id="val-{}-{}".format(
                            self.id, labels[i]["name"].replace(" ", "-")
                        ),
                    ),
                ]
            )

            rows.append(mat_row)
        return dbc.Table(table_head + [html.Tbody(rows, className="w-75")])


# class tots_bm:
#     def __init__(self, total, bm) -> None:
#         self.total = total
#         self.bm = bm

#     def total_calc(self):
#         df = pd.read_json(self.total, orient="split")
#         return df["gb_ec"].sum()


# ---- object instantiate ----
beams = table(
    id="beams",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
columns = table(
    id="Columns",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
slabs = table(
    id="Slabs",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
walls = table(
    id="Walls",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)
stairs = table(
    id="Stairs",
    concrete_options=greenbook_options.concrete,
    rebar_options=greenbook_options.rebar,
    steel_options=greenbook_options.steel,
    timber_options=greenbook_options.timber,
)


class total:
    def __init__(self) -> None:
        self.beam_obj = beams
        self.beam_total = sum(
            [
                self.beam_obj.conc_val,
                self.beam_obj.rebar_val,
                self.beam_obj.steel_val,
                self.beam_obj.timber_val,
            ]
        )
        self.column_obj = columns
        self.column_total = sum(
            [
                self.column_obj.conc_val,
                self.column_obj.rebar_val,
                self.column_obj.steel_val,
                self.column_obj.timber_val,
            ]
        )
        self.slab_obj = slabs
        self.slab_total = sum(
            [
                self.slab_obj.conc_val,
                self.slab_obj.rebar_val,
                self.slab_obj.steel_val,
                self.slab_obj.timber_val,
            ]
        )
        self.wall_obj = walls
        self.wall_total = sum(
            [
                self.wall_obj.conc_val,
                self.wall_obj.rebar_val,
                self.wall_obj.steel_val,
                self.wall_obj.timber_val,
            ]
        )
        self.stairs_obj = stairs
        self.stairs_total = sum(
            [
                self.stairs_obj.conc_val,
                self.stairs_obj.rebar_val,
                self.stairs_obj.steel_val,
                self.stairs_obj.timber_val,
            ]
        )


@callback(
    Output("gb_store", "data"),
    Input("proc_store", "data"),
    Input("beam_store", "modified_timestamp"),
    Input("col_store", "modified_timestamp"),
    Input("slab_store", "modified_timestamp"),
    Input("wall_store", "modified_timestamp"),
    Input("stair_store", "modified_timestamp"),
    State("beam_store", "data"),
    State("col_store", "data"),
    State("slab_store", "data"),
    State("wall_store", "data"),
    State("stair_store", "data"),
)
def update_gb_store(
    proc_store,
    beam_store_mts,
    col_store_mts,
    slab_store_mts,
    wall_store_mts,
    stair_store_mts,
    beam_store,
    col_store,
    slab_store,
    wall_store,
    stair_store,
):
    df = pd.read_json(proc_store, orient="split")
    beam_store_df = None
    col_store_df = None
    slab_store_df = None
    wall_store_df = None
    stair_store_df = None

    print("DF print\n", df)
    df.to_excel("test_df.xlsx")
    print("DF Total:\n", df["Green Book EC"].sum())
    if beam_store is None:
        beam_store_df = df.loc[(df["Element"] == "Beam")].copy()
    else:
        beam_df = pd.read_json(beam_store, orient="split")
        beam_store_df = beam_df.loc[(beam_df["Element"] == "Beam")]
        print("number of rows of beams\n", len(beam_store_df))
        # print(beam_store_df.sort_values(by="Floor Level"))

    if col_store is None:
        col_store_df = df.loc[(df["Element"] == "Column")].copy()
    else:
        col_df = pd.read_json(col_store, orient="split")
        col_store_df = col_df.loc[(col_df["Element"] == "Column")]
        print("number of rows of column\n", len(col_store_df))

    if slab_store is None:
        slab_store_df = df.loc[(df["Element"] == "Slab")].copy()
    else:
        slab_df = pd.read_json(slab_store, orient="split")
        slab_store_df = slab_df.loc[(slab_df["Element"] == "Slab")]
        print("number of rows of slab\n", len(slab_store_df))

    if wall_store is None:
        wall_store_df = df.loc[(df["Element"] == "Wall")].copy()
    else:
        wall_df = pd.read_json(wall_store, orient="split")
        wall_store_df = wall_df.loc[(wall_df["Element"] == "Wall")]
        print("number of rows of walls\n", len(wall_store_df))

    if stair_store is None:
        stair_store_df = df.loc[(df["Element"] == "Stairs")].copy()
    else:
        stair_df = pd.read_json(stair_store, orient="split")
        stair_store_df = stair_df.loc[(stair_df["Element"] == "Stairs")]
        print("number of rows of stairs\n", len(stair_store_df))

    gb_store_update = pd.concat(
        [beam_store_df, col_store_df, slab_store_df, wall_store_df, stair_store_df]
    )
    print("New edited data\n", gb_store_update)
    gb_store_update.to_excel("test_gb_store_update.xlsx")
    print("New edited total\n", gb_store_update["Green Book EC"].sum())
    # return gb_store_update.to_json(orient="split")
    return proc_store


# ---- This updates the total and benchmark ----
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


# ---- This updates/generates the table ----
@callback(
    Output("gb_tab_content", "children"),
    Input("gb_tabs", "active_tab"),
)
def update_layout(tabs):
    content = {
        "Beams": beams.table_gen(),
        "Columns": columns.table_gen(),
        "Slabs": slabs.table_gen(),
        "Walls": walls.table_gen(),
        "Stairs": stairs.table_gen(),
    }

    return content.get(tabs, "Error")


list = ["Concrete", "Reinforcement Bar", "Structural Steel", "Structural Timber"]


def material_dic(df: pd.DataFrame, cell_column: str, element: str) -> dict:
    """returns a dictionary of the material values for a given element

    Args:
        df (pd.DataFrame): dataframe of the material values
        cell_column (str): column name to access from df (Element, Materials, etc)
        element (str): Beam, Column, Slab, Wall, or Stairs

    Returns:
        dict: dictionary of elements mass or volume
    """
    d = []
    for i, mat in enumerate(list):
        try:
            val = df.loc[
                (df["Element"] == element) & (df["Materials"] == mat),
                cell_column,
            ].values[0]

        except:
            val = 0

        d.append((mat, val))
        vol = dict(d)
    return vol


def for_storage(
    df: pd.DataFrame, element: str, material: str, val: float
) -> pd.DataFrame:
    new_df = df.loc[(df["Element"] == element) & (df["Materials"] == material)].copy()
    ec_list = []
    # submat_list = []
    for i, rows in new_df.iterrows():
        ec_list.append(float(val) * rows["Volume"])
        # submat_list.append()

    new_df["Green Book EC"] = ec_list
    # return new_df.assign(gb_ec=ec_list)
    return new_df


# ---- callback for elements ----
@callback(
    Output("val-beams-Concrete", "children"),
    Output("val-beams-Reinforcement-Bar", "children"),
    Output("val-beams-Structural-Steel", "children"),
    Output("val-beams-Structural-Timber", "children"),
    Output("beam_store", "data"),
    Input("sel-beams-Concrete", "value"),
    Input("sel-beams-Reinforcement-Bar", "value"),
    Input("sel-beams-Structural-Steel", "value"),
    Input("sel-beams-Structural-Timber", "value"),
    State("proc_store", "data"),
)
def beam_val_update(conc_val, reb_val, ste_val, tim_val, data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df.drop(["Green Book EC"], axis=1, inplace=True)
        df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        vol = material_dic(df_grouped, "Volume", "Beam")
        mass = material_dic(df_grouped, "Mass", "Beam")
        beams.conc_val = float(conc_val) * vol["Concrete"]
        beams.rebar_val = float(reb_val) * mass["Reinforcement Bar"]
        beams.steel_val = float(ste_val) * mass["Structural Steel"]
        beams.timber_val = float(tim_val) * vol["Structural Timber"]

        concrete = for_storage(df, "Beam", "Concrete", float(conc_val))
        rebar = for_storage(df, "Beam", "Reinforcement Bar", float(conc_val))
        steel = for_storage(df, "Beam", "Structural Steel", float(conc_val))
        timber = for_storage(df, "Beam", "Structural Timber", float(conc_val))
        beam_data = pd.concat([concrete, rebar, steel, timber])

        return (
            "{:,.2f}".format(beams.conc_val),
            "{:,.2f}".format(beams.rebar_val),
            "{:,.2f}".format(beams.steel_val),
            "{:,.2f}".format(beams.timber_val),
            beam_data.to_json(orient="split"),
        )


@callback(
    Output("val-Columns-Concrete", "children"),
    Output("val-Columns-Reinforcement-Bar", "children"),
    Output("val-Columns-Structural-Steel", "children"),
    Output("val-Columns-Structural-Timber", "children"),
    Output("col_store", "data"),
    Input("sel-Columns-Concrete", "value"),
    Input("sel-Columns-Reinforcement-Bar", "value"),
    Input("sel-Columns-Structural-Steel", "value"),
    Input("sel-Columns-Structural-Timber", "value"),
    State("proc_store", "data"),
)
def col_val_update(conc_val, reb_val, ste_val, tim_val, data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df.drop(["Green Book EC"], axis=1, inplace=True)
        df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        vol = material_dic(df_grouped, "Volume", "Column")
        mass = material_dic(df_grouped, "Mass", "Column")
        columns.conc_val = float(conc_val) * vol["Concrete"]
        columns.rebar_val = float(reb_val) * mass["Reinforcement Bar"]
        columns.steel_val = float(ste_val) * mass["Structural Steel"]
        columns.timber_val = float(tim_val) * vol["Structural Timber"]

        concrete = for_storage(df, "Column", "Concrete", float(conc_val))
        rebar = for_storage(df, "Column", "Reinforcement Bar", float(conc_val))
        steel = for_storage(df, "Column", "Structural Steel", float(conc_val))
        timber = for_storage(df, "Column", "Structural Timber", float(conc_val))
        col_data = pd.concat([concrete, rebar, steel, timber])

        return (
            "{:,.2f}".format(columns.conc_val),
            "{:,.2f}".format(columns.rebar_val),
            "{:,.2f}".format(columns.steel_val),
            "{:,.2f}".format(columns.timber_val),
            col_data.to_json(orient="split"),
        )


@callback(
    Output("val-Slabs-Concrete", "children"),
    Output("val-Slabs-Reinforcement-Bar", "children"),
    Output("val-Slabs-Structural-Steel", "children"),
    Output("val-Slabs-Structural-Timber", "children"),
    Output("slab_store", "data"),
    Input("sel-Slabs-Concrete", "value"),
    Input("sel-Slabs-Reinforcement-Bar", "value"),
    Input("sel-Slabs-Structural-Steel", "value"),
    Input("sel-Slabs-Structural-Timber", "value"),
    State("proc_store", "data"),
)
def slab_val_update(conc_val, reb_val, ste_val, tim_val, data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df.drop(["Green Book EC"], axis=1, inplace=True)
        df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        vol = material_dic(df_grouped, "Volume", "Slab")
        mass = material_dic(df_grouped, "Mass", "Slab")
        slabs.conc_val = float(conc_val) * vol["Concrete"]
        slabs.rebar_val = float(reb_val) * mass["Reinforcement Bar"]
        slabs.steel_val = float(ste_val) * mass["Structural Steel"]
        slabs.timber_val = float(tim_val) * vol["Structural Timber"]

        concrete = for_storage(df, "Column", "Concrete", float(conc_val))
        rebar = for_storage(df, "Column", "Reinforcement Bar", float(conc_val))
        steel = for_storage(df, "Column", "Structural Steel", float(conc_val))
        timber = for_storage(df, "Column", "Structural Timber", float(conc_val))
        slab_data = pd.concat([concrete, rebar, steel, timber])
        print("print len_data\n", len(slab_data))

        return (
            "{:,.2f}".format(slabs.conc_val),
            "{:,.2f}".format(slabs.rebar_val),
            "{:,.2f}".format(slabs.steel_val),
            "{:,.2f}".format(slabs.timber_val),
            slab_data.to_json(orient="split"),
        )


@callback(
    Output("val-Walls-Concrete", "children"),
    Output("val-Walls-Reinforcement-Bar", "children"),
    Output("val-Walls-Structural-Steel", "children"),
    Output("val-Walls-Structural-Timber", "children"),
    Output("wall_store", "data"),
    Input("sel-Walls-Concrete", "value"),
    Input("sel-Walls-Reinforcement-Bar", "value"),
    Input("sel-Walls-Structural-Steel", "value"),
    Input("sel-Walls-Structural-Timber", "value"),
    State("proc_store", "data"),
)
def wall_val_update(conc_val, reb_val, ste_val, tim_val, data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df.drop(["Green Book EC"], axis=1, inplace=True)
        df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        vol = material_dic(df_grouped, "Volume", "Wall")
        mass = material_dic(df_grouped, "Mass", "Wall")
        walls.conc_val = float(conc_val) * vol["Concrete"]
        walls.rebar_val = float(reb_val) * mass["Reinforcement Bar"]
        walls.steel_val = float(ste_val) * mass["Structural Steel"]
        walls.timber_val = float(tim_val) * vol["Structural Timber"]

        concrete = for_storage(df, "Wall", "Concrete", float(conc_val))
        rebar = for_storage(df, "Wall", "Reinforcement Bar", float(conc_val))
        steel = for_storage(df, "Wall", "Structural Steel", float(conc_val))
        timber = for_storage(df, "Wall", "Structural Timber", float(conc_val))
        wall_data = pd.concat([concrete, rebar, steel, timber])

        return (
            "{:,.2f}".format(walls.conc_val),
            "{:,.2f}".format(walls.rebar_val),
            "{:,.2f}".format(walls.steel_val),
            "{:,.2f}".format(walls.timber_val),
            wall_data.to_json(orient="split"),
        )


@callback(
    Output("val-Stairs-Concrete", "children"),
    Output("val-Stairs-Reinforcement-Bar", "children"),
    Output("val-Stairs-Structural-Steel", "children"),
    Output("val-Stairs-Structural-Timber", "children"),
    Output("stair_store", "data"),
    Input("sel-Stairs-Concrete", "value"),
    Input("sel-Stairs-Reinforcement-Bar", "value"),
    Input("sel-Stairs-Structural-Steel", "value"),
    Input("sel-Stairs-Structural-Timber", "value"),
    State("proc_store", "data"),
)
def stair_val_update(conc_val, reb_val, ste_val, tim_val, data):

    if data is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        df.drop(["Green Book EC"], axis=1, inplace=True)
        df_grouped = df.groupby(["Element", "Materials"], as_index=False).sum()

        vol = material_dic(df_grouped, "Volume", "Stair")
        mass = material_dic(df_grouped, "Mass", "Stair")
        stairs.conc_val = float(conc_val) * vol["Concrete"]
        stairs.rebar_val = float(reb_val) * mass["Reinforcement Bar"]
        stairs.steel_val = float(ste_val) * mass["Structural Steel"]
        stairs.timber_val = float(tim_val) * vol["Structural Timber"]

        concrete = for_storage(df, "Stairs", "Concrete", float(conc_val))
        rebar = for_storage(df, "Stairs", "Reinforcement Bar", float(conc_val))
        steel = for_storage(df, "Stairs", "Structural Steel", float(conc_val))
        timber = for_storage(df, "Stairs", "Structural Timber", float(conc_val))
        stair_data = pd.concat([concrete, rebar, steel, timber])

        return (
            "{:,.2f}".format(stairs.conc_val),
            "{:,.2f}".format(stairs.rebar_val),
            "{:,.2f}".format(stairs.steel_val),
            "{:,.2f}".format(stairs.timber_val),
            stair_data.to_json(orient="split"),
        )
