from multiprocessing.sharedctypes import Value

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from config import config
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.exceptions import PreventUpdate

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")

gb_more_info = [
    html.H3("Embodied Carbon per Floor From Green Book Database"),
    dmc.Skeleton(visible=False, children = dcc.Graph(id="gb_bar", config = config)),
]

epic_more_info = [
    html.H3("Embodied Carbon per Floor From Epic Database"),
    dmc.Skeleton(visible=False, children = dcc.Graph(id="epic_bar")),
]

ice_more_info = [
    html.H3("Embodied Carbon per Floor From Ice Database"),
    dmc.Skeleton(visible=False, children = dcc.Graph(id="ice_bar")),
]

@callback(
Output('gb_bar', 'figure'),
Output('epic_bar', 'figure'),
Output('ice_bar', 'figure'),

Input('row_concrete', 'value'),
Input('row_steel', 'value'),
Input('row_timber', 'value'),
Input('epic_row_concrete', 'value'),
Input('epic_row_steel', 'value'),
Input('epic_row_timber', 'value'),
Input('ice_row_concrete', 'value'),
Input('ice_row_steel', 'value'),
Input('ice_row_timber', 'value'),

State('main_store', 'data')
)
def bar_update(
    gb_conc_value, gb_steel_value, gb_timber_value,
    epic_conc_value, epic_steel_value, epic_timber_value, 
    ice_conc_value, ice_steel_value, ice_timber_value, 
    data
    ):
    if data is not None:
        df = pd.read_json(data, orient="split")
        df['gb_ec'] = ec_calc("gb", df, gb_conc_value, gb_steel_value, gb_timber_value)
        df['epic_ec'] = ec_calc("epic", df, epic_conc_value, epic_steel_value, epic_timber_value)
        df['ice_ec'] = ec_calc("ice", df, ice_conc_value, ice_steel_value, ice_timber_value)

        df = df.groupby(['Home Story Name', 'Building Materials (All)'], as_index=False).sum()

        gb_fig = px.bar(
            df,
            x="Home Story Name",
            y="gb_ec",
            color='Building Materials (All)',
            color_discrete_map={
                'CONCRETE - IN-SITU':'#5463FF',
                'TIMBER - STRUCTURAL': '#FF1818',
                'STEEL - STRUCTURAL': '#FFC300'
            },
            labels={
                'gb_ec': 'Embodied Carbon From ICE Database'
            }
        )

        epic_fig = px.bar(
            df,
            x="Home Story Name",
            y="epic_ec",
            color='Building Materials (All)',
            color_discrete_map={
                'CONCRETE - IN-SITU':'#5463FF',
                'TIMBER - STRUCTURAL': '#FF1818',
                'STEEL - STRUCTURAL': '#FFC300'
            },
            labels={
                'epic_ec': 'Embodied Carbon From ICE Database'
            }
        )

        ice_fig = px.bar(
            df,
            x="Home Story Name",
            y="ice_ec",
            color='Building Materials (All)',
            color_discrete_map={
                'CONCRETE - IN-SITU':'#5463FF',
                'TIMBER - STRUCTURAL': '#FF1818',
                'STEEL - STRUCTURAL': '#FFC300'
            },
            labels={
                'ice_ec': 'Embodied Carbon From ICE Database'
            }
        )
        return gb_fig, epic_fig, ice_fig
    else: raise PreventUpdate

"""
    WE MAY NEED TO REFACTOR THIS DEFINITION BELOW. 
    SOMEONE UPLOADS SOMETHING THAT DOENS'T HAVE 'CONCRETE - IN-SITU', 'STEEL - STRUCTURAL' OR 'TIMBER - STRUCTURAL'
    THE DEFINITION WILL NOT WORK.
"""

def ec_calc(database, df, conc_value, steel_value, timber_value):
    ec_list = []
    for i, elements in enumerate(df['Building Materials (All)']):

        df_vols = df["Volume (Net)"].tolist()
        df_mass = df['Mass'].tolist()

        if elements == "CONCRETE - IN-SITU":
            if database == "gb":
                ec = gb_df.loc[gb_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = epic_df.loc[epic_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = ice_df.loc[ice_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            else: print("error only gb, epic, ice")

        elif elements == "STEEL - STRUCTURAL":
            if database == "gb":
                ec = gb_df.loc[gb_df['Sub Category'] == steel_value, 'Embodied Carbon'].values[0] * df_mass[i]
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = epic_df.loc[epic_df['Sub Category'] == steel_value, 'Embodied Carbon'].values[0] * df_mass[i]
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = ice_df.loc[ice_df['Sub Category'] == steel_value, 'Embodied Carbon'].values[0] * df_mass[i]
                ec_list.append(np.around(ec, 2))
            else: print("error only gb, epic, ice")

        elif elements == "TIMBER - STRUCTURAL":
            if database == "gb":
                ec = gb_df.loc[gb_df['Sub Category'] == timber_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = epic_df.loc[epic_df['Sub Category'] == timber_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = ice_df.loc[ice_df['Sub Category'] == timber_value, 'Embodied Carbon'].values[0] * df_mass[i]
                ec_list.append(np.around(ec, 2))
            else: print("error only gb, epic, ice")

        else: #if empty or unknown... it just defualts it to concrete
            if database == "gb":
                ec = gb_df.loc[gb_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "epic":
                ec = epic_df.loc[epic_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            elif database == "ice":
                ec = ice_df.loc[ice_df['Sub Category'] == conc_value, 'Embodied Carbon'].values[0] * df_vols[i]
                ec_list.append(np.around(ec, 2))
            else: print("error only gb, epic, ice")

    return ec_list
