# @TODO: 
# * I think it's better if we used pattern matching for the 3 diffrent card table menu thingy
# keeps the code smaller and efficient(?). 
# * I also think we can refactor the cards into a functions... not sure if callbacks like it
# or if it would make things more complicated. cuz you gotta consider different units of different
# databases... at the moment everything is good. (till it's not)


import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config import config, graph_colors
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from pages.dashboard import gfa_calc

from src import (analysis_more_info, epic_options, greenbook_options,
                 ice_options)

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

# ------------------------------Green Book Card--------------------------------------
table_header = [html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))]
row1 = html.Tr([
    html.Td(
        dbc.Select(options=greenbook_options.concrete_options, id="row_concrete", value="Concrete 50 MPa ")
    ), 
    html.Td(
        html.Div(id="row_concrete_value",)
    )
    ])
row2 = html.Tr([
    html.Td(
        dbc.Select(options=greenbook_options.steel_options, id="row_steel", value="Steel Universal Section")
    ), 
    html.Td(id="row_steel_value")
    ])
row3 = html.Tr([
    html.Td(dbc.Select(options=greenbook_options.timber_options, id="row_timber", value="Glue-Laminated Timber (Glu-lam)")), 
    html.Td(id="row_timber_value")
    ])
table_body = [html.Tbody([row1, row2, row3])]

greenbook_card = dbc.Card([
    html.H3("Green Book Database", className="mb-3 display-5"),
    html.Hr(),
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(id="gb_analysis_total", className="text-center")),
                dbc.Col(html.Div(id="gb_analysis_gfa", className="text-center"))
            ], className="mb-3"),
            dbc.Table(
                table_header + table_body, 
                striped=True, 
                bordered=True, 
                hover=True,
                ),
        ], style = {"width": "75%"}),
        dcc.Graph(id="gb_pie", config=config),

    ], 
    className="hstack",
    ),
    dmc.Accordion([
        dmc.AccordionItem(
            children=analysis_more_info.gb_more_info, 
            label="More Information and Analysis")
    ], 
    id="gb_accordion",
    state={"0": False})
    ],
class_name="my-5 p-4 shadow"
)


@callback(
Output('row_concrete_value', 'children'),
Output('row_steel_value', 'children'),
Output('row_timber_value', 'children'),
Output('gb_analysis_total', 'children'),
Output('gb_analysis_gfa', 'children'),

Input('row_concrete', 'value'), 
Input('row_steel', 'value'),
Input('row_timber', 'value'), 

State('main_store', 'data'),
State('gfa_store', 'data')
)
def gb_row_update(concrete, steel, timber, data, gfa):
    if concrete is not None and steel is not None and timber is not None:
        df = pd.read_json(data, orient="split")
        conc_ec = gb_df.loc[gb_df["Sub Category"] == concrete, "Embodied Carbon"] 
        steel_ec = gb_df.loc[gb_df["Sub Category"] == steel, "Embodied Carbon"] 
        timber_ec = gb_df.loc[gb_df["Sub Category"] == timber, "Embodied Carbon"] 

        # structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        # structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        # structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()

        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        
        # for index, row in df.iterrows():
        #     if re.search(row["Building Materials (All)"], "concrete", re.IGNORECASE):
        #         structure_concrete = row["Volume (Net)"]
        #     elif re.search(row["Building Materials (All)"], "steel", re.IGNORECASE):
        #         structure_steel = row["Mass"]
        #     elif re.search(row["Building Materials (All)"], "timber", re.IGNORECASE):
        #         structure_timber = row["Volume (Net)"]

        for index, row in df.iterrows():
            print(row["Building Materials (All)"])
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                print("concrete was found")
                structure_concrete = row["Volume (Net)"]
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                print("steel was found")
                structure_steel = row["Mass"]
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                print("timber was found")
                structure_timber = row["Volume (Net)"]

          
        
        # @TODO: MAYBE USE DATACLASSES FOR THIS?
        # current process looks for specific building materials and sums them up.
        # however the better way for flexility is using regex to find certain patterns
        # for instance rather than "STEEL - STRUCTURAL" we can look for "steel". 

        # this allows for flexibility of users to name "Building Materials" as any name they want.
        

        # ec_concrete = conc_ec * structure_concrete
        # ec_steel = steel_ec * structure_steel
        # ec_timber = timber_ec * structure_timber

        ec_concrete = conc_ec * 1
        ec_steel = steel_ec * 1
        ec_timber = timber_ec * 1

        total_ec = ec_concrete.tolist()[0] + ec_steel.tolist()[0] + ec_timber.tolist()[0]
        gfa_ = total_ec/gfa

        total = html.Div([
            html.H3("{:,}".format(np.around(total_ec))),
            html.P([html.Span("kgCO2e ", className="fs-4"),"Total EC"])
        ], style={"display": "block"})

        gfa_calc = html.Div([
            html.H3(["{:,} ".format(np.around(gfa_))]),
            html.P([html.Span("kgCO2e/m² ", className="fs-4"),"EC per m²"])
        ], style={"display": "block"})

        return html.P(ec_concrete.map("{:,.2f}".format), className="text-center"), \
            html.P(ec_steel.map("{:,.2f}".format), className="text-center"), \
            html.P(ec_timber.map("{:,.2f}".format), className="text-center"), total, gfa_calc
    else: raise PreventUpdate

@callback(
Output('gb_pie', 'figure'),
[
    Input('row_concrete', 'value'),
    Input('row_steel', 'value'),
    Input('row_timber', 'value')
], 
State('main_store', 'data')
)
def definition(cv, sv, tv, data):
    if all( i != None for i in [cv, sv, tv]):
        df = pd.read_json(data, orient="split")
        ec = [
            gb_df.loc[gb_df["Sub Category"] == cv, "Embodied Carbon"].to_numpy()[0],
            gb_df.loc[gb_df["Sub Category"] == sv, "Embodied Carbon"].to_numpy()[0],
            gb_df.loc[gb_df["Sub Category"] == tv, "Embodied Carbon"].to_numpy()[0]
        ]
        structure = [
            df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum(),
            df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum(),
            df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()
        ]

        ec_val = [x*y for x, y in zip(ec, structure)] #yup still don't understand list comprehension <( ￣^￣)...
        labels = [cv, sv, tv]

        fig = go.Figure(data=[go.Pie(labels=labels, values=ec_val, hole=0.5)])
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            annotations=[ dict(text='Green Book', x=0.5, y=0.5, font_size=16, showarrow=False)] )
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        return fig
    else: 
        ec_val = [50,50,50]
        labels = [cv, sv, tv]
        fig = go.Figure(data=[go.Pie(labels=labels, values=ec_val, hole=.3)])
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        return fig

# ------------------------------EPiC Card--------------------------------------
table_header = [html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))]
row1 = html.Tr([
    html.Td(
        dbc.Select(options=epic_options.concrete_option, id="epic_row_concrete", value="Concrete 50 MPa")
    ), 
    html.Td(
        html.Div(id="epic_row_concrete_value",)
    )
    ])
row2 = html.Tr([
    html.Td(
        dbc.Select(options=epic_options.steel_options, id="epic_row_steel", value="Steel structural steel section")
    ), 
    html.Td(id="epic_row_steel_value")
    ])
row3 = html.Tr([
    html.Td(dbc.Select(options=epic_options.timber_option, id="epic_row_timber", value="Glued laminated timber (glulam)")), 
    html.Td(id="epic_row_timber_value")
    ])
table_body = [html.Tbody([row1, row2, row3])]

epic_card = dbc.Card([
    html.H3("EPiC Database", className="mb-3 display-5"),
    html.Hr(),
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(id="epic_analysis_total", className="text-center")),
                dbc.Col(html.Div(id="epic_analysis_gfa", className="text-center"))
            ], className="mb-3"),
            dbc.Table(
                table_header + table_body, 
                striped=True, 
                bordered=True, 
                hover=True,
            ),
        ], style = {"width": "75%"}),        

        dcc.Graph(id="epic_pie", config=config),
    ], className="hstack"),
    dmc.Accordion([
        dmc.AccordionItem(
            children=analysis_more_info.epic_more_info, 
            label="More Information and Analysis")
    ], 
    id="gb_accordion",
    state={"0": False})
],
class_name="my-5 p-4 shadow"
)


@callback(
Output('epic_row_concrete_value', 'children'),
Output('epic_row_steel_value', 'children'),
Output('epic_row_timber_value', 'children'),
Output('epic_analysis_total', 'children'),
Output('epic_analysis_gfa', 'children'),

Input('epic_row_concrete', 'value'), 
Input('epic_row_steel', 'value'),
Input('epic_row_timber', 'value'), 

State('main_store', 'data'),
State('gfa_store', 'data')
)
def epic_row_update(concrete, steel, timber, data, gfa):
    if concrete is not None and steel is not None and timber is not None:
        df = pd.read_json(data, orient="split")
        conc_ec = epic_df.loc[epic_df["Sub Category"] == concrete, "Embodied Carbon"] 
        steel_ec = epic_df.loc[epic_df["Sub Category"] == steel, "Embodied Carbon"] 
        timber_ec = epic_df.loc[epic_df["Sub Category"] == timber, "Embodied Carbon"] 

        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()

        ec_concrete = np.around(conc_ec * structure_concrete, 2)
        ec_steel = np.around(steel_ec * structure_steel,2 )
        ec_timber = np.around(timber_ec * structure_timber, 2)

        total_ec = ec_concrete.tolist()[0] + ec_steel.tolist()[0] + ec_timber.tolist()[0]
        gfa_ = total_ec/gfa

        total = html.Div([
            html.H3("{:,}".format(np.around(total_ec))),
            html.P([html.Span("kgCO2e ", className="fs-4"),"Total EC"])
        ], style={"display": "block"})

        gfa_calc = html.Div([
            html.H3(["{:,} ".format(np.around(gfa_))]),
            html.P([html.Span("kgCO2e/m² ", className="fs-4"),"EC per m²"])
        ], style={"display": "block"})


        return html.P(ec_concrete.map("{:,}".format), className="text-center"), \
            html.P(ec_steel.map("{:,}".format), className="text-center"), \
            html.P(ec_timber.map("{:,}".format), className="text-center"), total, gfa_calc
    else: raise PreventUpdate

@callback(
Output('epic_pie', 'figure'),
[
    Input('epic_row_concrete', 'value'),
    Input('epic_row_steel', 'value'),
    Input('epic_row_timber', 'value')
], 
State('main_store', 'data')
)
def definition(epic_cv, epic_sv, epic_tv, data):
    if all( i != None for i in [epic_cv, epic_sv, epic_tv]):
        df = pd.read_json(data, orient="split")
        ec = [
            epic_df.loc[epic_df["Sub Category"] == epic_cv, "Embodied Carbon"].to_numpy()[0],
            epic_df.loc[epic_df["Sub Category"] == epic_sv, "Embodied Carbon"].to_numpy()[0],
            epic_df.loc[epic_df["Sub Category"] == epic_tv, "Embodied Carbon"].to_numpy()[0]
        ]
        structure = [
            df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum(),
            df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum(),
            df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()
        ]

        ec_val = [x*y for x, y in zip(ec, structure)]
        labels = [epic_cv, epic_sv, epic_tv]

        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=ec_val, 
            hole=0.5,
            )])
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            annotations=[ dict(text='EPiC', x=0.5, y=0.5, font_size=16, showarrow=False)] )
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        return fig
    else: 
        ec_val = [50,50,50]
        labels = [epic_cv, epic_sv, epic_tv]
        fig = go.Figure(data=[go.Pie(labels=labels, values=ec_val, hole=.3)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value',marker=dict(colors=graph_colors))
        return fig

# ------------------------------ice database Card--------------------------------------

table_header = [html.Thead(html.Tr([html.Th("Material"), html.Th("Embodied Carbon (kgCO2e)")]))]
row1 = html.Tr([
    html.Td(
        dbc.Select(options=ice_options.concrete_options, id="ice_row_concrete", value="Concrete 40 MPa")
    ), 
    html.Td(
        html.Div(id="ice_row_concrete_value",)
    )
    ])
row2 = html.Tr([
    html.Td(
        dbc.Select(options=ice_options.steel_options, id="ice_row_steel", value="Steel Section")
    ), 
    html.Td(id="ice_row_steel_value")
    ])
row3 = html.Tr([
    html.Td(dbc.Select(options=ice_options.timber_options, id="ice_row_timber", value="Timber Glulam")), 
    html.Td(id="ice_row_timber_value")
    ])
table_body = [html.Tbody([row1, row2, row3])]

ice_card = dbc.Card([
    html.H3("ICE Database", className="mb-3 display-5"),
    html.Hr(),
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(id="ice_analysis_total", className="text-center")),
                dbc.Col(html.Div(id="ice_analysis_gfa", className="text-center"))
            ], className="mb-3"),
            dbc.Table(
                table_header + table_body, 
                striped=True, 
                bordered=True, 
                hover=True,
            ),
        ], style = {"width": "75%"}),

        dcc.Graph(id="ice_pie", config=config),
    ], className="hstack"),
    dmc.Accordion([
        dmc.AccordionItem(
            children=analysis_more_info.ice_more_info, 
            label="More Information and Analysis")
    ], 
    id="gb_accordion",
    state={"0": False})
],
class_name="my-5 p-4 shadow"
)

@callback(
Output('ice_row_concrete_value', 'children'),
Output('ice_row_steel_value', 'children'),
Output('ice_row_timber_value', 'children'),
Output('ice_analysis_total', 'children'),
Output('ice_analysis_gfa', 'children'),

Input('ice_row_concrete', 'value'),
Input('ice_row_steel', 'value'),
Input('ice_row_timber', 'value'), 

State('main_store', 'data'),
State('gfa_store', 'data')
)
def ice_row_update(concrete, steel, timber, data, gfa):
    if concrete is not None and steel is not None and timber is not None:
        df = pd.read_json(data, orient="split")
        conc_ec = ice_df.loc[ice_df["Sub Category"] == concrete, "Embodied Carbon"] 
        steel_ec = ice_df.loc[ice_df["Sub Category"] == steel, "Embodied Carbon"] 
        timber_ec = ice_df.loc[ice_df["Sub Category"] == timber, "Embodied Carbon"] 

        structure_concrete = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum()
        structure_steel = df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum()
        structure_timber = df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Volume (Net)"].sum()

        ec_concrete = np.around(conc_ec * structure_concrete, 2)
        ec_steel = np.around(steel_ec * structure_steel, 2)
        ec_timber = np.around(timber_ec * structure_timber, 2)

        total_ec = ec_concrete.tolist()[0] + ec_steel.tolist()[0] + ec_timber.tolist()[0]
        gfa_ = total_ec/gfa

        total = html.Div([
            html.H3("{:,}".format(np.around(total_ec))),
            html.P([html.Span("kgCO2e ", className="fs-4"),"Total EC"])
        ])

        gfa_calc = html.Div([
            html.H3(["{:,} ".format(np.around(gfa_))]),
            html.P([html.Span("kgCO2e/m² ", className="fs-4"),"EC per m²"])
        ])

        return html.P(ec_concrete.map("{:,}".format), className="text-center"), \
            html.P(ec_steel.map("{:,}".format), className="text-center"), \
            html.P(ec_timber.map("{:,}".format), className="text-center"), total, gfa_calc
    else: raise PreventUpdate
    


@callback(
Output('ice_pie', 'figure'),
[
    Input('ice_row_concrete', 'value'),
    Input('ice_row_steel', 'value'),
    Input('ice_row_timber', 'value')
], 
State('main_store', 'data')
)
def definition(ice_cv, ice_sv, ice_tv, data):
    if all( i != None for i in [ice_cv, ice_sv, ice_tv]):
        df = pd.read_json(data, orient="split")
        ec = [
            ice_df.loc[ice_df["Sub Category"] == ice_cv, "Embodied Carbon"].to_numpy()[0],
            ice_df.loc[ice_df["Sub Category"] == ice_sv, "Embodied Carbon"].to_numpy()[0],
            ice_df.loc[ice_df["Sub Category"] == ice_tv, "Embodied Carbon"].to_numpy()[0]
        ]
        structure = [
            df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].sum(),
            df.loc[df["Building Materials (All)"] == "STEEL - STRUCTURAL", "Mass"].sum(),
            df.loc[df["Building Materials (All)"] == "TIMBER - STRUCTURAL", "Mass"].sum()
        ]

        ec_val = [x*y for x, y in zip(ec, structure)]
        labels = [ice_cv, ice_sv, ice_tv]

        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=ec_val, 
            hole=0.5,
            )])
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            annotations=[ dict(text='ICE', x=0.5, y=0.5, font_size=16, showarrow=False)] )
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        return fig
    else: 
        ec_val = [50,50,50]
        labels = [ice_cv, ice_sv, ice_tv]
        fig = go.Figure(data=[go.Pie(labels=labels, values=ec_val, hole=.3)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value',marker=dict(colors=graph_colors))
        return fig
