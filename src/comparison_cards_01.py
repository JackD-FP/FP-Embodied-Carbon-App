# This generates cards for the comparison page
#   - cards: cards01, cards02, cards03
#   - each cards has the ability to generate analysis from greenbook, epic and ice

# TODO
# - add bar chart in card 01 for GB, epic and ice
# - create upload feature for cards 02 and 03

import re
from operator import index

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from config import graph_colors
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
import numpy as np

from src import (epic_options, funcs, greenbook_options, ice_options,
                 material_table)

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

card01 = html.Div([
    html.Div(id='card01_table')
])

@callback(
Output('card01_table', 'children'), 
Input('gfa_store', 'modified_timestamp'),
State('main_store', 'data'),
State('gfa_store', 'data'),
)
def update_div(gfa_mts, main_data, gfa_data ):
    if main_data is None: 
        raise PreventUpdate
    else:
        df = pd.read_json(main_data, orient="split")
        _df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        # rounds the values to 2 decimal places
        tmp = _df.select_dtypes(include=['float64'])
        _df.loc[:, tmp.columns] = np.around(tmp,2)
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
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(options=greenbook_options.concrete_options, id="gb_comp_concrete", value="Concrete 50 MPa "),
                        html.P(id="gb_comp_concrete_val"),
                        dbc.Select(options=greenbook_options.steel_options, id="gb_comp_steel", value="Steel Universal Section"),
                        html.P(id="gb_comp_steel_val"),
                        dbc.Select(options=greenbook_options.timber_options, id="gb_comp_timber", value="Glue-Laminated Timber (Glu-lam)"),
                        html.P(id="gb_comp_timber_val"),
                    ),
                    label="Green Book DB Material Options ▼",
                ),
            ]),
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
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(options=epic_options.concrete_option, id="epic_comp_concrete", value="Concrete 50 MPa"),
                        html.P(id="epic_comp_concrete_val"),
                        dbc.Select(options=epic_options.steel_options, id="epic_comp_steel", value="Steel structural steel section"),
                        html.P(id="epic_comp_steel_val"),
                        dbc.Select(options=epic_options.timber_option, id="epic_comp_timber", value="Glued laminated timber (glulam)"),
                        html.P(id="epic_comp_timber_val"),
                    ),
                    label="EPiC DB Material Options ▼",
                ),
            ]),
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
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(options=ice_options.concrete_options, id="ice_comp_concrete", value="Concrete 40 MPa"),
                        html.P(id="ice_comp_concrete_val"),
                        dbc.Select(options=ice_options.steel_options, id="ice_comp_steel", value="Steel Section"),
                        html.P(id="ice_comp_steel_val"),
                        dbc.Select(options=ice_options.timber_options, id="ice_comp_timber", value="Timber Glulam"),
                        html.P(id="ice_comp_timber_val"),
                    ),
                    label="ICE DB Material Options ▼",
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3(id="ice_comp_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.H3(id="ice_comp_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], class_name="my-4"),
            html.Div(id="ice_pie"),

        ]
        return table_out 
'''
    @TODO: refactor the code below to be one callback function
    There is a lot of repetition in these callbacks. There is a possibility to refactor this into a callback. 
'''
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
        if val is None: 
            raise PreventUpdate
        else:
            df = pd.read_json(data, orient="split")
            df_grouped = df.groupby(by=["Building Materials (All)"], as_index=False).sum()

            structure_concrete, structure_steel, structure_timber = funcs.find2(df_grouped, False)


            # gb EC calculation
            conc_ec = gb_df.loc[gb_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
            steel_ec = gb_df.loc[gb_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
            timber_ec = gb_df.loc[gb_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]


            gb_concrete = html.P("{:,.2f}".format((concrete := conc_ec * sum(structure_concrete))))
            gb_steel = html.P("{:,.2f}".format((steel := steel_ec * sum(structure_steel))))
            gb_timber = html.P("{:,.2f}".format((timber := timber_ec * sum(structure_timber))))

            labels = [conc_val, steel_val, timber_val]
            ec_total = concrete + steel + timber
            values = [concrete, steel, timber]
            # yummy yummy pie
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
            fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
            
            return gb_concrete, gb_steel, gb_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/float(val)), dcc.Graph(figure=fig)


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
        if val is None:
            raise PreventUpdate
        else:
            df = pd.read_json(data, orient="split")
            df_grouped = df.groupby(by=["Building Materials (All)"], as_index=False).sum()

            structure_concrete, structure_steel, structure_timber = funcs.find2(df_grouped, False)

            # epic EC calculation
            conc_ec = epic_df.loc[epic_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
            steel_ec = epic_df.loc[epic_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
            timber_ec = epic_df.loc[epic_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
            
            epic_concrete = html.P("{:,.2f}".format((concrete := conc_ec * sum(structure_concrete))))
            epic_steel = html.P("{:,.2f}".format((steel := steel_ec * sum(structure_steel))))
            epic_timber = html.P("{:,.2f}".format((timber := timber_ec * sum(structure_timber))))

            labels = [conc_val, steel_val, timber_val]
            ec_total = concrete + steel + timber
            values = [concrete, steel, timber]
            # yummy yummy pie
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
            fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))

            return epic_concrete, epic_steel, epic_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/float(val)), dcc.Graph(figure=fig)


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
        if val is None:
            raise PreventUpdate
        else:  
            df = pd.read_json(data, orient="split")
            df_grouped = df.groupby(by=["Building Materials (All)"], as_index=False).sum()

            structure_concrete, structure_steel, structure_timber = funcs.find2(df_grouped, True)

            # ice EC calculation
            conc_ec = ice_df.loc[ice_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
            steel_ec = ice_df.loc[ice_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
            timber_ec = ice_df.loc[ice_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
            
            ice_concrete = html.P("{:,.2f}".format((concrete := conc_ec * sum(structure_concrete))))
            ice_steel = html.P("{:,.2f}".format((steel := steel_ec * sum(structure_steel))))
            ice_timber = html.P("{:,.2f}".format((timber := timber_ec * sum(structure_timber))))

            labels = [conc_val, steel_val, timber_val]
            ec_total = concrete + steel + timber
            values = [concrete, steel, timber]
            # yummy yummy pie
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
            fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))

            return ice_concrete, ice_steel, ice_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/float(val)), dcc.Graph(figure=fig)

