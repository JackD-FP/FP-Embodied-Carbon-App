import re
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import openpyxl  # just so excel upload works
import pandas as pd
import plotly.graph_objects as go
from config import config
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from src import building_type_option, funcs, uploader

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

layout = html.Div([
    html.H1("Dashboard", className="display-2 mb-5 "),
    html.Hr(),
    html.P('The Embodied Carbon App is built to help architects and designers make informed in order to design a more sustainable building. \
        It is obvious to us that timber is far less carbon intense than concrete and steel. However, when it comes to actual buildings where mixtures of materials are necessary for structural stability, \
        the answer is less obvious. We should all strive to minimise our design’s embodied carbon, however, not compromise with structural stability and design excellence.\
        The App can help identify which material is carbon intense and check if there are alternatives less carbon intense to the later. \
        It can also help identify what floor is causing the issue if a redesign or alteration is required.\
        This app free and open source for anyone. At Fitzpatrick and Partners, \
        we believe this is the way to help our industry move forward and achieve a better and sustainable tomorrow.'
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
            uploader.parse_contents(c, n, d, "temp-df-store", "name_1") for c, n, d in
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

@callback(
Output('dashboard_graph', 'children'),
[Input('main_store', 'data')])
def make_graphs(data):
    if data is None:
        raise PreventUpdate
    elif data is not None:
        df_o = pd.read_json(data, orient="split") 
        gb_ec, epic_ec, ice_ec = em_calc(df_o) # makes df for greenbook db

        df = df_o.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        df_mat = df["Building Materials (All)"].tolist()

        embodied_carbon_dict = { 
            "Materials" : df_mat , 
            "Green Book (kgCO2e)" : gb_ec, 
            "EPiC EC (kgCO2e)": epic_ec, 
            "ICE EC (kgCO2e)": ice_ec
            }
        total_dict = { #lol u a total dict
            "Materials" : "TOTALS", 
            "Green Book (kgCO2e)" :(gb_sum := sum(gb_ec)), 
            "EPiC EC (kgCO2e)": (epic_sum := sum(epic_ec)), 
            "ICE EC (kgCO2e)": (ice_sum := sum(ice_ec))
        }

        ec_df = pd.DataFrame(embodied_carbon_dict)

        ec_df.loc[:,"Green Book (kgCO2e)"] = ec_df["Green Book (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"EPiC EC (kgCO2e)"] = ec_df["EPiC EC (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"ICE EC (kgCO2e)"] = ec_df["ICE EC (kgCO2e)"].map('{:,.2f}'.format)

        label_colors = funcs.label_colours_update(df_mat, "list")

        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]])
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
            annotations=[
                        dict(text='Greenbook', x=0.12, y=0.50, font_size=16, showarrow=False),
                        dict(text='{:,.2f} kgCO2e'.format(gb_sum), x=0, y=0.1, font_size=32, showarrow=False),
                        dict(text='EPiC', x=0.50, y=0.50, font_size=16, showarrow=False),
                        dict(text='{:,.2f} kgCO2e'.format(epic_sum), x=0.5, y=0.1, font_size=32, showarrow=False),
                        dict(text='ICE', x=0.87, y=0.50, font_size=16, showarrow=False),
                        dict(text='{:,.2f} kgCO2e'.format(ice_sum), x=1, y=0.1, font_size=32, showarrow=False),
                        ],
                      )
        # fig.update_traces(hoverinfo='label+percent+value', textinfo='percent', marker=dict(colors=graph_colors))
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent', marker=dict(colors=label_colors))
        
        #drop embodied carbon if it exist
        if 'Embodied Carbon' in df.columns:
            df = df.drop(["Embodied Carbon"], axis=1)
        else: pass

        df.rename(
            columns={
            "Building Materials (All)": "Materials", 
            "Mass": "Mass (kg)", 
            "Volume (Net)": "Volume (m³)", 
            "3D Length": "Length (m)"}, 
            inplace=True
        )


        return html.Div([ # consolidated table..
            html.H3(["Uploaded File: ", html.Span(id="file_name", className="display-5")], className="my-3"),
            html.P("You can review your uploaded file with the table below. See if there are any errors or missing data.", className="my-3"),
            html.Div(id="error_check"),
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
                        value='5_a_grade',
                        options=building_type_option.building_type,
                        className="w-25",
                    ),
                ], className="my-5"),
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            #Green Book Column
                            html.H5(
                                "Green Book DB", 
                                className="my-4 display-6 text-center",
                                style={"marginLeft": "2rem"},
                                ),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),
                            html.Div([
                                dmc.Tooltip(
                                    wrapLines=True,
                                    width=208,
                                    withArrow=True,
                                    transition="fade",
                                    transitionDuration=200,
                                    label= funcs.total_ec_comparison(gb_sum,epic_sum,ice_sum,"EPiC DB","ICE DB"),
                                    children=[
                                        dbc.Row([
                                            dbc.Col(
                                                html.H3("{:,}".format(np.around(gb_sum,2)
                                                ), 
                                                className="text-end")
                                            ),
                                            dbc.Col(
                                                html.P([
                                                    html.Span([
                                                        "kgCO",
                                                        html.Sup(2),
                                                        html.Sub('e')
                                                    ], 
                                                    className="fs-4"
                                                    ), " Total EC"
                                                ]),
                                                className="text-start"
                                            ),
                                        ]),
                                    ],
                                    style={"display": "block"}
                                ),
                                #html.P(percent_check_return(lowest_ec, gb_sum), className="text-center"),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),

                            #GFA calc for green book
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="gb_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4")], id="gb_p",
                                        className="text-start"),
                                    ])
                                ]),
                                html.P("Design's Benchmark", className="text-center"),
                                html.P("Benchmark Score", className="text-center mt-5 "),
                                html.Div(id="gb_benchmark"),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),

                        ], className="bg-light py-5 px-3"),
                        
                        dbc.Col([
                            #EPiC Column
                            html.H5(
                                "EPIC DB", 
                                className="my-4 display-6 text-center",
                                style={"marginLeft": "2rem"},
                                ),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),
                            html.Div([
                                dmc.Tooltip(
                                    wrapLines=True,
                                    width=240,
                                    withArrow=True,
                                    transition="fade",
                                    transitionDuration=200,
                                    label= funcs.total_ec_comparison(epic_sum,gb_sum,ice_sum,"Green Book DB","ICE DB"),
                                    children=[
                                        dbc.Row([
                                            dbc.Col(
                                                html.H3("{:,}".format(np.around(epic_sum,2)
                                                ), 
                                                className="text-end")
                                            ),
                                            dbc.Col(
                                                html.P([
                                                    html.Span([
                                                        "kgCO",
                                                        html.Sup(2),
                                                        html.Sub('e')
                                                    ], 
                                                    className="fs-4"
                                                    ), " Total EC"
                                                ]),
                                                className="text-start"
                                            ),
                                        ]),
                                    ],
                                    style={"display": "block"}
                                ),
                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),

                            #GFA calc for epic
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="epic_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4")], id="epic_p",
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
                            className="my-4 display-6 text-center",
                            style={"marginLeft": "2rem"}
                            ),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),
                            html.Div([
                                dmc.Tooltip(
                                    wrapLines=True,
                                    width=256,
                                    withArrow=True,
                                    transition="fade",
                                    transitionDuration=200,
                                    label= funcs.total_ec_comparison(ice_sum,gb_sum,epic_sum,"Green Book DB","EPiC DB"),
                                    children=[
                                        dbc.Row([
                                            dbc.Col(
                                                html.H3("{:,}".format(np.around(ice_sum,2)
                                                ), 
                                                className="text-end")
                                            ),
                                            dbc.Col(
                                                html.P([
                                                    html.Span([
                                                        "kgCO",
                                                        html.Sup(2),
                                                        html.Sub('e')
                                                    ], 
                                                    className="fs-4"
                                                    ), " Total EC"
                                                ]),
                                                className="text-start"
                                            ),
                                        ]),
                                    ],
                                    style={"display": "block"}
                                ),   

                            ], style={"marginTop":"3rem","marginBottom":"3rem"}),
                            dmc.Divider(style={"marginLeft": "2rem", "marginRight": "2rem"}),

                            #GFA calc for ice
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H3(id="ice_gfa",
                                        className="text-end"),
                                    ]),
                                    dbc.Col([
                                        html.P([html.Span(["kgCO",html.Sup(2),html.Sub('e'),'/m',html.Sup(2)], className="fs-4")],id="ice_p",
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
Output('file_name', 'children'),
Input('project_name', 'data'), 
)
def filename_update(data):
    return data

@callback(
Output('error_check', 'children'),
Input('main_store', 'data'),
)
def error_update(data):
    df = pd.read_json(data, orient="split")
    return funcs.upload_alert(df)
    


@callback(
Output('gb_gfa', 'children'),
Output('epic_gfa', 'children'),
Output('ice_gfa', 'children'),
Output('gb_benchmark', 'children'),

Input('gfa_input', 'value'), 
Input('bld_type', 'value'),

State('main_store', 'data')
)
def gfa_calc(val, bld_type, data):
    df = pd.read_json(data, orient="split")
    gb_ec, epic_ec, ice_ec = em_calc(df)
    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 

    if val is not None:

        gfa_val = [sum(gb_ec)/val, sum(epic_ec)/val, sum(ice_ec)/val]

        gb_gfa_out = "{:,}".format(np.around(gfa_val[0],2))
        epic_gfa_out = "{:,}".format(np.around(gfa_val[1],2))
        ice_gfa_out = "{:,}".format(np.around(gfa_val[2],2))

        
        def benchmark(Embodied_Carbon, Building_Type):
            if Building_Type == "2_premium":
                if Embodied_Carbon <= 1450 and Embodied_Carbon >= 1160:
                    return funcs.progress_bar(3, Embodied_Carbon, 1160, 1450)
                elif Embodied_Carbon <= 1160 and Embodied_Carbon >= 870:
                    return funcs.progress_bar(4, Embodied_Carbon, 870, 1160)
                elif Embodied_Carbon <= 870:
                    return funcs.progress_bar(5, Embodied_Carbon, 0, 870)
                else: return html.Div("Improvement Required", className="text-center")

            elif Building_Type == "2_multi-res":
                if Embodied_Carbon <= 990 and Embodied_Carbon >= 790:
                    return funcs.progress_bar(3, Embodied_Carbon, 790, 990)
                elif Embodied_Carbon <= 790 and Embodied_Carbon >= 590:
                    return funcs.progress_bar(4, Embodied_Carbon, 590, 790)
                elif Embodied_Carbon <= 590:
                    return funcs.progress_bar(5, Embodied_Carbon, 0, 590)
                else: return html.Div("Improvement Required", className="text-center")

            elif Building_Type == "5_premium":
                if Embodied_Carbon <= 1500 and Embodied_Carbon >= 1200:
                    return funcs.progress_bar(3, Embodied_Carbon, 1200, 1500)
                elif Embodied_Carbon <= 1200 and Embodied_Carbon >= 900:
                    return funcs.progress_bar(4, Embodied_Carbon, 900, 1200)
                elif Embodied_Carbon <= 900:
                    return funcs.progress_bar(5, Embodied_Carbon, 0, 900)
                else: return html.Div("Improvement Required", className="text-center")

            elif Building_Type == "5_a_grade":
                if Embodied_Carbon <= 800 and Embodied_Carbon >= 640:
                    return funcs.progress_bar(3, Embodied_Carbon, 640, 800)
                elif Embodied_Carbon <= 640 and Embodied_Carbon >= 480:
                    return funcs.progress_bar(4, Embodied_Carbon, 480, 640)
                elif Embodied_Carbon <= 480:
                    return funcs.progress_bar(5, Embodied_Carbon, 0, 480)
                    # stars_append(5)
                else: return html.Div("Improvement Required", className="text-center")

            elif Building_Type == "6_regional":
                if Embodied_Carbon <= 2150 and Embodied_Carbon >= 1750:
                    return funcs.progress_bar(3, Embodied_Carbon, 1750, 2150)
                elif Embodied_Carbon <= 1720 and Embodied_Carbon >= 1250:
                    return funcs.progress_bar(4, Embodied_Carbon, 1250, 1720)
                elif Embodied_Carbon <= 1290:
                    return funcs.progress_bar(4, Embodied_Carbon, 0, 1290)
                else: return html.Div("Improvement Required", className="text-center")

            elif Building_Type == "5_sub_regional":
                if Embodied_Carbon <= 1220 and Embodied_Carbon >= 970:
                    return funcs.progress_bar(3, Embodied_Carbon, 970, 1220)
                elif Embodied_Carbon <= 970 and Embodied_Carbon >= 730:
                    return funcs.progress_bar(4, Embodied_Carbon, 730, 970)
                elif Embodied_Carbon <= 730:
                    return funcs.progress_bar(5, Embodied_Carbon, 0, 730)
                else: return html.Div("Improvement Required", className="text-center")

        return gb_gfa_out, epic_gfa_out, ice_gfa_out, html.Div(benchmark(gfa_val[0],bld_type))

    else: return "Unknown - Input GFA above", "Unknown - Input GFA above", "Unknown - Input GFA above", ""

