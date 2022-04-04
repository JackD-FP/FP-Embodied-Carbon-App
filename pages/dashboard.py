import base64
import datetime
import io
import math
import re
from pydoc import classname

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import openpyxl  # just so excel upload works
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from index import app, config
from plotly.subplots import make_subplots
from src import building_type_option, db_loader, uploader

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

graph_colors = ['#5463FF', '#FFC300', '#FF1818'] # graphing colours 

layout = html.Div([
    html.H1("Dashboard", className="display-2 mb-5 "),
    html.Hr(),
    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
        Curabitur scelerisque a eros sit amet egestas. Maecenas eget erat mollis, \
        molestie neque non, tincidunt elit. Nam maximus ex nec neque blandit semper. \
        Morbi ut sagittis velit, quis lacinia turpis. Proin nisl elit, venenatis et odio et, \
        egestas scelerisque eros. Nulla facilisi. Class aptent taciti sociosqu ad litora torquent per conubia nostra,\
        per inceptos himenaeos. Suspendisse faucibus libero vitae auctor faucibus. Duis at diam vel leo euismod pretium. \
        Praesent quis neque a metus pulvinar fermentum lacinia et purus. \
        Nulla egestas elit eros, ut venenatis ex sodales sit amet. Ut non eros eleifend.",
        ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            dbc.Button([
                html.I(className="bi bi-upload", style={"width":"2rem"}),
                html.P("Drag and Drop or Schedule File")
                ], 
            color="light",
            className = "align-center position-absolute top-50 start-50 translate-middle w-100 h-100",
            id="upload_btn"),
        ], 
        id='uploader_ui',
        style = {"height": "10rem", "width": "50%", "margin": "auto"},
        ),
        style={
            'height': '10rem',
            'width': '50%',
            'lineHeight': '60px',
            'textAlign': 'center',
            'margin': 'auto',
            'marginTop': '2rem',
        },
        className = 'text-center mb-5 border border-2 rounded-3 shadow-sm bg-light',
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id="display-table"),    
    html.Div(id="dashboard_graph"),     # could just check but idk ceebs not elegant(?)...no thing is elegant (╯▔皿▔)╯
])


@callback(Output('display-table', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            uploader.parse_contents(c, n, d, "temp-df-store") for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def em_calc(df):
    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() # create consolidated df
    #materials = []
    volumes = df["Volume (Net)"].tolist()
    df_mat = df["Building Materials (All)"].tolist()
    mass = df["Mass"].tolist()
    gb_embodied_carbon = []
    epic_embodied_carbon = []
    ice_embodied_carbon = []

    for i, mat in enumerate(df_mat):
        # if mat == "CONCRETE - IN-SITU":
        if re.search("concrete", mat, re.IGNORECASE):
            gb_embodied_carbon.append(volumes[i]*643) #Concrete 50 MPa || Green Book
            epic_embodied_carbon.append(volumes[i]*600) #Concrete 40 MPa || Epic 
            ice_embodied_carbon.append(volumes[i]*413.4943) # Concrete 50 MPa || Ice
        # elif mat == "STEEL - STRUCTURAL":
        elif re.search("steel", mat, re.IGNORECASE):
            gb_embodied_carbon.append(mass[i]*2.9) #Steel Universal Section || Green Book
            epic_embodied_carbon.append(mass[i]*2.9) #Steel structural steel section || Epic  
            ice_embodied_carbon.append(mass[i]*1.55) # steel Section|| Ice
        # elif mat == "TIMBER - STRUCTURAL":
        elif re.search("timber", mat, re.IGNORECASE):
            gb_embodied_carbon.append(volumes[i]*718) #Glue-Laminated Timber (Glu-lam) || Green Book
            epic_embodied_carbon.append(volumes[i]*1718) #Glued laminated timber (glulam) || Epic 
            ice_embodied_carbon.append(mass[i]*0.51) # Timber Gluelam || Ice
        else: # if all else fail assume concrete
            gb_embodied_carbon.append(volumes[i]*643) #Wood || Green Book
            epic_embodied_carbon.append(volumes[i]*600) #Wood || Epic
            ice_embodied_carbon.append(volumes[i]*413.4943) # Wood || Ice

        # ADD OTHER MATERIALS LIKE ALUMINIUM AND BRICK!!! (╯‵□′)╯︵┻━┻
        # Also i think it's better if we access dataframe.loc instead of a const
        # like look for the right material type or something.
        
    return np.around(gb_embodied_carbon,2), np.around(epic_embodied_carbon, 2), np.around(ice_embodied_carbon, 2)

def percent_check_return(lo, hi):
    if hi == lo:
        return "Lowest total EC"
    else: 
        sub = (hi-lo)*100
        return "+{}% more than lowest".format(np.around(sub/hi, 2))

def percent_calc(lo, hi):
    sub = (hi-lo)*100
    return int(sub/hi)


@callback(
Output('dashboard_graph', 'children'),
[Input('main_store', 'data')],)
def make_graphs(data):
    if data is None:
        raise PreventUpdate
    elif data is not None:
        df_o = pd.read_json(data, orient="split") 
        gb_ec, epic_ec, ice_ec = em_calc(df_o) # makes df for greenbook db

        df = df_o.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        df_mat = df["Building Materials (All)"].tolist()
        # df_ec = df["Embodied Carbon"].tolist() 

        embodied_carbon_dict = { 
            "Materials" : df_mat , 
            # "Archicad (kgCO2e)" : df_ec,
            "Green Book (kgCO2e)" : gb_ec, 
            "EPiC EC (kgCO2e)": epic_ec, 
            "ICE EC (kgCO2e)": ice_ec
            }
        total_dict = { #lol u a total dict
            "Materials" : "TOTALS", 
            #"Archicad (kgCO2e)" : (archicad_sum := sum(df_ec)),
            "Green Book (kgCO2e)" :(gb_sum := sum(gb_ec)), 
            "EPiC EC (kgCO2e)": (epic_sum := sum(epic_ec)), 
            "ICE EC (kgCO2e)": (ice_sum := sum(ice_ec))
        }

        ec_df = pd.DataFrame(embodied_carbon_dict)
        #ec_df = ec_df.append(total_dict, ignore_index=True)

        #ec_df.loc[:,"Archicad (kgCO2e)"] = ec_df["Archicad (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"Green Book (kgCO2e)"] = ec_df["Green Book (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"EPiC EC (kgCO2e)"] = ec_df["EPiC EC (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"ICE EC (kgCO2e)"] = ec_df["ICE EC (kgCO2e)"].map('{:,.2f}'.format)

        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]])
        #subplot for archicad
        # fig.add_trace(go.Pie(labels=df_mat, values=df_ec, name="Archicad", hole=0.5, scalegroup="dashboard_pie"),
        #       1, 1)
        #subplot for greenbook
        fig.add_trace(go.Pie(labels=df_mat, values=gb_ec, name="Green Book DB", hole=0.5, scalegroup="dashboard_pie"),
              1, 1)
        fig.add_trace(go.Pie(labels=df_mat, values=epic_ec, name="EPiC DB", hole=0.5, scalegroup="dashboard_pie"),
              1, 2)
        #subplot for greenbookW
        fig.add_trace(go.Pie(labels=df_mat, values=ice_ec, name="ICE DB", hole=0.5, scalegroup="dashboard_pie"),
              1, 3)
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            # Add annotations in the center of the donut pies.
            annotations=[#dict(text='Archicad', x=0.205, y=0.80, font_size=16, showarrow=False),
                       dict(text='Greenbook', x=0.12, y=0.50, font_size=16, showarrow=False),
                       dict(text='EPiC', x=0.50, y=0.50, font_size=16, showarrow=False),
                       dict(text='ICE', x=0.87, y=0.50, font_size=16, showarrow=False)],
                      )
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        
        #df = df.drop(["Complex Profile", "Structure"], axis=1)
        df = df.drop(["Complex Profile"], axis=1)

        #calc for them progress ring
        # db_total = sum((ec_list := [archicad_sum, gb_sum, epic_sum, ice_sum]))
        db_total = sum((ec_list := [gb_sum, epic_sum, ice_sum]))
        lowest_ec = min(ec_list)
        

        return html.Div([ # consolidated table..
            dash_table.DataTable(
                df_o.to_dict('records'),
                [{'name': i, 'id': i} for i in df_o.columns],
                page_size= 15,
            ),
            dbc.Card([
                html.H3("Structure Summery"),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
            ], class_name="my-5 p-4 shadow"),
            dbc.Card([
                html.H3("Embodied Carbon(EC) calculation"),
                dbc.Table.from_dataframe(ec_df, striped=True, bordered=True, hover=True),
                html.Div([
                    html.H5("Design Name:"),
                    dbc.Input(
                        id="name_input",
                        placeholder="What's the project Name?",
                        className="w-25",
                        type="text",
                        debounce=True,
                        persistence= True,
                        persistence_type="session",
                        required=True
                    ),
                    html.H5("GFA of Design:", className="mt-3"),
                    dbc.Input(
                        id="gfa_input",
                        placeholder="What's the gross floor area (gfa)?",
                        className="w-25",
                        type="number",
                        debounce=True,
                        persistence= True,
                        persistence_type="session",
                        required=True
                    ),
                    html.H5("BCA Building Type:", className="mt-3"),
                    dbc.Select(
                        id='bld_type', 
                        placeholder = "Building Type Class 1, 2, 3... so on",
                        options=building_type_option.building_type,
                        className="w-25",
                    ),
                ], className="my-5"),
                dbc.Container([
                    dbc.Row([
                        # dbc.Col([
                        #     #ArchiCAD Column
                        #     html.H5("Archicad", className="mt-3 mb-4"),   
                        #     html.Div([                         
                        #         dbc.Row([
                        #             dbc.Col(html.H3("{:,}".format(np.around(archicad_sum,2)), className="text-end")),
                        #             dbc.Col(html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"]),className="text-start"),    
                        #         ]),
                        #         html.P(percent_check_return(lowest_ec, archicad_sum), className="text-center"),
                        #     ],id="archicad_ec_check", style={"marginTop":"3rem","marginBottom":"3rem"} ),

                        #     html.Hr(style={
                        #         "marginLeft": "2rem",
                        #         "marginRight": "2rem",
                        #         "color": "d6d3d1"}),

                        #     #GFA calc for archicad
                        #     html.Div([
                        #         dbc.Row([
                        #             dbc.Col([
                        #                 html.H3(id="archicad_gfa",
                        #                 className="text-end"),
                        #             ]),
                        #             dbc.Col([
                        #                 html.P(id="archicad_p",
                        #                 className="text-start"),
                        #             ])
                        #         ]),
                        #         html.P("Design's Benchmark", className="text-center"),
                        #         html.Div([
                        #             html.I(className="bi bi-star-fill mx-2"),
                        #             html.I(className="bi bi-star-fill mx-2"),
                        #             html.I(className="bi bi-star-fill mx-2"),
                        #             html.I(className="bi bi-star-fill mx-2"),
                        #             html.I(className="bi bi-star-fill mx-2"),
                        #             ], className="mt-5 text-center"),
                        #         html.P("Benchmark Score", className="text-center"),
                        #         html.P([
                        #             html.I(className="bi bi-cone-striped"),
                        #             "Benchmark Scores are still under construction",
                        #             html.I(className="bi bi-cone-striped")], 
                        #             className="text-center text-secondary")
                        #     ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                        # ], className="py-5 px-3"),

                        dbc.Col([
                            #Green Book Column
                            html.H5(
                                "Green Book DB", 
                                className="my-4 display-6",
                                style={"marginLeft": "2rem"},
                                ),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(html.H3("{:,}".format(np.around(gb_sum,2)), className="text-end")),
                                    dbc.Col(html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"]),className="text-start"),
                                ]),
                                html.P(percent_check_return(lowest_ec, gb_sum), className="text-center"),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                            html.Hr(style={
                                "marginLeft": "2rem",
                                "marginRight": "2rem",
                                "color": "d6d3d1"}),

                            #GFA calc for green book
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="gb_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P(id="gb_p",
                                        className="text-start"),
                                    ])
                                ]),
                                html.P("Design's Benchmark", className="text-center"),
                                dmc.Tooltip(
                                    label="Based on Green Book Benchmark scores",
                                    withArrow=True,
                                    position="top",
                                    placement="center",
                                    color="dark",
                                    children=[ #@TODO: add working benchmark for green book
                                        html.Div([
                                            html.I(className="bi bi-star-fill mx-2"),
                                            html.I(className="bi bi-star-fill mx-2"),
                                            html.I(className="bi bi-star-fill mx-2"),
                                            html.I(className="bi bi-star-fill mx-2"),
                                            html.I(className="bi bi-star-fill mx-2"),
                                            ], className="mt-5 text-center"),
                                        html.P("Benchmark Score", className="text-center"),
                                    ],
                                    style={"display":"block"}
                                ),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                        ], className="bg-light py-5 px-3"),
                        
                        dbc.Col([
                            #EPiC Column
                            html.H5(
                                "EPIC DB", 
                                className="my-3 display-6",
                                style={"marginLeft": "2rem"},
                                ),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(html.H3("{:,}".format(np.around(epic_sum,2)), className="text-end")),
                                    dbc.Col(html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"]),className="text-start"),
                                ]),
                                html.P(percent_check_return(lowest_ec, epic_sum), className="text-center"),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                            html.Hr(style={
                                "marginLeft": "2rem",
                                "marginRight": "2rem",
                                "color": "d6d3d1"}),

                            #GFA calc for epic
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="epic_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P(id="epic_p",
                                        className="text-start"),
                                    ])
                                ]),
                                html.P("Design's Benchmark", className="text-center"),
                                dmc.Tooltip(
                                    label="No Benchmark scores available for EPIC",
                                    transition="fade",
                                    transitionDuration=300,
                                    transitionTimingFunction="ease",
                                    children=[
                                        html.P("No Benchmark Score", className="text-center mt-5 "),
                                    ],
                                    style={"display":"block"}
                                ),
                                
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                        ], className="py-5 px-3"),

                        dbc.Col([
                            #ICE column epic
                            html.H5("ICE DB", 
                            className="my-4 display-6",
                            style={"marginLeft": "2rem"}),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(html.H3("{:,}".format(np.around(ice_sum,2)), className="text-end")),
                                    dbc.Col(html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e')], className="fs-4"), " Total EC"]),className="text-start")
                                ]),
                                html.P(percent_check_return(lowest_ec, ice_sum), className="text-center"),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                            html.Hr(style={
                                "marginLeft": "2rem",
                                "marginRight": "2rem",
                                "color": "d6d3d1"}),

                            #GFA calc for ice
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="ice_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P(id="ice_p",
                                        className="text-start"),
                                    ])
                                ]), 
                                html.P("Design's Benchmark", className="text-center "),
                                dmc.Tooltip(
                                    label="No Benchmark scores available for ICE",
                                    transition="fade",
                                    transitionDuration=300,
                                    transitionTimingFunction="ease",
                                    children=[
                                        html.P("No Benchmark Score", className="text-center mt-5 "),
                                    ],
                                    style={"display":"block"}
                                ),                        
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),
                        ], className="bg-light py-5 px-3"), 
                    ],className="my-5"),
                ], fluid=True, className="gap-5"),
                dcc.Graph(figure=fig ,style={'height': '75vh'}, className='mt-3',config=config),
            ], class_name="my-5 p-4 shadow"),
        ])


@callback(
# Output('archicad_gfa', 'children'),
# Output('archicad_p', 'children'),
Output('gb_gfa', 'children'),
Output('gb_p', 'children'),
Output('epic_gfa', 'children'),
Output('epic_p', 'children'),
Output('ice_gfa', 'children'),
Output('ice_p', 'children'),
Input('gfa_input', 'value'), 
State('main_store', 'data')
)
def gfa_calc(val, data):
    df = pd.read_json(data, orient="split")
    gb_ec, epic_ec, ice_ec = em_calc(df)
    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
    # archicad_ec = sum(df["Embodied Carbon"].tolist())

    if val is not None:

        # gfa_val = [archicad_ec/val, sum(gb_ec)/val, sum(epic_ec)/val, sum(ice_ec)/val]
        gfa_val = [sum(gb_ec)/val, sum(epic_ec)/val, sum(ice_ec)/val]

        # archicad_gfa_out = "{:,}".format(np.around(gfa_val[0],2))
        gb_gfa_out = "{:,}".format(np.around(gfa_val[0],2))
        epic_gfa_out = "{:,}".format(np.around(gfa_val[1],2))
        ice_gfa_out = "{:,}".format(np.around(gfa_val[2],2))
        default_str = [html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4")]


        return gb_gfa_out, default_str, epic_gfa_out, default_str, ice_gfa_out, default_str

    else: return "Unknown", "Input GFA above", "Unknown", "Input GFA above","Unknown", "Input GFA above"  
