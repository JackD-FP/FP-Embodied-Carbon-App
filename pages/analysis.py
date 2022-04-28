# ---------------------------------------
# there is a few problems with this part. sometimes dash with give you error, even though the data is there.
# we may need to refactor that bit to simplify it... use 1 callback rather than 3... they do pretty much similar thing
#
# ---------------------------------------

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from src import analysis_cards

gb_df = pd.read_csv("src/Greenbook _reduced.csv")

layout = html.Div(
    [
        dcc.Store(id="page_storage", storage_type="session"),
        html.H1("Analysis", className="display-2 mb-5 "),
        html.Hr(),
        html.Div(id="table_div"),
    ],
    id="analysis_div",
)


@callback(
    Output("table_div", "children"),
    Input("proc_store", "data"),
)
def definition(data):
    if data is not None:
        df = pd.read_json(data, orient="split")
        if "Embodied Carbon" in df.columns:
            df = df.drop(["Embodied Carbon"], axis=1)
        else:
            pass

        df = df.groupby(by=["Materials"], as_index=False).sum()

        return html.Div(
            [
                html.H3("Structure Schedule"),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
                analysis_cards.greenbook_card,
                analysis_cards.epic_card,
                analysis_cards.ice_card,
            ]
        )

    elif data is None:
        dbc.Alert(  # not sure why this is not working
            [
                html.H1("UPLOAD you schule"),
                html.Hr(),
                html.P(
                    "please upload your structure schedule in the dashboard page",
                    className="h4",
                ),
                html.P("Happy designing! 😁"),
            ],
            is_open=True,
            dismissable=True,
        ),
