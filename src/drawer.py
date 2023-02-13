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
                    label="Rebar Concrete Ratio Settings is a rough estimate of how much rebar and concrete is used in a building. The higher the ratio, the more rebar is used. The lower the ratio, the more concrete is used.",
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
                    value=300,
                    min=250,
                    max=350,
                    step=1,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            children=[
                dmc.Text("Column: 0", id="ratio_column"),
                dmc.Slider(
                    id="column_slider",
                    persistence=True,
                    persistence_type="session",
                    value=325,
                    min=200,
                    max=450,
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
                    value=101,
                    min=67,
                    max=135,
                    step=1,
                ),
            ],
            className="mt-3",
        ),
        dmc.Text(
            "1 way slabs: 75-125 kg/m³.",
            color="gray",
            size="xs",
        ),
        dmc.Text(
            "2 way slabs: 67-135 kg/m³.",
            color="gray",
            size="xs",
            class_name="mb-3",
        ),
        html.Div(
            children=[
                dmc.Text("wall: 0", id="ratio_wall"),
                dmc.Slider(
                    id="wall_slider",
                    persistence=True,
                    persistence_type="session",
                    value=85,
                    min=70,
                    max=100,
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
                    value=150,
                    min=130,
                    max=170,
                    step=1,
                ),
            ],
            className="my-3",
        ),
        dmc.Text("Graphing Configuration", weight=700, size="lg", class_name="mt-3"),
        dmc.Select(
            label="Export Graphs As",
            id="graph_export_type",
            data=["png", "svg", "jpeg", "webp"],
            value="svg",
            dropdownPosition="flip",
            description="Select the type of file to export graphs as.",
            class_name="mb-3",
            persistence_type="session",
        ),
        dmc.TextInput(
            label="File Name",
            id="graph_export_name",
            value="custom_image",
            description="Enter the name of the file to export graphs as.",
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


@callback(
    Output("config_id", "data"),
    Input("url", "pathname"),
    Input("graph_export_type", "value"),
    Input("graph_export_name", "value"),
)
def update_config(pathname, graph_export_type: str, graph_export_name: str):
    config = {  # just tells plotly to save as svg rather than jpeg
        "toImageButtonOptions": {
            "format": graph_export_type,  # one of png, svg, jpeg, webp
            "filename": graph_export_name,
            "height": None,
            "width": None,
            # "scale": 2,  # Multiply title/legend/axis/canvas sizes by this factor
        },
        "displaylogo": False,
        # "scrollZoom": True,
    }
    return config
