from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import  plotly.graph_objects as go
#from server import app

labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
          "Rest of World"]

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=[16, 15, 12, 6, 5, 4, 42], name="GHG Emissions"),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=[27, 11, 25, 8, 1, 3, 25], name="CO2 Emissions"),
              1, 2)
fig.add_trace(go.Pie(labels=labels, values=[23, 54, 65, 87, 8, 36, 5], name="CO2 Emissions"),
              2, 1)
fig.add_trace(go.Pie(labels=labels, values=[65, 23, 56, 48, 32, 56, 6], name="CO2 Emissions"),
              2, 2)
# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="Global Emissions 1990-2011",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='GHG', x=0.25, y=0.5, font_size=20, showarrow=False),
                 dict(text='CO2', x=0.75, y=0.5, font_size=20, showarrow=False)])

layout = html.Div([
    html.H1("Total Embodied Carbon", className="display-2 mb-5 "),
    html.Hr(),
    html.Div([
        html.Img(
            src="https://img.icons8.com/ios-filled/100/000000/under-construction.png", 
            alt="under construction icon"),
        html.H1("UNDER CONSTRUCTION! SOMETHING COOL WILL COME OUT SOON", className="text-center"),
        html.Img(
            src="https://img.icons8.com/ios-filled/100/000000/under-construction.png", 
            alt="under construction icon")
    ], className="hstack gap-3"),
    dcc.Graph(figure=fig, style={'height': '75vh'})
], id="tec-div")