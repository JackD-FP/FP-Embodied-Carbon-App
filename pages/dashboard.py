import dash
from dash import Input, Output, State, dcc, html, callback, dash_table
import plotly.express as px
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
        df = pd.read_json(data, orient="split")
        df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() 
        material_pie_archicad = px.pie(
            data_frame=df,
            values="Embodied Carbon",
            names="Building Materials (All)",
            title="Structure Embodied Carbon per Material",
            hole=0.5
        )
        material_pie_archicad.update_layout(
            annotations=[dict(text='ArchiCAD', x=0.5, y=0.5, font_size=20, showarrow=False)] # probs change archicad to "BIM" in production build
        )

        # ADD CALCULATION OF DIFFERENT EMBODIED CARBON MATERIALS q(≧▽≦q)
        # MAYBE ADD A RERENDER BUTTON? GRAPH DISSAPEAR WHEN GOING TO OTHER PAGES
        
        return html.Div([ # consolidated table..
            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns],
                page_size= 15,
            ),
            dcc.Graph(figure=material_pie_archicad ,style={'height': '75vh'}, className='mt-3',config=config),
            html.H1("material '{}' has embodied carbon of {}".format(str(df["Building Materials (All)"][0]), str(df["Embodied Carbon"][0])))
        ])
        


