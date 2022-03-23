import dash
from dash import Input, Output, State, dcc, html, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc

import base64
import datetime
import io
import pandas as pd
import numpy as np
import openpyxl #just so excel upload works 
from index import app, config

from src import db_loader

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
    dcc.Store(id="dashboard_store"),
    html.Div(id="display-table"),    
    html.Div(id='reload_table'),        # There is a bug where this loads whilst dashboard_graph is still active
    html.Div(id="dashboard_graph"),     # could just check but idk ceebs not elegant(?)...no thing is elegant (╯▔皿▔)╯
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return dbc.Alert([
            html.H1("An opsies occured 😢"),
            html.Hr(),
            html.P(str(e)),
            html.P(["There is some error with the file you uploaded. Check ",html.A('reference page', href="/pages/reference"), " for more info."],
            className="fs-3 p-3"),
            ],
            dismissable=True,
            color="warning",
            className= "fixed-top w-25 mt-5 shadow",
            style = {
                "zIndex": "2",
                "marginLeft": "73%",
            })
    df = df.rename(columns=df.iloc[0], )
    df = df.drop([0,0])
    df['Structure'] = df['Home Story Name'].str.contains('basement',case=False,regex=True)
    df = df.replace("---", 0)
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size= 15,
        ),
        dcc.Store(id="temp-df-store", data = df.to_json(date_format="iso", orient="split")),
        html.Hr(),
                dbc.Alert(
            [
                html.H1("Upload is SUCCESSFUL!"),
                html.Hr(),
                html.P("{} has been uploaded succesfully".format(filename), className="fs-5"),
                html.P("Happy designing! 😁")
            ], 
            is_open=True, 
            dismissable=True,
            className= "fixed-top w-25 mt-5 p-3",
            style = {
                "zIndex": "2",
                "marginLeft": "73%",
            },
        ),
    ])

@callback(Output('display-table', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(                              #passes the data to a div that will stay there
Output('dashboard_store', 'data'),      #idk who to fix multi-page... keep reloading to the original layout
Input('temp-df-store', 'data'))         #maybe change layout into a dcc.store?  ¯\_(ツ)_/¯ 
def pass_df(data):
    return data

@callback(
Output('reload_table', 'children'),
Input('dashboard', 'n_clicks'),
State("main_store", 'data'))
def rerender_table(n, data):
    if n is None:
        raise PreventUpdate
    elif data is not None:
        df = pd.read_json(data, orient="split")
        return dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size= 15,
        ),

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
        if mat == "CONCRETE - IN-SITU":
            gb_embodied_carbon.append(volumes[i]*643) #Concrete 50 MPa || Green Book
            epic_embodied_carbon.append(volumes[i]*600) #Concrete 40 MPa || Epic 
            ice_embodied_carbon.append(volumes[i]*413.4943) # Concrete 50 MPa || Ice
        elif mat == "STEEL - STRUCTURAL":
            gb_embodied_carbon.append(mass[i]*2.9) #Steel Universal Section || Green Book
            epic_embodied_carbon.append(mass[i]*2.9) #Steel structural steel section || Epic  
            ice_embodied_carbon.append(mass[i]*1.55) # steel Section|| Ice
        elif mat == "TIMBER - STRUCTURAL":
            gb_embodied_carbon.append(volumes[i]*718) #Glue-Laminated Timber (Glu-lam) || Green Book
            epic_embodied_carbon.append(volumes[i]*1718) #Glued laminated timber (glulam) || Epic 
            ice_embodied_carbon.append(mass[i]*0.51) # Timber Gluelam || Ice

        #ADD OTHER MATERIALS LIKE ALUMINIUM AND BRICK!!! (╯‵□′)╯︵┻━┻
        # Also i think it's better if we access dataframe.loc instead of a const
        # like look for the right material type or something.
        
    return np.around(gb_embodied_carbon,2), np.around(epic_embodied_carbon, 2), np.around(ice_embodied_carbon, 2)

@callback(
Output('dashboard_graph', 'children'),
[Input('main_store', 'data')],)
def make_graphs(data):
    if data is None:
        raise PreventUpdate
    elif data is not None:
        df = pd.read_json(data, orient="split") 
        gb_ec, epic_ec, ice_ec = em_calc(df) # makes df for greenbook db

        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        df_mat = df["Building Materials (All)"].tolist()
        df_ec = df["Embodied Carbon"].tolist() 

        embodied_carbon_dict = { 
            "Materials" : df_mat , 
            "Archicad (kgCO2e)" : df_ec,
            "Green Book (kgCO2e)" : gb_ec, 
            "EPiC EC (kgCO2e)": epic_ec, 
            "ICE EC (kgCO2e)": ice_ec
            }
        total_dict = { #lol u a total dict
            "Materials" : "TOTALS", 
            "Archicad (kgCO2e)" : (archicad_sum := sum(df_ec)),
            "Green Book (kgCO2e)" :(gb_sum := sum(gb_ec)), 
            "EPiC EC (kgCO2e)": (epic_sum := sum(epic_ec)), 
            "ICE EC (kgCO2e)": (ice_sum := sum(ice_ec))
        }

        ec_df = pd.DataFrame(embodied_carbon_dict)
        ec_df = ec_df.append(total_dict, ignore_index=True)

        ec_df.loc[:,"Archicad (kgCO2e)"] = ec_df["Archicad (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"Green Book (kgCO2e)"] = ec_df["Green Book (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"EPiC EC (kgCO2e)"] = ec_df["EPiC EC (kgCO2e)"].map('{:,.2f}'.format)
        ec_df.loc[:,"ICE EC (kgCO2e)"] = ec_df["ICE EC (kgCO2e)"].map('{:,.2f}'.format)

        fig = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}]])
        #subplot for archicad
        fig.add_trace(go.Pie(labels=df_mat, values=df_ec, name="Archicad", hole=0.5, scalegroup="dashboard_pie"),
              1, 1)
        #subplot for greenbook
        fig.add_trace(go.Pie(labels=df_mat, values=gb_ec, name="Green Book DB", hole=0.5, scalegroup="dashboard_pie"),
              1, 2)
        fig.add_trace(go.Pie(labels=df_mat, values=epic_ec, name="EPiC DB", hole=0.5, scalegroup="dashboard_pie"),
              2, 1)
        #subplot for greenbookW
        fig.add_trace(go.Pie(labels=df_mat, values=ice_ec, name="ICE DB", hole=0.5, scalegroup="dashboard_pie"),
              2, 2)
        fig.update_layout(
            title_text="Structure Embodied Carbon",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Archicad', x=0.205, y=0.80, font_size=16, showarrow=False),
                       dict(text='Greenbook', x=0.80, y=0.80, font_size=16, showarrow=False),
                       dict(text='EPiC', x=0.21, y=0.20, font_size=16, showarrow=False),
                       dict(text='ICE', x=0.78, y=0.20, font_size=16, showarrow=False)],
                      )
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent',marker=dict(colors=graph_colors))
        
        df = df.drop(["Complex Profile", "Structure"], axis=1)

        #calc for them progress ring
        db_total = sum([archicad_sum, gb_sum, epic_sum, ice_sum])
        

        return html.Div([ # consolidated table..
            dbc.Card([
                html.H3("Structure Summery"),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
                


            ], class_name="my-5 p-4 shadow"),
            dbc.Card([
                html.H3("Embodied Carbon(EC) calculation"),
                dbc.Table.from_dataframe(ec_df, striped=True, bordered=True, hover=True),
                html.H5("Embodied Carbon per square meter"),
                dbc.Input(
                    id="gfa_input",
                    placeholder="What's the gross floor area (gfa)?",
                    className="w-25",
                    type="number",
                    value=1,
                    debounce=True,
                ),
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dmc.RingProgress(
                                label="+{}%".format(archicad := (int((archicad_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": archicad, "color": "blue"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(archicad_sum), className="text-center"),
                            html.H6("Archicad Total EC", className="text-center") 
                        ],className=""),
                        dbc.Col([
                            dmc.RingProgress(
                                label="+{}%".format(green_book := (int((gb_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": green_book, "color": "green"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(gb_sum), className="text-center"),
                            html.H6("Green Book Total EC", className="text-center") 
                        ]),
                        dbc.Col([
                            dmc.RingProgress(
                                label="+{}%".format(epic := (int((epic_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": epic, "color": "red"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(epic_sum), className="text-center"),
                            html.H6("EPiC Total EC", className="text-center") 
                        ]),
                        dbc.Col([
                            dmc.RingProgress(
                                label="+{}%".format(ice := (int((ice_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": ice, "color": "yellow"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(ice_sum), className="text-center"),
                            html.H6("ICE Total EC", className="text-center") 
                        ]), 
                    ],className="my-5"),
#className="d-flex justify-content-between my-5"
                    dbc.Row([
                        dbc.Col([
                            dmc.RingProgress(
                                id="archicad_ring",
                                # label="+{}%".format(590),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": 1, "color": "blue"}
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(archicad_sum), id="archicad_h3", className="text-center"),
                            html.H6("Archicad EC per meter square", className="text-center") 
                        ],className=""),
                        dbc.Col([
                            dmc.RingProgress(
                                id="gb_ring",
                                #label="+{}%".format(green_book := (int((gb_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": 1, "color": "green"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(gb_sum), className="text-center"),
                            html.H6("Green Book Total EC", className="text-center") 
                        ]),
                        dbc.Col([
                            dmc.RingProgress(
                                id="epic_ring",
                                #label="+{}%".format(epic := (int((epic_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": 1, "color": "red"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(epic_sum), className="text-center"),
                            html.H6("EPiC Total EC", className="text-center") 
                        ]),
                        dbc.Col([
                            dmc.RingProgress(
                                id="ice_ring",
                                #label="+{}%".format(ice := (int((ice_sum*100)/db_total))),
                                size=130,
                                thickness=20,
                                roundCaps=True,
                                sections=[
                                    {"value": 1, "color": "yellow"},
                                ],
                                style={'margin': 'auto'}
                            ),
                            html.H3("{:,} kgCO2e".format(ice_sum), className="text-center"),
                            html.H6("ICE Total EC", className="text-center") 
                        ]), 
                    ],id='test', className="my-5"),

                ], fluid=True, className="gap-5"),
                dcc.Graph(figure=fig ,style={'height': '75vh'}, className='mt-3',config=config),
            ], class_name="my-5 p-4 shadow"),
        ])


@callback(
[Output('archicad_ring', 'sections'),
Output('gb_ring', 'sections'),
Output('ice_ring', 'sections'),
Output('epic_ring', 'sections')],
Input('gfa_input', 'value'),
State("main_store", 'data')
)
def archicad_gfa(value, data):
    df = pd.read_json(data, orient="split")
    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
    archicad_ec = sum(df["Embodied Carbon"].tolist())
    gb_ec, epic_ec, ice_ec = em_calc(df)

    if value is not None:
        archicad_ecgfa = archicad_ec/value
        gb_ecgfa = gb_ec[0]/value
        epic_ecgfa = epic_ec[0]/value
        ice_ecgfa = ice_ec[0]/value
        tot_ecgfa = archicad_ecgfa + gb_ecgfa + epic_ecgfa + ice_ecgfa

        archicad_sections = [{"value": archicad_ecgfa*100/tot_ecgfa, "color": "blue"}]
        gb_sections = [{"value": gb_ecgfa*100/tot_ecgfa, "color": "green"}]
        epic_sections = [{"value": epic_ecgfa*100/tot_ecgfa, "color": "red"}]
        ice_sections = [{"value": ice_ecgfa*100/tot_ecgfa, "color": "yellow"}]
        return archicad_sections, gb_sections, epic_sections, ice_sections
    else: raise PreventUpdate