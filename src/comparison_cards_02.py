import base64
import datetime
import io
import math

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate

from src import (epic_options, greenbook_options, ice_options, material_table,
                 uploader)
from src.comparison_cards_01 import epic_df, gb_df

card02 = html.Div([
    dcc.Upload(
        id='card2_upload_data',
        children=html.Div([
            dmc.Tooltip(
                label="fade",
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

        ]),
        className='position-absolute translate-middle',
        style={
            'zIndex':'5', 
            'left':'98%', 
            'top':'0%'
        },
    # Allow multiple files to be uploaded
    multiple=True
    ),
    html.Div(id='card2_output'),
    html.Div(id="card2_contents")
])


@callback(Output('card2_output', 'children'),
              Input('card2_upload_data', 'contents'),
              State('card2_upload_data', 'filename'),
              State('card2_upload_data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            uploader.parse_contents(c, n, d, "card2_temp_store") for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(
Output('card2_contents', 'children'),
Input('card02_store', 'modified_timestamp'), 
State('card02_store', 'data'),
)
def card2_content_update(mts, data,):
    if data is None or mts is None:
        return html.P("Upload another project to compare with!", className="display-6 text-center fs-4")
    else:
        df = pd.read_json(data, orient="split")
        _df = df.groupby(by=['Building Materials (All)'], as_index=False).sum()
        _df = _df.filter(items=['Building Materials (All)', 'Mass', 'Volume (Net)'])

        return html.Div([
            html.H3("Comparison 2", className="display-5 my-3"),
            dmc.Divider(class_name="mb-3"),
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
            html.H5(["GFA in m", html.Sup(2)]),
            # input for gfa calculation
            dbc.Input(
                id="comp_card2_gfa",
                placeholder="GFA?",
                className="w-25",
                type="number",
                debounce=True,
                persistence= True,
                persistence_type="session",
                required=True
            ),
            dmc.Divider(class_name="my-3"),

# ----------- Green book comparison for CARD 2 ----------            
            html.H3("Green Book DB", className="mb-3"),
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(
                            options=greenbook_options.concrete_options, 
                            id="gb_card2_concrete", 
                            value="Concrete 50 MPa ", 
                            persistence=True, 
                            persistence_type="session"
                            ),
                        html.Div(id="gb_card2_concrete_val"),
                        dbc.Select(
                            options=greenbook_options.steel_options, 
                            id="gb_card2_steel", 
                            value="Steel Universal Section",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="gb_card2_steel_val"),
                        dbc.Select(
                            options=greenbook_options.timber_options, 
                            id="gb_card2_timber", 
                            value="Glue-Laminated Timber (Glu-lam)",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="gb_card2_timber_val"),
                    ),
                    label="Green Book DB Material Options",
                ),
            ], 
            class_name="py-3",
            ),
            dbc.Row([
                dbc.Col([
                    html.Div(id="gb_card2_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.Div(id="gb_card2_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ]),




        ]) # END OF CARD 2 LIST DON'T DELETE

@callback(
Output('gb_card2_total', 'children'),
Output('gb_card2_gfa', 'children'),
Output('gb_card2_concrete_val', 'children'),
Output('gb_card2_steel_val', 'children'),
Output('gb_card2_timber_val', 'children'),

Input('comp_card2_gfa', 'value'), 
Input('gb_card2_concrete', 'value'),
Input('gb_card2_steel', 'value'),
Input('gb_card2_timber', 'value'),

State('card02_store', "data")
)
def card2_total_gfa_update(val, conc_val, steel_val, timber_val, data):
    if val is None:
        unknown_total_gfa = html.H3(["Unknown", html.P("Input GFA above")])
        unknown = html.P("Unknown")
        return unknown_total_gfa, unknown_total_gfa, unknown, unknown, unknown
    else:
        df = pd.read_json(data, orient="split")

        #iron ice calculation
        conc_ec = gb_df.loc[gb_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        #iron ice calculation
        steel_ec = gb_df.loc[gb_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        #wood ice calculation
        timber_ec = gb_df.loc[gb_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()
        
        gb_concrete = html.P("{:,.2f}".format((concrete := conc_ec * structure_concrete)))
        gb_steel = html.P("{:,.2f}".format((steel := steel_ec * structure_steel)))
        gb_timber = html.P("{:,.2f}".format((timber := timber_ec * structure_timber)))

        labels = [conc_val, steel_val, timber_val]
        total = concrete + steel + timber
        total_per_m2 = total/float(val)
        values_pie = [concrete, steel, timber]

        # Generate Pie graph
        fig = go.Figure(data=[go.Pie(labels=labels, values=values_pie, hole=0.5)])

        return html.H3(total), html.H3(np.around(total_per_m2, 2)), gb_concrete, gb_steel, gb_timber



