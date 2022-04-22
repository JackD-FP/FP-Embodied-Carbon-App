import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config import graph_colors
from dash import Input, Output, State, callback, dcc, html

from src import (epic_options, funcs, greenbook_options, ice_options,
                 material_table, uploader)
from src.comparison_cards_01 import epic_df, gb_df, ice_df

card02 = html.Div([
    dcc.Upload(
        id='card2_upload_data',
        children=html.Div([
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
            uploader.parse_contents(c, n, d, "card2_temp_store", "name_2") for c, n, d in
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
        tmp = _df.select_dtypes(include=['float64'])
        _df.loc[:, tmp.columns] = np.around(tmp,2)
        _df = _df.filter(items=['Building Materials (All)', 'Mass', 'Net Volume'])

        return html.Div([
            html.H3("Comparison 2", className="display-5 my-3"),
            dmc.Divider(class_name="mb-3"),
            html.H3("Structure Schedule"),
            dbc.Table.from_dataframe(_df, striped=True, bordered=True, hover=True),
            html.H5(["GFA in m", html.Sup(2)]),
            # input for gfa calculation
            dbc.Input(
                id="comp_card2_gfa",
                #placeholder="GFA?",
                value=5000,
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
                    label="Green Book DB Material Options ▼",
                ),
            ], 
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
            ], className="my-5"),
            html.Div(id="card2_gb_pie"),
            dmc.Divider(class_name="my-4"),

# ----------- EPiC comparison for CARD 2 ----------    
            html.H3("EPiC DB", className="mb-3"),
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(
                            options=epic_options.concrete_option, 
                            id="epic_card2_concrete", 
                            value="Concrete 50 MPa", 
                            persistence=True, 
                            persistence_type="session"
                            ),
                        html.Div(id="epic_card2_concrete_val"),
                        dbc.Select(
                            options=epic_options.steel_options, 
                            id="epic_card2_steel", 
                            value="Steel structural steel section",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="epic_card2_steel_val"),
                        dbc.Select(
                            options=epic_options.timber_option, 
                            id="epic_card2_timber", 
                            value="Glued laminated timber (glulam)",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="epic_card2_timber_val"),
                    ),
                    label="EPiC DB Material Options ▼",
                ),
            ], 
            ),
            dbc.Row([
                dbc.Col([
                    html.Div(id="epic_card2_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.Div(id="epic_card2_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], className="my-5"),
            html.Div(id="card2_epic_pie"),
            dmc.Divider(class_name="my-3"),

# ----------- ICE comparison for CARD 2 ----------    
            html.H3("ICE DB", className="mb-3"),
            dmc.Accordion([
                dmc.AccordionItem(
                    material_table.table_gen(
                        dbc.Select(
                            options=ice_options.concrete_options, 
                            id="ice_card2_concrete", 
                            value="Concrete 40 MPa", 
                            persistence=True, 
                            persistence_type="session"
                            ),
                        html.Div(id="ice_card2_concrete_val"),
                        dbc.Select(
                            options=ice_options.steel_options, 
                            id="ice_card2_steel", 
                            value="Steel Section",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="ice_card2_steel_val"),
                        dbc.Select(
                            options=ice_options.timber_options, 
                            id="ice_card2_timber", 
                            value="Timber Glulam",
                            persistence=True,
                            persistence_type="session"
                            ),
                        html.Div(id="ice_card2_timber_val"),
                    ),
                    label="ICE DB Material Options ▼",
                ),
            ], 
            ),
            dbc.Row([
                dbc.Col([
                    html.Div(id="ice_card2_total", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"], className="text-center")
                ]),
                dbc.Col([
                    html.Div(id="ice_card2_gfa", className="text-center"),
                    html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4"), " EC per m", html.Sup(2)], className="text-center")
                ]),
            ], className="my-4"),
            html.Div(id="card2_ice_pie"),
        ]) # END OF CARD 2 LIST DON'T DELETE


# Green Book callback
@callback(
Output('gb_card2_total', 'children'),
Output('gb_card2_gfa', 'children'),
Output('gb_card2_concrete_val', 'children'),
Output('gb_card2_steel_val', 'children'),
Output('gb_card2_timber_val', 'children'),
Output('card2_gb_pie', 'children'),

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
        df_grouped = df.groupby(by=["Building Materials (All)"], as_index=False).sum()

        structure_concrete, structure_steel, structure_timber = funcs.find2(df_grouped, False)

        conc_ec = gb_df.loc[gb_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        steel_ec = gb_df.loc[gb_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        timber_ec = gb_df.loc[gb_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]


        gb_concrete = html.P("{:,.2f}".format((concrete := conc_ec * sum(structure_concrete))))
        gb_steel = html.P("{:,.2f}".format((steel := steel_ec * sum(structure_steel))))
        gb_timber = html.P("{:,.2f}".format((timber := timber_ec * sum(structure_timber))))

        labels = [conc_val, steel_val, timber_val]
        total = concrete + steel + timber
        total_per_m2 = total/float(val)
        values_pie = [concrete, steel, timber]

        # Generate Pie graph
        fig = go.Figure(data=[go.Pie(labels=labels, values=values_pie, hole=0.5)])
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        pie_child = dcc.Graph(figure=fig)

        return html.H3("{:,}".format(np.around(total,2))), \
            html.H3("{:,}".format(np.around(total_per_m2, 2))), \
            gb_concrete, gb_steel, gb_timber, pie_child



# Epic callback
@callback(
Output('epic_card2_total', 'children'),
Output('epic_card2_gfa', 'children'),
Output('epic_card2_concrete_val', 'children'),
Output('epic_card2_steel_val', 'children'),
Output('epic_card2_timber_val', 'children'),
Output('card2_epic_pie', 'children'),

Input('comp_card2_gfa', 'value'), 
Input('epic_card2_concrete', 'value'),
Input('epic_card2_steel', 'value'),
Input('epic_card2_timber', 'value'),

State('card02_store', "data")
)
def card2_total_gfa_update(val, conc_val, steel_val, timber_val, data):
    if val is None:
        unknown_total_gfa = html.H3(["Unknown", html.P("Input GFA above")])
        unknown = html.P("Unknown")
        return unknown_total_gfa, unknown_total_gfa, unknown, unknown, unknown
    else:
        df = pd.read_json(data, orient="split")
        df_grouped = df.groupby(by=["Building Materials (All)"], as_index=False).sum()

        structure_concrete, structure_steel, structure_timber = funcs.find2(df_grouped, False)

        #epic ec calculation
        conc_ec = epic_df.loc[epic_df["Sub Category"] == conc_val, "Embodied Carbon"].values[0]
        steel_ec = epic_df.loc[epic_df["Sub Category"] == steel_val, "Embodied Carbon"].values[0]
        timber_ec = epic_df.loc[epic_df["Sub Category"] == timber_val, "Embodied Carbon"].values[0]


        epic_concrete = html.P("{:,.2f}".format((concrete := conc_ec * sum(structure_concrete))))
        epic_steel = html.P("{:,.2f}".format((steel := steel_ec * sum(structure_steel))))
        epic_timber = html.P("{:,.2f}".format((timber := timber_ec * sum(structure_timber))))

        labels = [conc_val, steel_val, timber_val]
        total = concrete + steel + timber
        total_per_m2 = total/float(val)
        values_pie = [concrete, steel, timber]

        # Generate Pie graph
        fig = go.Figure(data=[go.Pie(labels=labels, values=values_pie, hole=0.5)])
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        pie_child = dcc.Graph(figure=fig)

        return html.H3("{:,}".format(np.around(total,2))), html.H3("{:,}".format(np.around(total_per_m2, 2))), epic_concrete, epic_steel, epic_timber, pie_child

# ice callback
@callback(
Output('ice_card2_total', 'children'),
Output('ice_card2_gfa', 'children'),
Output('ice_card2_concrete_val', 'children'),
Output('ice_card2_steel_val', 'children'),
Output('ice_card2_timber_val', 'children'),
Output('card2_ice_pie', 'children'),

Input('comp_card2_gfa', 'value'), 
Input('ice_card2_concrete', 'value'),
Input('ice_card2_steel', 'value'),
Input('ice_card2_timber', 'value'),

State('card02_store', "data")
)
def card2_total_gfa_update(val, conc_val, steel_val, timber_val, data):
    if val is None:
        unknown_total_gfa = html.H3(["Unknown", html.P("Input GFA above")])
        unknown = html.P("Unknown")
        return unknown_total_gfa, unknown_total_gfa, unknown, unknown, unknown
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
        total = concrete + steel + timber
        total_per_m2 = total/float(val)
        values_pie = [concrete, steel, timber]

        # Generate Pie graph
        fig = go.Figure(data=[go.Pie(labels=labels, values=values_pie, hole=0.5)])
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        pie_child = dcc.Graph(figure=fig)

        return html.H3("{:,}".format(np.around(total))), html.H3("{:,}".format(np.around(total_per_m2, 2))), ice_concrete, ice_steel, ice_timber, pie_child
