from dash import Input, Output, State, dcc, html, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def table_gen(
    conc_input, conc_out, steel_input, steel_out, timber_input, timber_output
):
    table_header = [
        html.Thead(html.Tr([html.Th("Material Name"), html.Th("Embodied Carbon")]))
    ]

    row1 = html.Tr([html.Td(conc_input), html.Td(conc_out)])
    row2 = html.Tr([html.Td(steel_input), html.Td(steel_out)])
    row3 = html.Tr([html.Td(timber_input), html.Td(timber_output)])

    table_body = [html.Tbody([row1, row2, row3])]

    return dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)
