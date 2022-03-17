from http import server
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, dcc, html, callback
from flask import Flask
import json
# from server import app

from pages import analysis, dashboard, total_embodied_carbon, documentation
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
external_stylesheets = [dbc.themes.BOOTSTRAP] #dbc theme

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
                dbc.NavLink("Total Embodied Carbon", href="/pages/total_embodied_carbon", id="tec", active="exact"),
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
        html.Hr(className="my-5"),
        html.H5("Files", className="mb-3 display-6 fs-3"),
        html.Div([
            dbc.Button("Primary", color="primary", className="m-auto"),
            dbc.Button("Primary", outline=True, color="primary", className="m-auto"),
        ], className="vstack"),


    ],
    style=SIDEBAR_STYLE,
)

#passes store to main_store
@app.callback(
Output('main_store', 'data'),
Input('temp-df-store', 'data'))
def definition(data):
    if data is not None:
        return data
    else: PreventUpdate

app.layout = html.Div([
    dcc.Store(id="main_store", storage_type="session"), #stores all the BS here (⊙_⊙;) add other stores if needed
    dcc.Location(id="url", refresh=False), 
    sidebar,
    html.Div(id="content-id", style=CONTENT_STYLE)
    ])

#routing bs
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
    elif pathname == "/pages/total_embodied_carbon":
        return total_embodied_carbon.layout
    elif pathname == "/pages/documentation":
        return documentation.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger display-3"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...", className="lead"),
        ]
    )

if __name__ == "__main__":
    #app.run_server(port=8888, debug=True)
    app.run_server(host="0.0.0.0", port=8888, debug=True)
