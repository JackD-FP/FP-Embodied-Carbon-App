from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from src import markdown

modal_layout = dmc.Modal(
    children=[
        markdown.markdown_layout,
        dmc.Space(h=20),
        # dmc.Button("Close", color="red", variant="outline", id="close-modal"),
    ],
    id="disclaimer_modal",
    size="xl",
)
