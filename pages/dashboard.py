from logging import PlaceHolder
from dash import Input, Output, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from index import app

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "32rem",
    "padding": "4rem 2rem",
    "backgroundColor": "#f8f9fa",
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


layout = html.Div([sidebar,
    html.H1("Dashboard", className="display-2 mb-5 "),
    html.Hr(),
    html.P("opsies usually occur with 2 things wrong file input the table format does not have the right headers"),
    dbc.Input(id="input", placeholder="type something", type="text"),
    html.Div(id = "dashboard-div")
])
@callback(
    Output("dashboard-div", 'children'),
    Input("input", "value")
)
def test_callback(value):
    return value