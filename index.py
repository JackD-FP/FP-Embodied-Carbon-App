from importlib.resources import path
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Input, Output, dcc, html
from server import app



from pages import analysis, dashboard, reference, total_embodied_carbon
import os

if not os.path.exists("image"):
    os.mkdir("image")

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "32rem",
    "padding": "4rem 2rem",
    "backgroundColor": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "34rem",
    "marginRight": "2rem",
    "padding": "4rem 2rem",
}

sidebar = html.Div(
    [
        html.Img(src="/assets/f+p_mono.svg", className="img-fluid"),
        html.H5("Embodied Carbon", className="my-5 display-6", style={"font": "2rem"}),
        html.Hr(),
        html.P(
            "Analyse design using this Embodied Carbon Calculator. More information in the reference page below.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/pages/dashboard", active="exact", id="dashboard_click"),
                dbc.NavLink("Analysis", href="/pages/analysis", active="exact"),
                dbc.NavLink("Total Embodied Carbon", href="/pages/total_embodied_carbon", active="exact"),
                dbc.NavLink("Reference", href="/pages/reference", active="exact")
            ],
            vertical=True,
            pills=True,
            style={
                "marginTop": "3rem",
                "fontSize": "1.5rem"
            },
            className="display-6",
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(id="content-id", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Store(id="main-store", storage_type="session"), #stores all the BS here (⊙_⊙;) add other stores if needed
    dcc.Location(id="url", refresh=False), 
    sidebar, 
    content
    ])

@app.callback(
    Output("content-id", "children"), 
    [Input("url", "pathname")]
    )
def render_page_content(pathname):
    if pathname == "/":
        return dcc.Location(pathname="/pages/dashboard", id="Iamauselessid") #redirect from /
    elif pathname == "/pages/dashboard":
        return dashboard.dashboard
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