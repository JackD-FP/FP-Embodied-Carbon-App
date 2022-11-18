import base64
import datetime
import io

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dash_table, dcc, html
from dash_iconify import DashIconify


def parse_contents(contents, filename, date, id, id_name):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return dmc.Alert(
            "There was an error processing this file.",
        )

    df = df.rename(columns=df.iloc[0])
    df = df.drop([0, 0])
    df = df.replace("---", 0)
    return html.Div(
        [
            dcc.Store(id=id, data=df.to_json(orient="split")),
            dcc.Store(id=id_name, data=filename),
            dmc.Notification(
                id="my-notification",
                title="Data loaded",
                message="The process has started.",
                color="green",
                action="show",
                icon=[DashIconify(icon="akar-icons:circle-check")],
            ),
        ]
    )
