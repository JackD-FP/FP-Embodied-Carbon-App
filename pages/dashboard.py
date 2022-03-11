import dash
from dash import Input, Output, State, dcc, html, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import base64
import datetime
import io
import pandas as pd
import openpyxl #just so excel upload works 
from index import app, config

from src import db_loader

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

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
            dbc.Button("Drag and Drop or Schedule File", 
            className = "fs-3 align-center position-absolute top-50 start-50 translate-middle text-light w-100 h-100",
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
        className = 'text-center mb-5 border border-1 rounded-3 shadow bg-primary',
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Store(id="dashboard_store", storage_type="session"),# i wish there a better way
    html.Div(id="display-table"),     #reload_table is only there cause display-table only loads once
    html.Div(id='reload_table'),      #this is triggered by the dashboard click in the side menu
    html.Div(id="dashboard_graph"),
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
                html.P("{} has been uploaded succesfully".format(filename), className="h4"),
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
State("dashboard_store", 'data'))
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

@callback(
Output('dashboard_graph', 'children'),
[Input('dashboard', 'n_clicks'),Input('upload_btn', 'n_clicks')],
State('dashboard_store', 'data'))
def make_graphs(n_dashb, n_upload, data):
    if n_dashb or n_upload is None:
        raise PreventUpdate
    elif data is not None:
        labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
          "Rest of World"]
        df = pd.read_json(data, orient="split")
        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        df_mat = df["Building Materials (All)"].tolist()
        df_ec = df["Embodied Carbon"].tolist()
        gb = gb_calc(df) # makes df for greenbook db
        gb_mat = gb["Materials"].tolist()
        gb_ec = gb["Embodied Carbon"].tolist()
        #fig = make_subplots(rows=1, cols=2)
        # fig.add_trace(row=1, col=1,
        #     trace = go.Pie(labels = df_mat, values = df_ec))
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=df_mat, values=df_ec, name="Archicad", hole=0.5),
              1, 1)
        fig.add_trace(go.Pie(labels=gb_mat, values=gb_ec, name="Green Book DB",hole=0.5),
              1, 2)
        #fig.add_trace(row=1, col=2,
            #trace = go.Pie(Labels = gb["Materials"], values=df["Embodied Carbon"], name="Green Book DB"))
        # Use `hole` to create a donut-like pie chart
        #fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig.update_layout(
            title_text="Global Emissions 1990-2011",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Archicad', x=0.18, y=0.5, font_size=20, showarrow=False ),
                        dict(text='Greenbook', x=0.82, y=0.5, font_size=20, showarrow=False)])

        # material_pie_archicad = px.pie(
        #     data_frame=df,
        #     values="Embodied Carbon",
        #     names="Building Materials (All)",
        #     title="Structure Embodied Carbon per Material",
        #     hole=0.5
        # )
        # material_pie_archicad.update_layout(
        #     annotations=[dict(text='ArchiCAD', x=0.5, y=0.5, font_size=20, showarrow=False)] # probs change archicad to "BIM" in production build
        # )
        
        #for calculations
        # materials = df["Building Materials (All)"].tolist()
        # volumes = df["Volume (Net)"].tolist()
        # mass = df["Mass"].tolist()
        # length = df["3D Length"].tolist()
        # gb = []
        # epic = []
        # ice = []

        # gb_mat = []
        # epic_mat = []
        # ice_mat = []

        # #greenbook:
        # df_greenbook = pd.DataFrame({"materials": gb_mat, "Embodied Carbon": gb})
        # df_epic = pd.DataFrame({"materials": epic_mat, "Embodied Carbon": epic})
        # df_ice = pd.DataFrame({"materials": ice_mat, "Embodied Carbon": ice})

        # ADD CALCULATION OF DIFFERENT EMBODIED CARBON MATERIALS q(≧▽≦q)
        # MAYBE ADD A RERENDER BUTTON? GRAPH DISSAPEAR WHEN GOING TO OTHER PAGES
        
        return html.Div([ # consolidated table..
            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns],
                page_size= 15,
            ),
            dcc.Graph(figure=fig ,style={'height': '75vh'}, className='mt-3',config=config),
            # dcc.Graph(figure=material_pie_archicad ,style={'height': '75vh'}, className='mt-3',config=config),
            #html.H1('{}'.format(str(gb_calc(df, gb_df))))
        ])
        


# def gb_calc(df):
#     for i in range(len(df)):
#         if "concrete" not in df["Building Materials (All)"][i]:
#             return df["Volume (Net)"][i]*db_loader.gb_df.loc[db_loader["Sub-Category"] == "Concrete 50 MPa", "Embodied Carbon"]

def gb_calc(df):
    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() # create consolidated df
    materials = []
    volumes = df["Volume (Net)"].tolist()
    mass = df["Mass"].tolist()
    embodied_carbon = []

    for i, mat in enumerate(materials):
        if mat == "CONCRETE - IN-SITU":
            embodied_carbon.append(volumes[i]*643) #Concrete 50 MPa 
            materials.append("Concrete 50 MPa ")
        elif mat == "STEEL - STRUCTURAL":
            embodied_carbon.append(mass[i]*2900) #Steel Universal Section
            materials.append("Steel Universal Section")
        if mat == "TIMBER - STRUCTURAL":
            embodied_carbon.append(volumes[i]*718) #Glue-Laminated Timber (Glu-lam)
            materials.append("Glue-Laminated Timber (Glu-lam)")
        else: embodied_carbon.append(0) # add other materials like aluminium and brick
        
    return pd.DataFrame({'Materials': materials, 'Embodied Carbon': embodied_carbon})

    # for i in range(len(df)):

    #     volume.append(df.loc[df[materials[i]] == "CONCRETE - IN-SITU", "Volume (Net)"].values[0])
    
    
    
    #volume = df.loc[df["Building Materials (All)"] == "CONCRETE - IN-SITU", "Volume (Net)"].values[0]
