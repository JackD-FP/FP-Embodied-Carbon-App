import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP] #dbc theme

app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    meta_tags=[{ #for mobile bs 
        'name': 'viewport',
        'content': 'width=device-width, intial-scale=1.0'
    }]
    )
server = app.server
app._favicon = ("assets/favicon.ico")