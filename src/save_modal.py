from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc 
from numpy import greater, place

save_modal = dbc.Modal([
    dbc.ModalHeader(style={"borderBottom": "0px"}),
    dbc.ModalBody([
        html.Div([
            html.Img(src="/assets/folder.svg", 
                width=64, 
                className="text-center",
                style={
                    "marginLeft": '43%'
                }
            ),
            html.H1("Save Session", className="display-6 mb-5 text-center"),
            html.P("Save your session for later analysis and comparison", className="text-center text-secondary"),
            dbc.Input(
                placeholder="Give your session a name!",
                className="mb-5"
            ),
            html.Div([
                dbc.Button("Save", id="save_btn"),
                dbc.Button("Cancel", id="cancel_btn", outline=True, color="primary"),
                html.P([
                    html.I(className="bi bi-cone-striped"),
                    "save session is still under construction",
                    html.I(className="bi bi-cone-striped")],
                    className="text-center text-secondary fs-6")
            ], className="vstack m-auto gap-2")
        ], 
        id="save_main",
        style={"margin": "3rem"},
        hidden=False),
        html.Div(id="save_success",style={"margin": "3rem"})
    ])
],
id="save",
centered=True,
is_open=False, 
className=""
)

@callback(
Output('save_main', 'hidden'),
Input('save_btn', 'n_clicks'), 
)
def success_or_fail(n):
    if n is not None:
        return True

@callback(
Output('save_success', 'children'),
Input('save_btn', 'n_clicks'), 
)
def success_or_fail(n):
    if n is not None:
        children =[
            html.Div([
                html.Img(src="/assets/file_check.svg", 
                    width=64, 
                    className="text-center",
                    style={"marginLeft": '43%'}
                ),
                html.H1("Session saved", className="display-6 mb-5 text-center"),
                #dbc.Button("Close", id="close_btn", className="w-100 text-center", outline=True, color="success")
            ], className="m-auto"
            ),

        ]
        return children
    else: PreventUpdate