import base64
import datetime
import io

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import dash_table, dcc, html


def check_title(bool, id, data):
    if bool is False:
        pass
    else:
        return dcc.Store(id=id, data=data)


def parse_contents(contents, filename, date, id, id_name):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return dbc.Alert(
            [
                html.H1("An opsies occured 😢"),
                html.Hr(),
                html.P(str(e)),
                html.P(
                    [
                        "There is some error with the file you uploaded",
                    ],
                    className="fs-3 p-3",
                ),
            ],
            dismissable=True,
            color="warning",
            className="fixed-top w-25 mt-5 shadow",
            style={
                "zIndex": "2",
                "marginLeft": "73%",
            },
        )
    # cleaning dataset removes the header
    # TODO:
    # - make a cleaning script that removes header (Done)
    # - make script for users to chose which columns are which

    df = df.rename(
        columns=df.iloc[0],
    )
    df = df.drop([0, 0])
    df = df.replace("---", 0)
    return html.Div(
        [
            dcc.Store(id=id, data=df.to_json(date_format="iso", orient="split")),
            dcc.Store(id=id_name, data=filename),
            # dbc.Alert(
            #     [
            #         html.H1("Upload is SUCCESSFUL!"),
            #         html.Hr(),
            #         html.P(
            #             "{} has been uploaded succesfully".format(filename),
            #             className="fs-5",
            #         ),
            #         html.P("Happy designing! 😁"),
            #     ],
            #     is_open=True,
            #     dismissable=True,
            #     duration=1500,
            #     className="fixed-top w-25 mt-5 p-3",
            #     style={
            #         "zIndex": "10",
            #         "marginLeft": "73%",
            #     },
            # ),
        ]
    )
