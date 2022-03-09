from importlib.resources import path
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Input, Output, dcc, html, callback
import json
# from server import app

from pages import analysis, dashboard, reference, total_embodied_carbon
import os

#server BS (¬_¬")
external_stylesheets = [dbc.themes.BOOTSTRAP] #dbc theme
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    meta_tags=[{ #for mobile bs 
        'name': 'viewport',
        'content': 'width=device-width, intial-scale=1.0' #initial-scale don't work why? idk!
    }]
)
# #server = app.server
app._favicon = ("assets/favicon.ico")
#--------------------------------------------------------------------------------------------

if not os.path.exists("image"):
    os.mkdir("image")

CONTENT_STYLE = {
    "marginLeft": "34rem",
    "marginRight": "2rem",
    "padding": "4rem 2rem",
}


app.layout = html.Div([
    dcc.Store(id="main-store", storage_type="session"), #stores all the BS here (⊙_⊙;) add other stores if needed
    dcc.Location(id="url", refresh=False), 
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
    elif pathname == "/pages/reference":
        return reference.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger display-3"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...", className="lead"),
        ]
    )

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
    # app.run_server(host="0.0.0.0", port=8888, debug=True)