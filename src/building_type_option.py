from dash import Input, Output, State, callback, dash_table, dcc, html
import dash_mantine_components as dmc
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

gb_types = {
    "2_premium": "Class 2 Residential - Premium(>25m)",
    "2_multi-res": "Class 2 - Multi-residential",
    "5_premium": "Class 5 Office - Premium",
    "5_a_grade": "Class 5 Office - A Grade",
    "6_regional": "Class 6 Retail - Regional",
    "6_sub_regional": "Class 6 Retail - Sub Regional",
}

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
    leti = {"sh": 500, "mh": 500, "school": 600, "co": 600}
    return leti.get(bld_type, 0)


def gb_benchmark(bld_type):
    gb_bm = {
        "2_premium": {
            "5 star": 870.0,
            "4 star": 1160.0,
            "3 star": 1450.0,
            "2 star": 1740.0,
            "1 star": 2090.0,
        },
        "2_multi-res": {
            "5 star": 590.0,
            "4 star": 790.0,
            "3 star": 990.0,
            "2 star": 1190.0,
            "1 star": 1390.0,
        },
        "5_premium": {
            "5 star": 900.0,
            "4 star": 1200.0,
            "3 star": 1500.0,
            "2 star": 1800.0,
            "1 star": 2100.0,
        },
        "5_a_grade": {
            "5 star": 480.0,
            "4 star": 640.0,
            "3 star": 800.0,
            "2 star": 960.0,
            "1 star": 1120.0,
        },
        "6_regional": {
            "5 star": 1290.0,
            "4 star": 1720.0,
            "3 star": 2150.0,
            "2 star": 2580.0,
            "1 star": 3010.0,
        },
        "6_sub_regional": {
            "5 star": 730.0,
            "4 star": 970.0,
            "3 star": 1220.0,
            "2 star": 1470.0,
            "1 star": 1720.0,
        },
    }
    return gb_bm.get(bld_type, 0)


def gb_benchmark_calc(value, benchmark):
    bld_type = gb_benchmark(value)

    if benchmark < bld_type["5 star"]:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
            ],
            style={"justifyContent": "center"},
        )
    elif benchmark < bld_type["4 star"]:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
            ],
            style={"justifyContent": "center"},
        )
    elif benchmark < bld_type["3 star"]:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
            ],
            style={"justifyContent": "center"},
        )
    elif benchmark < bld_type["2 star"]:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
            ],
            style={"justifyContent": "center"},
        )
    elif benchmark < bld_type["1 star"]:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
            ],
            style={"justifyContent": "center"},
        )
    else:
        return dmc.Group(
            [
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
                DashIconify(icon="ic:baseline-star-border", width=30),
            ],
            style={"justifyContent": "center"},
        )


def gb_benchmark_optimum(value, benchmark):
    bld_type = gb_benchmark(value)
    diff = benchmark - bld_type["5 star"]

    if diff < 0:
        return "Structure is 'Best Practice' design"
    else:
        return [
            "Reduce embodied carbon by ",
            html.Strong("{:.2f} kgCO2e".format(diff)),
            " for 5 stars",
        ]
