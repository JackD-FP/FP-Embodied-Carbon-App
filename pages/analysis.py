from dash import Input, Output, State, dcc, html, dash_table
import dash_bootstrap_components as dbc
#from index import app, config
from pages import dashboard
from src import db_loader

layout = html.Div([
    html.H1("Analysis", className="display-2 mb-5 "),
    html.Hr(),
    html.Div([
        html.Img(
            src="https://img.icons8.com/ios-filled/100/000000/under-construction.png", 
            alt="under construction icon"),
        html.H1("UNDER CONSTRUCTION! SOMETHING COOL WILL COME OUT SOON", className="text-center"),
        html.Img(
            src="https://img.icons8.com/ios-filled/100/000000/under-construction.png", 
            alt="under construction icon")
    ], className="hstack gap-3"),
    dash_table.DataTable(
            db_loader.gb_df.to_dict('records'),
            [{'name': i, 'id': i} for i in db_loader.gb_df.columns],
            page_size= 15,
        )
])

# @app.callback(
# Output('analysis_test', 'children'),
# Input('dashboard_store', ''), 
# State('id_1', 'id_1_prop'))
# def definition(input):
#     return
