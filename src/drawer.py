import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html
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
                    label="Ratio is the volumn of Reinforcement Bars (m³) per volumn of Concrete (m³).",
                    children=[DashIconify(icon="feather:info")],
                ),
            ],
            direction="row",
        ),
        html.Div(
            children=[
                dmc.Text("Beam: 0", id="ratio_beam"),
                dmc.Slider(
                    id="beam_slider",
                    persistence_type="session",
                    persistence=True,
                    value=39,
                    min=32,
                    max=45,
                    step=1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("Column: 0", id="ratio_column"),
                dmc.Slider(
                    id="column_slider",
                    persistence=True,
                    persistence_type="session",
                    value=41,
                    min=25,
                    max=57,
                    step=1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("Slab: 0", id="ratio_slab"),
                dmc.Slider(
                    id="slab_slider",
                    persistence=True,
                    persistence_type="session",
                    value=13,
                    min=9,
                    max=17,
                    step=1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("wall: 0", id="ratio_wall"),
                dmc.Slider(
                    id="wall_slider",
                    persistence=True,
                    persistence_type="session",
                    value=11,
                    min=9,
                    max=13,
                    step=1,
                ),
            ],
            className="my-3",
        ),
        html.Div(
            children=[
                dmc.Text("stair: 0", id="ratio_stair"),
                dmc.Slider(
                    id="stair_slider",
                    persistence=True,
                    persistence_type="session",
                    value=19.5,
                    min=17,
                    max=22,
                    step=1,
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

print_layout = html.Div(children=[], id="print-layout")

drawer_print = html.Div(
    children=[
        dmc.Drawer(
            id="print-drawer",
            padding="md",
            size="full",
            withCloseButton=False,
            children=print_layout,
        )
    ]
)


@callback(
    Output("print-layout", "children"),
    Input("print-button", "n_clicks"),
    State("proc_store", "data"),
    prevent_initial_call=True,
)
def update_print_layout(n_clicks, proc_store):
    layout = [dcc.Graph(id="gb_analysis_comp_pie_2")]

    return layout
