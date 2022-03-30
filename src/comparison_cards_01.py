# This generates cards for the comparison page
#   - cards: cards01, cards02, cards03
#   - each cards has the ability to generate analysis from greenbook, epic and ice

# TODO
# - add bar chart in card 01 for GB, epic and ice
# - create upload feature for cards 02 and 03

from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import  plotly.graph_objects as go
import pandas as pd
import numpy as np

from src import material_table, greenbook_options, epic_options, ice_options

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

card01 = html.Div([
    html.Div(id='card01_table')
])

@callback(
Output('card01_table', 'children'),
Input('main_store', 'modified_timestamp'), 
Input('gfa_store', 'modified_timestamp'),
State('main_store', 'data'),
State('gfa_store', 'data'),
)
def update_div(main_mts, gfa_mts, main_data, gfa_data ):
    if main_mts is None: raise PreventUpdate
    else:
        df = pd.read_json(main_data, orient="split")
        _df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        _df = _df.filter(items=['Building Materials (All)', 'Mass', 'Volume (Net)'])

        if gfa_mts is None or gfa_mts == "":
            gfa = 0
        else: gfa = gfa_data

        table_out = [
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
            html.H5(["GFA in m", html.Sup(2)]),
            dbc.Input(
                id="comp_card01_gfa",
                placeholder="What's the project Name?",
                value= gfa,
                className="w-25",
                type="text",
                debounce=True,
                persistence= True,
                persistence_type="session",
                required=True
            ),
            dmc.Divider(class_name="my-3"),

#----------- green book comparison for card 01 -----------
            html.H3("Green Book DB", className="mb-3"),
            material_table.table_gen(
                dbc.Select(options=greenbook_options.concrete_options, id="gb_comp_concrete", value="Concrete 50 MPa "),
                html.P(id="gb_comp_concrete_val"),
                dbc.Select(options=greenbook_options.steel_options, id="gb_comp_steel", value="Steel Universal Section"),
                html.P(id="gb_comp_steel_val"),
                dbc.Select(options=greenbook_options.timber_options, id="gb_comp_timber", value="Glue-Laminated Timber (Glu-lam)"),
                html.P(id="gb_comp_timber_val"),
                ),
            dbc.Row([
                dbc.Col([
                    html.H3(id="gb_comp_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.H3(id="gb_comp_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], class_name="my-5"),
            html.Div(id="gb_pie"),
            html.Div(id="gb_bars"),  # there is provision for bar graphs but will add that later        
            dmc.Divider(class_name="my-3"), 

#---------- EPIC comparison for card 01 -----------
            html.H3("EPiC DB", className="mb-3"),
            material_table.table_gen(
                dbc.Select(options=epic_options.concrete_option, id="epic_comp_concrete", value="Concrete 50 MPa"),
                html.P(id="epic_comp_concrete_val"),
                dbc.Select(options=epic_options.steel_options, id="epic_comp_steel", value="Steel structural steel section"),
                html.P(id="epic_comp_steel_val"),
                dbc.Select(options=epic_options.timber_option, id="epic_comp_timber", value="Glued laminated timber (glulam)"),
                html.P(id="epic_comp_timber_val"),
                ),
            dbc.Row([
                dbc.Col([
                    html.H3(id="epic_comp_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.H3(id="epic_comp_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], class_name="my-5"),
            html.Div(id="epic_pie"),
            dmc.Divider(class_name="my-3"),

#---------- Ice comparison for card 01 -----------
            html.H3("ICE DB", className="mb-3"),
            material_table.table_gen(
                dbc.Select(options=ice_options.concrete_options, id="ice_comp_concrete", value="Concrete 40 MPa"),
                html.P(id="ice_comp_concrete_val"),
                dbc.Select(options=ice_options.steel_options, id="ice_comp_steel", value="Steel Section"),
                html.P(id="ice_comp_steel_val"),
                dbc.Select(options=ice_options.timber_options, id="ice_comp_timber", value="Timber Glulam"),
                html.P(id="ice_comp_timber_val"),
                ),
            dbc.Row([
                dbc.Col([
                    html.H3(id="ice_comp_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.H3(id="ice_comp_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], class_name="my-5"),
            html.Div(id="ice_pie"),

        ]
        return table_out 

# ---------------- GREENBOOK CALLBACK ----------------
@callback(
Output('gb_comp_concrete_val', 'children'),
Output('gb_comp_steel_val', 'children'),
Output('gb_comp_timber_val', 'children'),
Output('gb_comp_total', 'children'),
Output('gb_comp_gfa', 'children'),
Output('gb_pie', 'children'),
Input('gb_comp_concrete', 'value'), 
Input('gb_comp_steel', 'value'), 
Input('gb_comp_timber', 'value'), 
Input('comp_card01_gfa', 'value'), 
State("main_store", "data")
)
def definition(conc_val, steel_val, timber_val, val, data):
    if data is None: raise PreventUpdate
    else:
        df = pd.read_json(data, orient="split")
        #concrete gb calculation
        conc_ec = gb_df.loc[gb_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        #iron gb calculation
        steel_ec = gb_df.loc[gb_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        #wowd gb calculation
        timber_ec = gb_df.loc[gb_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()

        gb_concrete = html.P("{:,.2f}".format((concrete := conc_ec * structure_concrete)))
        gb_steel = html.P("{:,.2f}".format((steel := steel_ec * structure_steel)))
        gb_timber = html.P("{:,.2f}".format((timber := timber_ec * structure_timber)))

        labels = [conc_val, steel_val, timber_val]
        ec_total = concrete + steel + timber
        values = [concrete, steel, timber]
        # yummy yummy pie
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])

        return gb_concrete, gb_steel, gb_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/val), dcc.Graph(figure=fig)


# ---------------- EPIC CALLBACK ----------------
@callback(
Output('epic_comp_concrete_val', 'children'),
Output('epic_comp_steel_val', 'children'),
Output('epic_comp_timber_val', 'children'),
Output('epic_comp_total', 'children'),
Output('epic_comp_gfa', 'children'),
Output('epic_pie', 'children'),
Input('epic_comp_concrete', 'value'), 
Input('epic_comp_steel', 'value'), 
Input('epic_comp_timber', 'value'), 
Input('comp_card01_gfa', 'value'), 
State("main_store", "data")
)
def definition(conc_val, steel_val, timber_val, val, data):
    if data is None: raise PreventUpdate
    else: 
        df = pd.read_json(data, orient="split")
        #concrete epic calculation
        conc_ec = epic_df.loc[epic_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        #iron epic calculation
        steel_ec = epic_df.loc[epic_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        #wowd epic calculation
        timber_ec = epic_df.loc[epic_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()
        
        epic_concrete = html.P("{:,.2f}".format((concrete := conc_ec * structure_concrete)))
        epic_steel = html.P("{:,.2f}".format((steel := steel_ec * structure_steel)))
        epic_timber = html.P("{:,.2f}".format((timber := timber_ec * structure_timber)))

        labels = [conc_val, steel_val, timber_val]
        ec_total = concrete + steel + timber
        values = [concrete, steel, timber]
        # yummy yummy pie
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])

        return epic_concrete, epic_steel, epic_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/val), dcc.Graph(figure=fig)


# ---------------- ICE CALLBACK ----------------
@callback(
Output('ice_comp_concrete_val', 'children'),
Output('ice_comp_steel_val', 'children'),
Output('ice_comp_timber_val', 'children'),
Output('ice_comp_total', 'children'),
Output('ice_comp_gfa', 'children'),
Output('ice_pie', 'children'),
Input('ice_comp_concrete', 'value'), 
Input('ice_comp_steel', 'value'), 
Input('ice_comp_timber', 'value'), 
Input('comp_card01_gfa', 'value'), 
State("main_store", "data")
)
def definition(conc_val, steel_val, timber_val, val, data):
    if data is None: raise PreventUpdate
    else: 
        df = pd.read_json(data, orient="split")
        #concrete ice calculation
        conc_ec = ice_df.loc[ice_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        #iron ice calculation
        steel_ec = ice_df.loc[ice_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        #wowd ice calculation
        timber_ec = ice_df.loc[ice_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Mass"].sum()
        
        ice_concrete = html.P("{:,.2f}".format((concrete := conc_ec * structure_concrete)))
        ice_steel = html.P("{:,.2f}".format((steel := steel_ec * structure_steel)))
        ice_timber = html.P("{:,.2f}".format((timber := timber_ec * structure_timber)))

        labels = [conc_val, steel_val, timber_val]
        ec_total = concrete + steel + timber
        values = [concrete, steel, timber]
        # yummy yummy pie
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])

        return ice_concrete, ice_steel, ice_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/val), dcc.Graph(figure=fig)
