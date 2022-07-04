import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash_iconify import DashIconify

building_type = [
    {
        "label": "Class 2 Residential - Premium(>25m)",
        "value": "2_premium",
    },
    {"label": "Class 2 - Multi-residential", "value": "2_multi-res"},
    {"label": "Class 5 Office - Premium", "value": "5_premium"},
    {"label": "Class 5 Office - A Grade", "value": "5_a_grade"},
    {"label": "Class 6 Retail - Regional", "value": "6_regional"},
    {"label": "Class 6 Retail - Sub Regional", "value": "6_sub_regional"},
]

leti_type = [
    {"label": "Small House", "value": "sh"},
    {"label": "Medium House", "value": "mh"},
    {"label": "Schools", "value": "school"},
    {"label": "Commercial Offices", "value": "co"},
]

leti_option = {
    "sh": "Small House",
    "mh": "Medium House",
    "school": "Schools",
    "co": "Commercial Offices",
}


def leti(bld_type):
    leti = {"sh": 150, "mh": 230, "school": 180, "co": 288}
    return leti.get(bld_type, 0)
