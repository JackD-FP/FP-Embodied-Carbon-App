import math
import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from config import graph_colors
from dash import html

from src import epic_options, greenbook_options, ice_options

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")


def total_ec_comparison(base, val1, val2, val1_db, val2_db):
    str = [
        checker(
            base,
            val1,
            val1_db,
        ),
        "\n",
        checker(base, val2, val2_db),
    ]
    return str


def checker(base, val, val_db):
    if base <= val:
        val1_percent = (val / base) * 100
        return "{} is 🔺 by +{:,.2f}%, ".format(val_db, val1_percent)
    else:
        val1_percent = (val / base) * 100
        return "{} is 🔻 by {:,.2f}%".format(val_db, val1_percent)


def find(df, ice):

    structure_concrete = 0
    structure_steel = 0
    structure_timber = 0

    if ice != True:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete = row["Net Volume"]
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel = row["Mass"]
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber = row["Net Volume"]
            else:
                pass
    else:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete = row["Net Volume"]
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel = row["Mass"]
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber = row["Mass"]
            else:
                pass
    return structure_concrete, structure_steel, structure_timber


def find2(df, ice):
    """Creates tupled list declared units of building material

    Args:
        df (_dataframe_): _pd dataframe of uploaded schedule_
        ice (_bool_): _bool to determine if ice is present

    Returns:
        _List_: tuple list of declared units of building material -> ([structure_concrete], [structure_steel], [structure_timber])
    """

    structure_concrete = []
    structure_steel = []
    structure_timber = []

    if ice != True:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete.append(row["Net Volume"])
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel.append(row["Mass"])
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber.append(row["Net Volume"])
            else:  # if it doesn't know it'll assume it's concrete
                structure_concrete.append(row["Net Volume"])
    else:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete.append(row["Net Volume"])
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel.append(row["Mass"])
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber.append(row["Mass"])
            else:  # if it doesn't know it'll assume it's concrete
                structure_concrete.append(row["Net Volume"])
    return structure_concrete, structure_steel, structure_timber


def label_colours_update(l, type_):
    color_list = []
    color_dict = {}
    if type_ == "list":

        for i, iter in enumerate(l):
            if re.search("concrete", iter, re.IGNORECASE):
                color_list.append("#5463FF")

            elif re.search("STEEL ", iter, re.IGNORECASE):
                color_list.append("#FFC300")

            elif re.search("TIMBER", iter, re.IGNORECASE):
                color_list.append("#FF1818")

            elif re.search("reinforcement", iter, re.IGNORECASE):
                color_list.append("#79B159")

        return color_list

    else:

        for i, iter in enumerate(l):
            if re.search("concrete", iter, re.IGNORECASE):
                # color_dict.append(graph_colors[0])
                color_dict.update({iter: graph_colors[0]})
            elif re.search("steel", iter, re.IGNORECASE):
                # color_dict.append(graph_colors[1])
                color_dict.update({iter: graph_colors[1]})
            elif re.search("timber", iter, re.IGNORECASE):
                # color_dict.append(graph_colors[2])
                color_dict.update({iter: graph_colors[2]})
            elif re.search("reinforcement Bar", iter, re.IGNORECASE):
                color_list.update({iter: graph_colors[4]})

        return color_dict


"""
        ADD OTHER MATERIALS LIKE ALUMINIUM AND BRICK!!! (╯‵□′)╯︵┻━┻
        - create flexibilities for other materials
"""


def em_calc(db, df, conc_val, steel_val, timber_val):
    """em_calc() calculates the EC of each material based on the database

    Args:
        db { String }: name of databse to use. "gb", "epic" or "ice"
        df { dataframe }: pd dataframe from the uploaded schedule
        conc_val { float }: concrete EC value from db eg. 643 from Concrete 50 MPa
        steel_val { float }: steel EC value from db eg. 2.9 from Steel Universal Section
        timber_val { float }: timber EC value from db eg. 718 from Glue-Laminated Timber (Glu-lam)

    Returns:
        [ list ]: returns a list of the EC of input db
    """

    df = df.groupby(
        by=["Building Materials (All)"], as_index=False
    ).sum()  # create consolidated df
    volumes = df["Net Volume"].tolist()
    df_mat = df["Building Materials (All)"].tolist()
    mass = df["Mass"].tolist()

    gb_embodied_carbon = []
    epic_embodied_carbon = []
    ice_embodied_carbon = []

    for i, mat in enumerate(df_mat):
        # if mat == "CONCRETE - IN-SITU":
        if re.search("concrete", mat, re.IGNORECASE):
            gb_embodied_carbon.append(
                volumes[i] * conc_val
            )  # Concrete 50 MPa || Green Book
            epic_embodied_carbon.append(
                volumes[i] * conc_val
            )  # Concrete 40 MPa || Epic
            ice_embodied_carbon.append(volumes[i] * conc_val)  # Concrete 50 MPa || Ice
        # elif mat == "STEEL - STRUCTURAL":
        elif re.search("steel", mat, re.IGNORECASE):
            gb_embodied_carbon.append(
                mass[i] * steel_val
            )  # Steel Universal Section || Green Book
            epic_embodied_carbon.append(
                mass[i] * steel_val
            )  # Steel structural steel section || Epic
            ice_embodied_carbon.append(mass[i] * steel_val)  # steel Section|| Ice
        # elif mat == "TIMBER - STRUCTURAL":
        elif re.search("timber", mat, re.IGNORECASE):
            gb_embodied_carbon.append(
                volumes[i] * timber_val
            )  # Glue-Laminated Timber (Glu-lam) || Green Book
            epic_embodied_carbon.append(
                volumes[i] * timber_val
            )  # Glued laminated timber (glulam) || Epic
            ice_embodied_carbon.append(mass[i] * timber_val)  # Timber Gluelam || Ice
        else:  # if all else fail assume concrete
            gb_embodied_carbon.append(volumes[i] * conc_val)  # Green Book
            epic_embodied_carbon.append(volumes[i] * conc_val)  # Epic
            ice_embodied_carbon.append(volumes[i] * conc_val)  # Ice

    if db == "gb":
        return gb_embodied_carbon
    elif db == "epic":
        return epic_embodied_carbon
    elif db == "ice":
        return ice_embodied_carbon


def stars_append(n):
    stars = []
    for i in range(n):
        stars.append(html.I(className="bi bi-star-fill mx-2"))
        star_outline = 4 - i
    for j in range(star_outline):
        stars.append(html.I(className="bi bi-star mx-2"))
    return html.Div(stars, className="text-center")


def progress_bar(n_stars, ec_val, lower, upper):
    """Progress bar for EC values

    Args:
        n_stars ( int ): number of stars
        ec_val ( float ): the EC value
        lower ( float ): lower bounds of benchmark
        upper ( float ): upper bounds of benchmark

    Returns:
        list: return list of components to render
    """

    val = (ec_val - lower) / (upper - lower)
    val = val * 100

    if lower == 0:
        label = "Design is {}% away from 4 stars. Please note that value will never reach 0 EC per meter.".format(
            100 - int(val)
        )
    else:
        label = ("{}% more for the next star".format(int(val)),)

    return html.Div(
        [
            stars_append(n_stars),
            html.Div(
                [
                    html.P(lower, className="text-start mb-0"),
                    dmc.Tooltip(
                        label=label,
                        transition="pop",
                        width=220,
                        transitionDuration=300,
                        transitionTimingFunction="ease",
                        withArrow=True,
                        children=[
                            dbc.Progress(label="{}%".format(int(val)), value=val),
                        ],
                        class_name="w-75",
                    ),
                    html.P(upper, className="text-end mb-0"),
                ],
                className="hstack mt-5",
                style={"justify-content": "space-between"},
            ),
            html.Div(
                [
                    html.P(
                        ["kgCO", html.Sub("e"), html.Sup("2"), "/m", html.Sup("2")],
                        className="text-start text-secondary",
                    ),
                    html.P(
                        ["kgCO", html.Sub("e"), html.Sup("2"), "/m", html.Sup("2")],
                        className="text-start text-secondary",
                    ),
                ],
                className="hstack",
                style={"justify-content": "space-between"},
            ),
        ],
        className="mx-5",
    )


def upload_alert(df):
    """checks for errors and returns a message

    Args:
        df ( dataframe ): dataframe from the uploaded schedule

    Returns:
        list: components to render
    """
    df = df.reset_index()
    nan_check = sum(df.isna().sum().tolist())
    nan_values = df[df.isna().any(axis=1)]
    nan_values_list = nan_values.index.tolist()

    if nan_check > 0:
        return dbc.Alert(
            [
                html.H3(
                    [
                        html.Span(
                            html.I(className="bi bi-exclamation-circle-fill me-3")
                        ),
                        "Warning:",
                    ],
                    className="mb-3",
                ),
                html.P(
                    [
                        "Please note that there are ",
                        html.Strong("{}".format(nan_check)),
                        " missing values in your input file. This will cause errors in the Analysis Page.",
                    ]
                ),
                dmc.Divider(class_name="my-3"),
                html.P(
                    [
                        "missing values can be found in row/s: ",
                        html.Strong(",".join(str(e + 1) for e in nan_values_list)),
                    ]
                ),
                html.P(
                    "You can edit the value on excel or other spreadsheet software and upload again."
                ),
                dbc.Table.from_dataframe(
                    nan_values,
                    striped=False,
                    bordered=True,
                    hover=True,
                    responsive=True,
                ),
            ],
            "Please fill in all the fields",
            color="warning",
            dismissable=True,
            is_open=True,
        )
    else:
        return dbc.Alert(
            [
                html.H3(
                    [
                        html.Span(
                            html.I(className="bi bi-exclamation-circle-fill me-3")
                        ),
                        "No errors found 😁",
                    ],
                    className="mb-3",
                ),
                html.P(
                    [
                        "there was no missing values in your input file. You can proceed to the Analysis Page."
                    ]
                ),
            ],
            "Please fill in all the fields",
            color="success",
            dismissable=True,
            is_open=True,
            duration=2000,
        )


def mass2vol(mass, density):
    """converts mass to volume

    Args:
        mass ( float ): mass in kg
        density ( float ): density in kg/m3

    Returns:
        float: volume in m3
    """
    return mass / density


def cyl2vol(diameter, height):
    """converts cylinder to volume

    Args:
        diameter ( float ): diameter in m
        height ( float ): height in m

    Returns:
        float: volume in m3
    """
    return math.pi * (diameter / 2) ** 2 * height


def vol2mass(vol, density):
    """converts volume to mass

    Args:
        vol ( float ): volume in m3
        density ( float ): density in kg/m3

    Returns:
        float: mass in kg
    """
    return vol * density


# # calculates the amount of reinforcement bars in the building
# df_s = df["Building Materials (All)"].str.contains('concrete', regex=True, flags=re.IGNORECASE)
# conc_vol = df.loc[lambda df: df["Building Materials (All)"].str.contains('concrete', regex=True, flags=re.IGNORECASE) == True, "Net Volume"]
# conc_mass = df.loc[lambda df: df["Building Materials (All)"].str.contains('concrete', regex=True, flags=re.IGNORECASE) == True, "Mass"]


def find_vols(vol, ratio):
    """Finds the volume of concrete and rebar of a beams element

    Args:
        vol ( float ): Volume of the element
        ratio ( float ): ratio of vol of rebar : vol of concrete

    Returns:
        Tuple: (vol_conc, vol_rebar) volume of concrete and rebar respectively
    """
    vol_conc = vol / (ratio + 1)
    vol_rebar = vol - vol_conc
    return vol_conc, vol_rebar


def mat_interpreter(
    df: pd.DataFrame,
) -> tuple:
    """interprets the materials in the schedule

    Args:
        df ( pd dataframe): uploaded schedule

    Returns:
        tuple: (mat, vol, mass, floor) tuple of lists of mass, volume, material and floor
    """
    mass = []
    vol = []
    mat = []
    floor = []
    layer = []
    gb_ec = []
    epic_ec = []
    ice_ec = []

    for i, row in df.iterrows():
        if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):

            # --------- check if the layer is BEAMS
            if re.search("beams", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.0385)

                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(vol_conc * greenbook_options.concrete[11]["value"])
                epic_ec.append(vol_conc * epic_options.concrete[12]["value"])
                ice_ec.append(vol_conc * ice_options.concrete[28]["value"])

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(mass_rebar * greenbook_options.rebar[0]["value"])
                epic_ec.append(mass_rebar * epic_options.rebar[0]["value"])
                ice_ec.append(mass_rebar * ice_options.rebar[0]["value"])

            # --------- Cheack if the layer is COLUMNS
            elif re.search("columns", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.041)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(vol_conc * greenbook_options.concrete[11]["value"])
                epic_ec.append(vol_conc * epic_options.concrete[12]["value"])
                ice_ec.append(vol_conc * ice_options.concrete[28]["value"])

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(mass_rebar * greenbook_options.rebar[0]["value"])
                epic_ec.append(mass_rebar * epic_options.rebar[0]["value"])
                ice_ec.append(mass_rebar * ice_options.rebar[0]["value"])

            # --------- Check if the layer is SLAB
            elif re.search("slab", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.013)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(vol_conc * greenbook_options.concrete[11]["value"])
                epic_ec.append(vol_conc * epic_options.concrete[12]["value"])
                ice_ec.append(vol_conc * ice_options.concrete[28]["value"])

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(mass_rebar * greenbook_options.rebar[0]["value"])
                epic_ec.append(mass_rebar * epic_options.rebar[0]["value"])
                ice_ec.append(mass_rebar * ice_options.rebar[0]["value"])

            # --------- Check if the layer is WALLS
            elif re.search("wall", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.022)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(vol_conc * greenbook_options.concrete[11]["value"])
                epic_ec.append(vol_conc * epic_options.concrete[12]["value"])
                ice_ec.append(vol_conc * ice_options.concrete[28]["value"])

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(mass_rebar * greenbook_options.rebar[0]["value"])
                epic_ec.append(mass_rebar * epic_options.rebar[0]["value"])
                ice_ec.append(mass_rebar * ice_options.rebar[0]["value"])

            # --------- Check if the layer is STAIRS
            elif re.search("stairs", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.022)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(vol_conc * greenbook_options.concrete[11]["value"])
                epic_ec.append(vol_conc * epic_options.concrete[12]["value"])
                ice_ec.append(vol_conc * ice_options.concrete[28]["value"])

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                gb_ec.append(mass_rebar * greenbook_options.rebar[0]["value"])
                epic_ec.append(mass_rebar * epic_options.rebar[0]["value"])
                ice_ec.append(mass_rebar * ice_options.rebar[0]["value"])

        # Appends timber values from layer
        elif re.search("timber", row["Layer"], re.IGNORECASE):
            mat.append(row["Building Materials (All)"])
            vol.append(row["Net Volume"])
            mass.append(row["Mass"])
            floor.append(row["Home Story Name"])
            layer.append(row["Layer"])
            gb_ec.append(
                row["Net Volume"] * greenbook_options.timber[1]["value"]
            )  # timber... assumes there no other materials types
            epic_ec.append(row["Net Volume"] * epic_options.timber[1]["value"])
            ice_ec.append(row["Mass"] * ice_options.timber[1]["value"])

        # Appends steel values from layer
        elif re.search("steel", row["Layer"], re.IGNORECASE):
            mat.append(row["Building Materials (All)"])
            vol.append(row["Net Volume"])
            mass.append(row["Mass"])
            floor.append(row["Home Story Name"])
            layer.append(row["Layer"])
            gb_ec.append(
                row["Mass"] * greenbook_options.steel[1]["value"]
            )  # timber... assumes there no other materials types
            epic_ec.append(row["Mass"] * epic_options.steel[1]["value"])
            ice_ec.append(row["Mass"] * ice_options.steel[1]["value"])
    return mat, vol, mass, floor, layer, gb_ec, epic_ec, ice_ec


def ec_calculator(
    df: pd.DataFrame,
    concrete_val: float,
    rebar_val: float,
    timber_val: float,
    steel_val: float,
    if_ice=False,
) -> tuple:
    """interprets the materials in the schedule

    Args:
        df ( pd dataframe): uploaded schedule
        if_ice (bool): if the schedule is ice default is False

    Returns:
        tuple: (mat, vol, mass, floor, layer, ec) tuple of lists of mass, volume, material and floor
    """
    mass = []
    vol = []
    mat = []
    floor = []
    layer = []
    ec = []

    for i, row in df.iterrows():
        if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):

            # --------- check if the layer is BEAMS
            if re.search("beams", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.0385)

                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(vol_conc * concrete_val)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(mass_rebar * rebar_val)

            # --------- Cheack if the layer is COLUMNS
            elif re.search("columns", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.041)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(vol_conc * concrete_val)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(mass_rebar * rebar_val)

            # --------- Check if the layer is SLAB
            elif re.search("slab", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.013)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(vol_conc * concrete_val)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(mass_rebar * rebar_val)

            # --------- Check if the layer is WALLS
            elif re.search("wall", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.022)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(vol_conc * concrete_val)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(mass_rebar * rebar_val)

            # --------- Check if the layer is STAIRS
            elif re.search("stairs", row["Layer"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Net Volume"], 0.022)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (7850 * vol_rebar))
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(vol_conc * concrete_val)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := row["Mass"] - mass_conc)
                floor.append(row["Home Story Name"])
                layer.append(row["Layer"])
                ec.append(mass_rebar * rebar_val)

        # Appends timber values from layer
        elif re.search("timber", row["Layer"], re.IGNORECASE):
            mat.append(row["Building Materials (All)"])
            vol.append(row["Net Volume"])
            mass.append(row["Mass"])
            floor.append(row["Home Story Name"])
            layer.append(row["Layer"])

            if if_ice:
                ec.append(row["Mass"] * timber_val)
                # timber... assumes there no other materials types
            else:
                ec.append(row["Net Volume"] * timber_val)

        # Appends steel values from layer
        elif re.search("steel", row["Layer"], re.IGNORECASE):
            mat.append(row["Building Materials (All)"])
            vol.append(row["Net Volume"])
            mass.append(row["Mass"])
            floor.append(row["Home Story Name"])
            layer.append(row["Layer"])
            ec.append(
                row["Mass"] * steel_val
            )  # steel... assumes there no other materials types

    return mat, vol, mass, floor, layer, ec
