from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import  plotly.graph_objects as go
import pandas as pd
import numpy as np

from src import material_table, greenbook_options

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
            html.Div(id="gb_bars")          
            
        ]
        return table_out 

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

        #print(np.around((conc_ec * structure_concrete), 2))
        gb_concrete = html.P("{:,.2f}".format((concrete := conc_ec * structure_concrete)))
        gb_steel = html.P("{:,.2f}".format((steel := steel_ec * structure_steel)))
        gb_timber = html.P("{:,.2f}".format((timber := timber_ec * structure_timber)))

        labels = [conc_val, steel_val, timber_val]
        ec_total = concrete + steel + timber
        values = [concrete, steel, timber]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        return gb_concrete, gb_steel, gb_timber, "{:,.2f}".format(ec_total), "{:,.2f}".format(ec_total/val), dcc.Graph(figure=fig)