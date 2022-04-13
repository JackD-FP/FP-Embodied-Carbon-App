import re

import numpy as np
import pandas as pd
from config import graph_colors

gb_df = pd.read_csv("src/Greenbook _reduced.csv")
epic_df = pd.read_csv("src/epic _reduced.csv")
ice_df = pd.read_csv("src/ice _reduced.csv")


def total_ec_comparison(base, val1, val2, val1_db, val2_db):
    str = [
        checker(base, val1, val1_db,),
        "\n",
        checker(base, val2, val2_db),
    ]
    return str

def checker(base, val, val_db):
    if base <=  val:
        val1_percent = (val/base) * 100
        return "{} is 🔺 by +{:,.2f}%, ".format(val_db, val1_percent)
    else:
        val1_percent = (val/base) * 100
        return "{} is 🔻 by {:,.2f}%".format(val_db, val1_percent)

def find(df, ice):

    structure_concrete = 0
    structure_steel = 0
    structure_timber = 0

    if ice != True:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete = row["Volume (Net)"]
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel = row["Mass"]
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber = row["Volume (Net)"]
            else:
                pass
    else:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete = row["Volume (Net)"]
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
                structure_concrete.append(row["Volume (Net)"])
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel.append(row["Mass"])
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber.append(row["Volume (Net)"])
            else:
                pass
    else:
        for index, row in df.iterrows():
            if re.search("concrete", row["Building Materials (All)"], re.IGNORECASE):
                structure_concrete.append(row["Volume (Net)"])
            elif re.search("steel", row["Building Materials (All)"], re.IGNORECASE):
                structure_steel.append(row["Mass"])
            elif re.search("timber", row["Building Materials (All)"], re.IGNORECASE):
                structure_timber.append(row["Mass"])
            else:
                pass
    return structure_concrete, structure_steel, structure_timber


def label_colours_update(l, type_):
    color_list = []
    color_dict = {}
    if type_ == "list":

        for i, iter in enumerate(l):
            if re.search("concrete", iter, re.IGNORECASE):
                color_list.append(graph_colors[0])
            elif re.search("steel", iter, re.IGNORECASE):
                color_list.append(graph_colors[1])
            elif re.search("timber", iter, re.IGNORECASE):
                color_list.append(graph_colors[2])
        return color_list

    else :

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

        return color_dict


'''
        ADD OTHER MATERIALS LIKE ALUMINIUM AND BRICK!!! (╯‵□′)╯︵┻━┻
        - create flexibilities for other materials
'''

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

    df = df.groupby(by=['Building Materials (All)'], as_index=False).sum() # create consolidated df
    volumes = df["Volume (Net)"].tolist()
    df_mat = df["Building Materials (All)"].tolist()
    mass = df["Mass"].tolist()

    gb_embodied_carbon = []
    epic_embodied_carbon = []
    ice_embodied_carbon = []

    for i, mat in enumerate(df_mat):
        # if mat == "CONCRETE - IN-SITU":
        if re.search("concrete", mat, re.IGNORECASE):
            gb_embodied_carbon.append(volumes[i]*conc_val) #Concrete 50 MPa || Green Book
            epic_embodied_carbon.append(volumes[i]*conc_val) #Concrete 40 MPa || Epic 
            ice_embodied_carbon.append(volumes[i]*conc_val) # Concrete 50 MPa || Ice
        # elif mat == "STEEL - STRUCTURAL":
        elif re.search("steel", mat, re.IGNORECASE):
            gb_embodied_carbon.append(mass[i]*steel_val) #Steel Universal Section || Green Book
            epic_embodied_carbon.append(mass[i]*steel_val) #Steel structural steel section || Epic  
            ice_embodied_carbon.append(mass[i]*steel_val) # steel Section|| Ice
        # elif mat == "TIMBER - STRUCTURAL":
        elif re.search("timber", mat, re.IGNORECASE):
            gb_embodied_carbon.append(volumes[i]*timber_val) #Glue-Laminated Timber (Glu-lam) || Green Book
            epic_embodied_carbon.append(volumes[i]*timber_val) #Glued laminated timber (glulam) || Epic 
            ice_embodied_carbon.append(mass[i]*timber_val) # Timber Gluelam || Ice
        else: # if all else fail assume concrete
            gb_embodied_carbon.append(volumes[i]*conc_val) # Green Book
            epic_embodied_carbon.append(volumes[i]*conc_val) # Epic
            ice_embodied_carbon.append(volumes[i]*conc_val) # Ice       

    if db == "gb":
        return gb_embodied_carbon
    elif db == "epic":
      return epic_embodied_carbon
    elif db == "ice":
        return ice_embodied_carbon
