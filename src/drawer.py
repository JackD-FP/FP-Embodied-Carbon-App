import dash_mantine_components as dmc
from dash import Input, Output, State, dcc, html, callback
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

settings_ui = html.Div(
    children=[
        dmc.Group(
            [
                dmc.Text("Rebar Concrete Ratio Settings", weight=700, size="lg"),
                dmc.Tooltip(
                    wrapLines=True,
                    width=220,
                    withArrow=True,
                    transition="fade",
                    transitionDuration=200,
                    # delay=250,
                    label="Ratio is the volumn of Reinforcement Bars (m³) per volumn of Concrete (1000 m³).",
                    children=[DashIconify(icon="feather:info")],
                ),
            ],
            direction="row",
        ),
        html.Div(
            children=[
                dmc.Text("Beam: 39", id="ratio_beam"),
                dmc.Slider(
                    id="beam_slider",
                    persistence_type="session",
                    persistence=True,
                    value=39,
                    min=32,
                    max=45,
                    step=0.1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("Column: 41", id="ratio_column"),
                dmc.Slider(
                    id="column_slider",
                    persistence=True,
                    persistence_type="session",
                    value=41,
                    min=25,
                    max=57,
                    step=0.1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("Slab: 13", id="ratio_slab"),
                dmc.Slider(
                    id="slab_slider",
                    persistence=True,
                    persistence_type="session",
                    value=13,
                    min=9,
                    max=17,
                    step=0.1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("wall: 11", id="ratio_wall"),
                dmc.Slider(
                    id="wall_slider",
                    persistence=True,
                    persistence_type="session",
                    value=11,
                    min=9,
                    max=13,
                    step=0.1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("stair: 19.5", id="ratio_stair"),
                dmc.Slider(
                    id="stair_slider",
                    persistence=True,
                    persistence_type="session",
                    value=19.5,
                    min=17,
                    max=22,
                    step=0.1,
                ),
            ],
            className="my-3",
        ),
    ],
    className="px-5",
)

drawer_layout = html.Div(
    children=[
        dmc.Drawer(
            title="Settings",
            id="settings-drawer",
            padding="md",
            size=450,
            children=[settings_ui],
        )
    ]
)


# updates the setting data with sliders
@callback(
    [
        Output("ratio_beam", "children"),
        Output("ratio_column", "children"),
        Output("ratio_slab", "children"),
        Output("ratio_wall", "children"),
        Output("ratio_stair", "children"),
    ],
    [
        Input("beam_slider", "value"),
        Input("column_slider", "value"),
        Input("slab_slider", "value"),
        Input("wall_slider", "value"),
        Input("stair_slider", "value"),
        Input("url", "pathname"),
    ],
    prevent_initial_call=True,
)
def drawer_update(beam, column, slab, wall, stair, url):
    if url != "pages/analysis":
        raise PreventUpdate
    else:
        return (
            "Beam: {}".format(beam),
            "Column: {}".format(column),
            "Slab: {}".format(slab),
            "Wall: {}".format(wall),
            "Stair: {}".format(stair),
        )
