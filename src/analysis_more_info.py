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

#Output('test_potato', 'children'),
#Output('epic_bar', 'figure'),
#Output('ice_bar', 'figure'),
#Input('gb_accordion', 'state'), 


@callback(
    Output('gb_bar', 'figure'),
    Input('row_concrete', 'value'),
    Input('row_steel', 'value'),
    Input('row_timber', 'value'),
    State('main_store', 'data')
)# updates Green Book Database card
def accodion_graph(conc_value, steel_value, timber_value, data): 
    if data is not None:
        df = pd.read_json(data, orient="split")
        gb_ec = ec_calc("gb", df, conc_value, steel_value, timber_value)
        df['gb_ec'] = gb_ec
        df = df.groupby(['Home Story Name', 'Building Materials (All)'], as_index=False).sum()
        figure = px.bar(
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
                'gb_ec': 'Embodied Carbon From Green Book Database'
            }
        )
        return figure
    else: raise PreventUpdate 

@callback(
    Output('epic_bar', 'figure'),
    Input('epic_row_concrete', 'value'),
    Input('epic_row_steel', 'value'),
    Input('epic_row_timber', 'value'),
    State('main_store', 'data')
)# updates the epic database card
def epic_accodion_graph(conc_value, steel_value, timber_value, data):
    if data is not None:
        df = pd.read_json(data, orient="split")
        epic_ec = ec_calc("epic", df, conc_value, steel_value, timber_value)
        df['epic_ec'] = epic_ec
        df = df.groupby(['Home Story Name', 'Building Materials (All)'], as_index=False).sum()
        figure = px.bar(
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
                'epic_ec': 'Embodied Carbon From EPiC Database'
            }
        )
        return figure
    else: raise PreventUpdate 

@callback(
    Output('ice_bar', 'figure'),
    Input('ice_row_concrete', 'value'),
    Input('ice_row_steel', 'value'),
    Input('ice_row_timber', 'value'),
    State('main_store', 'data')
)# updates the ice database card
def ice_accodion_graph(conc_value, steel_value, timber_value, data):
    if data is not None:
        df = pd.read_json(data, orient="split")
        epic_ec = ec_calc("ice", df, conc_value, steel_value, timber_value)
        df['ice_ec'] = epic_ec
        df = df.groupby(['Home Story Name', 'Building Materials (All)'], as_index=False).sum()
        figure = px.bar(
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
        return figure
    else: raise PreventUpdate 


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
