import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import firebase_admin
from dash import Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from firebase_admin import credentials, firestore, storage
from flask import Flask

from pages import analysis, benchmark, dashboard, documentation
from pages.analysis import analysis
from src import drawer, load_file, save_file

# server shit
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.icons.BOOTSTRAP,
    "styles.css",
]  # dbc theme

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    meta_tags=[
        {  # for mobile bs
            "name": "viewport",
            "content": "width=device-width, intial-scale=1.0",  # initial-scale don't work why? idk!
        }
    ],
)


@server.route("/pages/<path>")  # to change tab name to "Ebodied Carbon: dashboard"
def dash_app(path):  # but for some reason the page name doesn't work
    app.title = "Embodied Carbon: %s" % (path)  # just shows dashboard ¯\_(ツ)_/¯
    return app.index()


server = app.server  # this is for flask functionality
app._favicon = "assets/favicon.ico"
# --------------------------------------------------------------------------------------------


CONTENT_STYLE = {
    "marginLeft": "15rem",
    "marginRight": "2rem",
    "padding": "4rem 2rem",
}
CONTENT_STYLE_SMALL = {
    "marginLeft": "2rem",
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
# ----- Header UI -----
def create_home_link(label):
    return dmc.Text(
        label,
        size="xl",
        color="gray",
    )


header_ui = dmc.Header(
    height=70,
    fixed=True,
    p="md",
    children=[
        dmc.Group(
            position="apart",
            align="flex-start",
            children=[
                dmc.Center(
                    dcc.Link(
                        [
                            dmc.MediaQuery(
                                create_home_link("Embodied Carbon Tool"),
                                smallerThan="sm",
                                styles={"display": "none"},
                            ),
                            dmc.MediaQuery(
                                create_home_link("ECT"),
                                largerThan="sm",
                                styles={"display": "none"},
                            ),
                        ],
                        href="/",
                        style={"paddingTop": 5, "textDecoration": "none"},
                    ),
                ),
                dmc.Group(
                    position="right",
                    align="center",
                    spacing="xl",
                    children=[
                        html.A(
                            dmc.Tooltip(
                                dmc.ThemeIcon(
                                    DashIconify(
                                        icon="radix-icons:github-logo",
                                        width=22,
                                    ),
                                    radius=30,
                                    size=36,
                                    variant="outline",
                                    color="gray",
                                ),
                                label="Source Code",
                                position="bottom",
                            ),
                            href="https://github.com/JackD-FP/FP-Embodied-Carbon-App",
                        ),
                        html.A(
                            dmc.Tooltip(
                                dmc.ThemeIcon(
                                    DashIconify(
                                        icon="bi:discord",
                                        width=22,
                                    ),
                                    radius=30,
                                    size=36,
                                    variant="outline",
                                ),
                                label="Discord",
                                position="bottom",
                            ),
                            href="https://discord.gg/CEt4jbqV",
                        ),
                    ],
                ),
            ],
        )
    ],
)

# ----- Sidebar UI -----
def create_main_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                dmc.Text(label, size="md", color="gray"),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


def create_nav_link(name, path):
    return dcc.Link(
        dmc.Text(name, size="md", color="gray"),
        href=path,
        id=name,
        style={"textDecoration": "none"},
    )


def dividers(icon, label):
    return html.Div(
        dmc.Divider(
            label=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),  # "fluent:app-folder-24-filled"
                    size=20,
                    radius=20,
                    color="gray",
                    variant="light",
                    style={"marginRight": "0.5rem"},
                ),
                dmc.Text(label, size="sm", color="gray"),
            ],
            style={
                "marginBottom": 30,
                "marginTop": 30,
                "width": "100%",
            },
        ),
    )


sidebar_ui_element = html.Div(
    [
        dmc.ScrollArea(
            offsetScrollbars=True,
            type="scroll",
            children=[
                dmc.Group(
                    direction="column",
                    children=[
                        create_main_nav_link(
                            icon="radix-icons:rocket",
                            label="Getting Started",
                            href="/pages/documentation",
                        ),
                        # create_main_nav_link(
                        #     icon="radix-icons:iconjar-logo",
                        #     label="Dash Iconify",
                        #     href="/dashiconify",
                        # ),
                    ],
                ),
                dividers("fluent:app-folder-24-filled", "Analysis"),
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link("Dashboard", "/pages/dashboard"),
                        create_nav_link("Analysis", "/pages/analysis"),
                        create_nav_link("Benchmark", "/pages/benchmark"),
                    ],
                ),
                dividers("fa:folder-open-o", "Data"),
                dmc.Group(
                    [
                        dmc.Button(
                            "Save",
                            variant="outline",
                            leftIcon=[DashIconify(icon="fluent:save-24-regular")],
                            id="save-button",
                            color="green",
                        ),
                        dmc.Button(
                            "Load",
                            variant="outline",
                            leftIcon=[
                                DashIconify(icon="fluent:open-folder-24-regular")
                            ],
                            id="load-button",
                            color="blue",
                            # style={"marginBottom": "3rem"},
                        ),
                    ],
                    direction="column",
                ),
                dividers("akar-icons:gear", "settings"),
                dmc.Group(
                    [
                        dmc.Button(
                            "Print",
                            variant="outline",
                            leftIcon=[DashIconify(icon="bytesize:print")],
                            id="print-button",
                        ),
                        dmc.Button(
                            "Settings",
                            variant="outline",
                            leftIcon=[DashIconify(icon="fluent:settings-32-regular")],
                            id="settings-button",
                        ),
                    ],
                    direction="column",
                ),
                load_file.load_modal,
                save_file.save_modal,
                drawer.drawer_print,
                drawer.drawer_layout,
                dmc.Affix(
                    dmc.Tooltip(
                        label="Send some feedback!",
                        transition="rotate-left",
                        transitionDuration=300,
                        transitionTimingFunction="ease",
                        children=[
                            html.A(
                                dmc.Button(
                                    html.H5(
                                        className="bi bi-chat-dots-fill translate-middle",
                                        style={"position": "absolute", "top": "50%"},
                                    ),
                                    radius="xl",
                                    size="lg",
                                ),
                                href="mailto:jackd@fitzpatrickpartners.com?subject=Feedback for Embodied Carbon App!",
                            ),
                        ],
                    ),
                    style={"marginRight": "2rem", "marginBottom": "2rem"},
                ),
            ],
        )
    ],
)

sidebar_ui = dmc.MediaQuery(
    children=[
        dmc.Navbar(
            fixed=True,  # uncomment this line if you are using this example in your app
            width={"base": "18rem"},
            p="md",
            pl="lg",
            children=sidebar_ui_element,
        )
    ],
    smallerThan="lg",
    styles={"display": "none"},
)

# ----- Main UI -----
# media query for the main content... expands and contracts depending on the width of the screen

main_ui = dmc.MediaQuery(
    children=[html.Div(id="content-id", style=CONTENT_STYLE_SMALL)],
    largerThan="lg",
    styles=CONTENT_STYLE,
)

# ---------------------------- callback functions ----------------------------

# passes store to main_store
@app.callback(Output("main_store", "data"), Input("temp-df-store", "data"))
def save_2_main(data):
    if data is not None:
        return data
    else:
        PreventUpdate


# passes temp_proc_store to proc_store
@app.callback(
    Output("proc_store", "data"),
    Input("temp_proc_store", "data"),
)
def proc_store_update(data):
    if data is not None:
        return data
    else:
        raise PreventUpdate


# @app.callback(
#     Output("load_data", "data"),
#     Input("load-data-store", "data "),
# )
# def load_data_update(data):
#     if data is not None:
#         return data
#     else:
#         raise PreventUpdate


# passes the upload from card 2 for later access.
@app.callback(Output("card02_store", "data"), Input("card2_temp_store", "data"))
def save_2_card02(data):
    if data is not None:
        return data
    else:
        PreventUpdate


# passes the upload from card 3 for later access.
@app.callback(Output("card03_store", "data"), Input("card3_temp_store", "data"))
def save_2_card03(data):
    if data is not None:
        return data
    else:
        PreventUpdate


# saves project name
@app.callback(
    Output("project_name", "data"),
    Input("name_1", "data"),
)
def project_name_update(value):
    return value


# save gfa value
@app.callback(
    Output("nla_store", "data"),
    Output("gb_bld_type_store", "data"),
    Input("temp_gb_nla", "modified_timestamp"),
    Input("temp_gb_blt_type", "modified_timestamp"),
    State("temp_gb_nla", "data"),
    State("temp_gb_blt_type", "data"),
)
def gfa_store_update(
    nla_mts,
    blt_mts,
    nla,
    blt_type,
):
    if nla_mts is None or blt_mts is None:
        raise PreventUpdate
    else:
        return nla, blt_type


@app.callback(
    Output("gia_store", "data"),
    Input("temp_ice_gia", "modified_timestamp"),
    State("temp_ice_gia", "data"),
)
def gia_store_update(gia_mts, gia):
    if gia_mts is None:
        raise PreventUpdate
    else:
        return gia


# updates the setting data with sliders
@app.callback(
    [
        Output("settings-drawer", "opened"),
        Output("ratio_beam", "children"),
        Output("ratio_column", "children"),
        Output("ratio_slab", "children"),
        Output("ratio_wall", "children"),
        Output("ratio_stair", "children"),
    ],
    [
        Input("settings-button", "n_clicks"),
        Input("beam_slider", "value"),
        Input("column_slider", "value"),
        Input("slab_slider", "value"),
        Input("wall_slider", "value"),
        Input("stair_slider", "value"),
    ],
    prevent_initial_call=True,
)
def drawer_update(
    n,
    beam,
    column,
    slab,
    wall,
    stair,
):
    return (
        True,
        "Beam: {}".format(beam),
        "Column: {}".format(column),
        "Slab: {}".format(slab),
        "Wall: {}".format(wall),
        "Stair: {}".format(stair),
    )


# OPEN SAVE MODAL
@app.callback(
    Output("save-modal", "opened"),
    Input("save-button", "n_clicks"),
    State("save-modal", "opened"),
    prevent_initial_call=True,
)
def open_save_modal(n, opened):
    return not opened


# OPEN LOAD MODAL
@app.callback(
    Output("load-modal", "opened"),
    Input("load-button", "n_clicks"),
    State("save-modal", "opened"),
    prevent_initial_call=True,
)
def definition(n, opened):
    return not opened


@app.callback(
    Output("print-drawer", "opened"),
    Input("print-button", "n_clicks"),
    State("print-drawer", "opened"),
    prevent_initial_call=True,
)
def update_print_drawer(n, opened):
    return not opened


# routing stuff also 404 page
@app.callback(Output("content-id", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dcc.Location(pathname="/pages/dashboard", id="doesntmatter")
    elif pathname == "/pages/dashboard":
        return dashboard.layout
    elif pathname == "/pages/analysis":
        return analysis.analysis_layout
    elif pathname == "/pages/benchmark":
        return benchmark.layout
    elif pathname == "/pages/documentation":
        return documentation.layout

    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1(f"404: Page not found", className="text-danger display-5"),
            html.Hr(),
            html.Img(
                src="https://blush.design/api/download?shareUri=Itj_HmyiadrUTfGf&c=Hair_0%7Ef9a34e_Skin_0%7Ed8936c&w=800&h=800&fm=png",
                alt="shocked avatar by Diana Aguilar Ortiz",
                style={"margin": "auto", "display": "block", "height": "500px"},
            ),
            html.H3(
                "Are you lost? No worries, click the button below",
                className="text-center display-6",
                style={"marginTop": "2rem", "marginBottom": "2rem"},
            ),
            dbc.Button(
                "Show me the way out!",
                href="/pages/dashboard",
                size="lg",
                class_name="m-auto ",
                style={"width": "25%", "display": "block", "margin": "auto"},
                outline=True,
                color="primary",
            ),
        ]
    )


app.layout = dmc.NotificationsProvider(
    [
        header_ui,
        dcc.Store(id="analysis_store", storage_type="session"),
        dcc.Store(id="proc_store", storage_type="session"),  # PROCessed data
        dcc.Store(id="load_data", storage_type="session"),
        dcc.Store(id="main_store", storage_type="session"),  # unedited data
        dcc.Store(id="nla_store", storage_type="session"),
        dcc.Store(id="gb_bld_type_store", storage_type="session"),
        dcc.Store(id="gia_store", storage_type="session"),
        dcc.Store(id="project_name", storage_type="session"),
        dcc.Store(id="firebase_storage", storage_type="session"),
        dcc.Store(id="temp-load-store", storage_type="session"),
        dcc.Store(id="card02_store", storage_type="session"),
        # Stores card 2 upload data
        dcc.Store(id="card03_store", storage_type="session"),
        # Stores card 3 upload data
        dcc.Location(id="url", refresh=False),
        sidebar_ui,
        main_ui,
    ]
)

if __name__ == "__main__":
    # app.run_server(port=8888, debug=True)
    app.run_server(host="0.0.0.0", port=5555, debug=True)
