import re

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dash import html

from src import epic_options, greenbook_options, ice_options, material_options


def find_vols(vol, rebar_slider):
    """Finds the volume of concrete and rebar of a beams element.
    equation is: vol_concrete = vol_total / (1 + (1 / ratio))

    Args:
        vol ( float ): Volume of the element
        rebar_slider ( float ): kg of rebar per m3 of concrete
    Returns:
        Tuple: (vol_conc, vol_rebar) volume of concrete and rebar respectively
    """
    # vol_rebar_ratio = rebar_slider / 7850
    vol_conc = (7850 * vol) / (7850 + rebar_slider)
    vol_rebar = vol - vol_conc
    return vol_conc, vol_rebar


def mat_interpreter(  # TODO: PLEASE REFACTOR THIS TO DICTIONARY TO SHORTEN THE CODE
    df: pd.DataFrame,
    beam_slider: float,
    column_slider: float,
    slab_slider: float,
    wall_slider: float,
    stair_slider: float,
    gb_conc=greenbook_options.concrete[11]["value"],
    epic_conc=epic_options.concrete[12]["value"],
    ice_conc=ice_options.concrete[28]["value"],
    gb_rebar=greenbook_options.rebar[0]["value"],
    epic_rebar=epic_options.rebar[0]["value"],
    ice_rebar=ice_options.rebar[0]["value"],
    gb_steel=greenbook_options.steel[1]["value"],
    epic_steel=epic_options.steel[1]["value"],
    ice_steel=ice_options.steel[1]["value"],
    gb_timber=greenbook_options.timber[1]["value"],
    epic_timber=epic_options.timber[1]["value"],
    ice_timber=ice_options.timber[1]["value"],
) -> tuple:
    """interprets the materials in the schedule

    Args:
        df ( pd dataframe ): uploaded schedule
        beam_slider ( float ): value of the beam slider
        column_slider ( float ): value of the column slider
        slab_slider ( float ): value of the slab slider
        wall_slider ( float ): value of the wall slider
        stair_slider ( float ): value of the stair slider

    Returns:
        tuple: (mat, vol, mass, floor) tuple of lists of mass, volume, material and floor
    """
    mass = []
    vol = []
    mat = []
    floor = []
    element = []
    gb_ec = []
    epic_ec = []
    ice_ec = []

    for i, row in df.iterrows():
        if re.search(
            r"(concrete)|(conc)", row["Materials"], re.IGNORECASE
        ) or re.search(r"(concrete)|(conc)", row["Layer"], re.IGNORECASE):
            # TODO: refactor the if statments
            # FIXME: there are too many repeating append statements

            # --------- check if the layer is BEAMS
            if re.search(
                r"(beam)|(BEAM)|(Beam)", row["Layer"], re.IGNORECASE
            ) or re.search(r"(beam)|(BEAM)|(Beam)", row["Materials"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Volume"], beam_slider)

                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                # mass.append( 2360 * vol_conc )  # 2360 is the density of average concrete density from EPiC
                mass.append(mass_conc := row["Mass"] - (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Beam")
                gb_ec.append(vol_conc * gb_conc)
                epic_ec.append(vol_conc * epic_conc)
                ice_ec.append(vol_conc * ice_conc)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := vol_rebar * 7850)
                floor.append(row["Levels"])
                element.append("Beam")
                gb_ec.append(mass_rebar * gb_rebar)
                epic_ec.append(mass_rebar * epic_rebar)
                ice_ec.append(mass_rebar * ice_rebar)

            # --------- Cheack if the layer is COLUMNS
            elif re.search(
                r"(column)|(COLUMN)|(Column)", row["Layer"], re.IGNORECASE
            ) or re.search(
                r"(column)|(COLUMN)|(Column)",
                row["Materials"],
                re.IGNORECASE,
            ):
                vol_conc, vol_rebar = find_vols(row["Volume"], column_slider)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(mass_conc := row["Mass"] - (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Column")
                gb_ec.append(vol_conc * gb_conc)
                epic_ec.append(vol_conc * epic_conc)
                ice_ec.append(vol_conc * ice_conc)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Column")
                gb_ec.append(mass_rebar * gb_rebar)
                epic_ec.append(mass_rebar * epic_rebar)
                ice_ec.append(mass_rebar * ice_rebar)

            # --------- Check if the layer is SLAB
            elif re.search(
                r"(slab)|(Slab)|(SLAB)", row["Layer"], re.IGNORECASE
            ) or re.search(r"(slab)|(Slab)|(SLAB)", row["Materials"], re.IGNORECASE):
                vol_conc, vol_rebar = find_vols(row["Volume"], slab_slider)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(
                    mass_conc := row["Mass"] - (vol_rebar * 7850)
                )  # (7850 * vol_rebar))
                floor.append(row["Levels"])
                element.append("Slab")
                gb_ec.append(vol_conc * gb_conc)
                epic_ec.append(vol_conc * epic_conc)
                ice_ec.append(vol_conc * ice_conc)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Slab")
                gb_ec.append(mass_rebar * gb_rebar)
                epic_ec.append(mass_rebar * epic_rebar)
                ice_ec.append(mass_rebar * ice_rebar)

            # --------- Check if the layer is WALLS
            elif re.match(r"(wall)|(walls)", row["Layer"], re.IGNORECASE) or re.match(
                "concrete", row["Materials"], re.IGNORECASE
            ):
                vol_conc, vol_rebar = find_vols(row["Volume"], wall_slider)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(
                    mass_conc := row["Mass"] - (vol_rebar * 7850)
                )  # (7850 * vol_rebar))
                floor.append(row["Levels"])
                element.append("Wall")
                gb_ec.append(vol_conc * gb_conc)
                epic_ec.append(vol_conc * epic_conc)
                ice_ec.append(vol_conc * ice_conc)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Wall")
                gb_ec.append(mass_rebar * gb_rebar)
                epic_ec.append(mass_rebar * epic_rebar)
                ice_ec.append(mass_rebar * ice_rebar)

            # --------- Check if the layer is STAIRS
            elif re.search(
                r"(stair)|(Stair)|(STAIR)", row["Layer"], re.IGNORECASE
            ) or re.search(
                r"(stair)|(Stair)|(STAIR)",
                row["Materials"],
                re.IGNORECASE,
            ):
                vol_conc, vol_rebar = find_vols(row["Volume"], stair_slider)
                # add concrete volume
                mat.append("Concrete")
                vol.append(vol_conc)
                mass.append(
                    mass_conc := row["Mass"] - (vol_rebar * 7850)
                )  # (7850 * vol_rebar))
                floor.append(row["Levels"])
                element.append("Stairs")
                gb_ec.append(vol_conc * gb_conc)
                epic_ec.append(vol_conc * epic_conc)
                ice_ec.append(vol_conc * ice_conc)

                # add rebar volume
                mat.append("Reinforcement Bar")
                vol.append(vol_rebar)
                mass.append(mass_rebar := (vol_rebar * 7850))
                floor.append(row["Levels"])
                element.append("Stairs")
                gb_ec.append(mass_rebar * gb_rebar)
                epic_ec.append(mass_rebar * epic_rebar)
                ice_ec.append(mass_rebar * ice_rebar)

        # Appends timber values from layer
        elif re.search("timber", row["Layer"], re.IGNORECASE) or re.search(
            "timber", row["Materials"], re.IGNORECASE
        ):
            mat.append("Structural Timber")
            vol.append(row["Volume"])
            mass.append(row["Mass"])
            floor.append(row["Levels"])
            element.append(
                element_check(row["Layer"])
            )  # TODO: add function to define what element is being used
            gb_ec.append(
                row["Volume"] * gb_timber
            )  # timber... assumes there no other materials types
            epic_ec.append(row["Volume"] * epic_timber)
            ice_ec.append(row["Mass"] * ice_timber)

        # Appends steel values from layer
        elif re.search("steel", row["Layer"], re.IGNORECASE) or re.search(
            "steel", row["Materials"], re.IGNORECASE
        ):
            mat.append("Structural Steel")
            # mat.append(row["Materials"])
            vol.append(row["Volume"])
            mass.append(row["Mass"])
            floor.append(row["Levels"])
            element.append(
                element_check(row["Layer"])
            )  # TODO: add function to define what element is being used
            gb_ec.append(
                row["Mass"] * gb_steel
            )  # timber... assumes there no other materials types
            epic_ec.append(row["Mass"] * epic_steel)
            ice_ec.append(row["Mass"] * ice_steel)
    return mat, vol, mass, floor, element, gb_ec, epic_ec, ice_ec


def element_check(layer: str) -> str:
    """finds and returns the correct building ele

    Args:
        layer ( String ): string that contains the building element

    Returns:
        String : string of the element
    """
    if re.search("column", layer, re.IGNORECASE):
        return "Column"
    elif re.search("beam", layer, re.IGNORECASE):
        return "Beam"
    elif re.search("slab", layer, re.IGNORECASE):
        return "Slab"
    elif re.search("wall", layer, re.IGNORECASE):
        return "Wall"
    elif re.search("stair", layer, re.IGNORECASE):
        return "Stairs"
    else:  # if no match is found
        return "Unknown"


def none_check(is_none):
    """Checks if is_none is None and returns 0.0 if so

    Args:
        is_none ( float ): The value to check

    Returns:
        flaot : The value of is_none if not None, 0.0 if None
    """

    if len(is_none) == 0:
        return 0
    else:
        return is_none.values[0]


def concrete(value, vol, source=material_options.concrete):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for concrete

    Args:
        value ( float ): value of the dropdown
        unit_value ( float ): value of the unit for concrete (Greenbook - Volume) (epic - Volume) (ice - Volume)
        source ( dict ): values of the dropdown and ec

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    if source == material_options.concrete:
        gb_submat = [x["gb_label"] for x in source if x["value"] == value][0]
        gb_val = [x["gb"] for x in source if x["value"] == value][0] * vol

        epic_submat = [x["epic_label"] for x in source if x["value"] == value][0]
        epic_val = [x["epic"] for x in source if x["value"] == value][0] * vol

        ice_submat = [x["ice_label"] for x in source if x["value"] == value][0]
        ice_val = [x["ice"] for x in source if x["value"] == value][0] * vol

        colors = [x["color"] for x in source if x["value"] == value][0]

        return gb_val, gb_submat, epic_val, epic_submat, ice_val, ice_submat, colors
    else:
        sub_material = [x["label"] for x in source if x["value"] == float(value)][0]
        new_colors = [x["color"] for x in source if x["value"] == float(value)][0]
        ec_value = float(value) * vol
        return sub_material, ec_value, new_colors


def rebar(value, unit_value, source=material_options.rebar):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for rebar

    Args:
        value ( float ): value of the dropdown
        unit_value ( float ): value of the unit for rebar (Greenbook - kilogram kg) (epic - kilogram kg) (ice - kilogram kg)

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    if source == material_options.rebar:
        gb_submat = [x["gb_label"] for x in source if x["value"] == value][0]
        gb_val = [x["gb"] for x in source if x["value"] == value][0] * unit_value

        epic_submat = [x["epic_label"] for x in source if x["value"] == value][0]
        epic_val = [x["epic"] for x in source if x["value"] == value][0] * unit_value

        ice_submat = [x["ice_label"] for x in source if x["value"] == value][0]
        ice_val = [x["ice"] for x in source if x["value"] == value][0] * unit_value

        colors = [x["color"] for x in source if x["value"] == value][0]

        return gb_val, gb_submat, epic_val, epic_submat, ice_val, ice_submat, colors
    else:
        sub_material = [x["label"] for x in source if x["value"] == float(value)][0]
        colors = [x["color"] for x in source if x["value"] == float(value)][0]
        ec_value = float(value) * unit_value
        return sub_material, ec_value, colors


def steel(value, unit_value, source=material_options.steel):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for steel

    Args:
        value ( float ): value of the dropdown
        unit_value ( float ): value of the unit for steel (Greenbook - kilogram kg) (epic - kilogram kg) (ice - kilogram kg)

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    if source == material_options.steel:
        gb_submat = [x["gb_label"] for x in source if x["value"] == value][0]
        gb_val = [x["gb"] for x in source if x["value"] == value][0] * unit_value

        epic_submat = [x["epic_label"] for x in source if x["value"] == value][0]
        epic_val = [x["epic"] for x in source if x["value"] == value][0] * unit_value

        ice_submat = [x["ice_label"] for x in source if x["value"] == value][0]
        ice_val = [x["ice"] for x in source if x["value"] == value][0] * unit_value

        colors = [x["color"] for x in source if x["value"] == value][0]

        return gb_val, gb_submat, epic_val, epic_submat, ice_val, ice_submat, colors
    else:
        sub_material = [x["label"] for x in source if x["value"] == float(value)][0]
        color = [x["color"] for x in source if x["value"] == float(value)][0]
        ec_value = float(value) * unit_value
        return sub_material, ec_value, color


def timber(value, mass, vol, source=material_options.timber, ice=False):
    """
    meant to work with callback below. This returns submaterial with ec value.
    This definition should be used in a dictionary.
    definition for timber

    Args:
        value ( float ): value of the dropdown
        unit_value ( float ): value of the unit for timber (Greenbook - Volume) (epic - Volume) (ice - Volume)

    Returns:
        str : sub-materials to be append
        float: embodied carbon value to be append
    """
    if source == material_options.timber:
        gb_submat = [x["gb_label"] for x in source if x["value"] == value][0]
        gb_val = [x["gb"] for x in source if x["value"] == value][0] * vol

        epic_submat = [x["epic_label"] for x in source if x["value"] == value][0]
        epic_val = [x["epic"] for x in source if x["value"] == value][0] * vol

        ice_submat = [x["ice_label"] for x in source if x["value"] == value][0]
        ice_val = [x["ice"] for x in source if x["value"] == value][0] * mass

        colors = [x["color"] for x in source if x["value"] == value][0]

        return gb_val, gb_submat, epic_val, epic_submat, ice_val, ice_submat, colors
    else:
        sub_material = [x["label"] for x in source if x["value"] == float(value)][0]
        colors = [x["color"] for x in source if x["value"] == float(value)][0]
        if ice is True:
            ec_value = float(value) * mass
            return sub_material, ec_value, colors
        else:
            ec_value = float(value) * vol
            return sub_material, ec_value, colors


def percent_diff(current, prev):
    """
    Calculates the percent difference between two values. Then return a dash dmc.Badge component.

    Args:
        current (float): current value
        prev (float): previous value

    Returns:
        Dash Component: returns a dmc.Badge() component with the percent difference of
    """

    percent = (current - prev) / (prev + current) * 100
    if percent > 0:
        return dmc.Badge(
            ["+" + str(np.around(percent, 1)) + "%"], variant="filled", color="yellow"
        )
    else:
        return dmc.Badge(
            [str(np.around(percent, 1)) + "%"], variant="filled", color="lime"
        )


class table:
    def __init__(
        self,
        id,
        concrete_options,
        rebar_options,
        steel_options,
        timber_options,
        db_name,
        concrete=0,
        rebar=0.0,
        steel=0.0,
        timber=0.0,
    ):
        self.id = id
        self.concrete_options = concrete_options
        self.rebar_options = rebar_options
        self.steel_options = steel_options
        self.timber_options = timber_options
        self.conc_val = concrete
        self.rebar_val = rebar
        self.steel_val = steel
        self.timber_val = timber
        self.db_name = db_name

    def table_gen(self):
        table_head = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Materials"),
                        html.Th("Embodied Carbon", style={"width": "30%"}),
                    ]
                )
            )
        ]
        options = [
            self.concrete_options,
            self.rebar_options,
            self.steel_options,
            self.timber_options,
        ]
        mat_val = [
            self.conc_val,
            self.rebar_val,
            self.steel_val,
            self.timber_val,
        ]
        labels = [
            {"name": "Concrete", "value": self.conc_val},
            {"name": "Reinforcement Bar", "value": self.rebar_val},
            {"name": "Structural Steel", "value": self.steel_val},
            {"name": "Structural Timber", "value": self.timber_val},
        ]
        rows = []

        for i, options in enumerate(options):
            mat_row = html.Tr(
                [
                    html.Td(
                        dbc.Row(
                            [
                                dbc.Col(
                                    children=dmc.Text(labels[i]["name"]),
                                    class_name="w-25",
                                ),
                                dbc.Col(
                                    children=dbc.Select(
                                        id="sel-custom-{}-{}-{}".format(
                                            self.db_name,
                                            self.id,
                                            labels[i]["name"].replace(" ", "-"),
                                        ),
                                        options=options,
                                        value=labels[i]["value"],
                                        persistence=True,
                                    )
                                ),
                            ]
                        )
                    ),
                    html.Td(
                        mat_val[i],
                        id="{}-val-custom-{}-{}".format(
                            self.db_name, self.id, labels[i]["name"].replace(" ", "-")
                        ),
                    ),
                ]
            )

            rows.append(mat_row)
        return dbc.Table(table_head + [html.Tbody(rows, className="w-75")])


def create_data(x, label):
    x = x.drop(["Element"], axis=1)
    values = x.values
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    row_label = html.Tr([html.Td(label, rowSpan=len(x) + 1)])
    return [row_label] + rows


def create_table(x):
    x.rename(
        columns={
            "Mass": "Mass (kg)",
            "Volume": "Volume (m³)",
            "Green Book EC": "Green Book (kgCO₂e)",
            "Epic EC": "EPiC (kgCO₂e)",
            "Ice EC": "Ice (kgCO₂e)",
        },
        inplace=True,
    )
    columns = x.columns
    header = [html.Tr([html.Th(col) for col in columns])]
    beam = create_data(x.loc[x["Element"] == "Beam"], "Beam")
    column = create_data(x.loc[x["Element"] == "Column"], "Column")
    slab = create_data(x.loc[x["Element"] == "Slab"], "Slab")
    walls = create_data(x.loc[x["Element"] == "Wall"], "Wall")
    stair = create_data(x.loc[x["Element"] == "Stairs"], "Stairs")

    rows = column + beam + slab + walls + stair
    table = [html.Thead(header), html.Tbody(rows)]

    return table
