import re
from config import graph_colors

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


def label_colours_update(l):
    color_list = []
    for i, iter in enumerate(l):
        if re.search("concrete", iter, re.IGNORECASE):
            color_list.append(graph_colors[0])
        elif re.search("steel", iter, re.IGNORECASE):
            color_list.append(graph_colors[1])
        elif re.search("timber", iter, re.IGNORECASE):
            color_list.append(graph_colors[2])
    return color_list