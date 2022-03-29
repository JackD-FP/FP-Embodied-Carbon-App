from http import server
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, dcc, html, callback
from flask import Flask
import json

from src import save_modal
import dash_mantine_components as dmc
# from server import app

from pages import analysis, dashboard, documentation, comparison
import os

config = { #just tells plotly to save as svg rather than jpeg
    'toImageButtonOptions': {
        'format': 'svg', # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
    }
}

if not os.path.exists("image"):  #why do i have this?
    os.mkdir("image")            #was I suppose to do something with this?＼（〇_ｏ）／

#server shit
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP] #dbc theme

server = Flask(__name__)
app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    meta_tags=[{ #for mobile bs 
        'name': 'viewport',
        'content': 'width=device-width, intial-scale=1.0' #initial-scale don't work why? idk!
    }]
)
@server.route("/pages/<path>")                  #to change tab name to "Ebodied Carbon: dashboard" 
def dash_app(path):                             #but for some reason the page name doesn't work
    app.title = "Embodied Carbon: %s"%(path)     #just shows dashboard ¯\_(ツ)_/¯
    return app.index()
# #server = app.server
app._favicon = ("assets/favicon.ico")
#--------------------------------------------------------------------------------------------


CONTENT_STYLE = {
    "marginLeft": "26rem",
    "marginRight": "2rem",
    "padding": "4rem 2rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "4rem 2rem",
    "backgroundColor": "#f8f9fa",
}

#----------------------- side bar stuff -----------------------------------------
sidebar = html.Div(
    [
        html.Img(src="/assets/f+p_mono.svg", className="img-fluid"),
        html.H5("Embodied Carbon", className="mt-5 display-6", style={"font": "2rem"}),
        html.H5("Structure", className="mb-5 display-6 fs-3"),
        html.Hr(),
        html.P(
            "Analyse design using this Embodied Carbon Calculator. More information in the reference page below.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/pages/dashboard",  id="dashboard", active="exact"),
                dbc.NavLink("Analysis", href="/pages/analysis", id="analysis", active="exact"),
                dbc.NavLink("Comparison", href="/pages/comparison", id="tec", active="exact"),
                dbc.NavLink("Documentation", href="/pages/documentation", id="documentation", active="exact")
            ],
            vertical=True,
            pills=True,
            style={
                "marginTop": "3rem",
                "fontSize": "1.5rem"
            },
            className="display-6",
        ), 
        html.Hr(className="mt-5"),

        html.P([
                    html.I(className="bi bi-cone-striped"),
                    "save session is still under construction",
                    html.I(className="bi bi-cone-striped")],
                    className="text-center text-secondary fs-6"),

        html.H5("Files", className="mb-3 display-6 fs-3"),
        html.P("Save your session locally or share your project with everyone.", className="text-secondary"),
        dbc.Nav([
            dbc.NavItem(
                dbc.NavLink(
                    "Save Session", 
                    href="#",  
                    id="save_session", 
                    active=True,
                    className="border border-1 rounded-3 border-primary mb-3",
                    ),
            ),
            dbc.DropdownMenu(
                label="Load Session",
                children=[
                dbc.DropdownMenuItem("test 1"),
                dbc.DropdownMenuItem("test 2"),
                dbc.DropdownMenuItem("test 3"),
                ], nav=True, className="flex-grow-1 mb-3"
            ),
        ], vertical=True),
        save_modal.save_modal,
        dbc.Button([
            html.Div([
                html.Span(className="bi bi-share-fill"),
                html.Span("Share", style={'marginLeft': '0.5rem'}),
            ], style = {'display': 'block'}),
        ],className="mb-3"),
        html.P("Sharing Projects helps Architects \
            compare embodied carbon with other projects and make \
            benchmark scores more accurate", 
            className="text-secondary")
    ],
    style=SIDEBAR_STYLE,
)
#---------------------------- callback functions ----------------------------
@app.callback(
Output('save', 'is_open'),
Input('save_session', 'n_clicks'), 
Input('cancel_btn', 'n_clicks'),
State('save', 'is_open'))
def definition(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#passes store to main_store
@app.callback(
Output('main_store', 'data'),
Input('temp-df-store', 'data'))
def definition(data):
    if data is not None:
        return data
    else: PreventUpdate

app.layout = html.Div([
    dcc.Store(id="main_store", storage_type="session"), #stores all the BS here (⊙_⊙;) (add other stores if needed?)
    dcc.Store(id="project_name", storage_type="session"), # Stores project name
    dcc.Location(id="url", refresh=False), 
    sidebar,
    html.Div(id="content-id", style=CONTENT_STYLE)
    ])

@app.callback(
Output('project_name', 'data'),
Input('name_input', 'value'), 
)
def project_name_update(value):
    return value

#routing stuff also 404 page 
@app.callback(
    Output("content-id", "children"), 
    [Input("url", "pathname")]
    )
def render_page_content(pathname):
    if pathname == "/":
        return dcc.Location(pathname="/pages/dashboard", id="doesntmatter")
    elif pathname == "/pages/dashboard":
        return dashboard.layout
    elif pathname == "/pages/analysis":
        return analysis.layout
    elif pathname == "/pages/comparison":
        return comparison.layout
    elif pathname == "/pages/documentation":
        return documentation.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1(f"404: {pathname} Not found", className="text-danger display-5"),
            html.Hr(),
            html.Img(src="https://media0.giphy.com/media/Ta3v3I4GI1gH7Rqek6/giphy.gif?cid=790b76112944eebcc185f3eb1d07e97f8a5ec3bc078fd858&rid=giphy.gif&ct=g",
            alt="the weeknd lost gif", 
            style={
                "margin": "auto",
                'display': 'block'
            }),
            html.H3("Are you lost? No worries, click the button below", 
            className="text-center display-6",
            style={'marginTop': '2rem', 'marginBottom': '2rem'}),
            dbc.Button(
                "Show me the way out!", 
                href="/pages/dashboard",
                size="lg",
                class_name="m-auto ",
                style={
                    'width': '25%',
                    'display': 'block',
                    'margin': 'auto'
                    },
                outline=True,
                color='primary'
                ),
        ]
    )

if __name__ == "__main__":
    #app.run_server(port=8888, debug=True)
    app.run_server(port=5555, debug=True)
