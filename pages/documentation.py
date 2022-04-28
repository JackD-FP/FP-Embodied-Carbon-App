import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html

layout = html.Div(
    [
        html.H1("How To...", className="display-2 mb-5 "),
        html.Hr(),
        html.Div(
            [
                html.H3("Introduction", className="display-4, mt-5"),
                html.Hr(className="mb-5"),
                html.P(
                    "The Embodied Carbon App is built to help architects and designers make informed decisions.\
            To aid in the design of a more sustainable building. \
            It is obvious to us that timber is far less carbon intense than concrete and steel.\
            However, when it comes to actual buildings where mixtures of materials are necessary for structural stability, the answer is less obvious. \
            The App can help identify which material is carbon intense and check if there are alternatives less carbon intense to the later. \
            It can also help identify what floor is causing the issue if a redesign or alteration is required. \
            In essense the app helps you interrogate your designs and find improvements that can be made. \
            We should all strive to minimise our design's embodied carbon, \
            hopefully this app can aid with that."
                ),
                html.P(
                    "This app free and open source for anyone. \
            At Fitzpatrick and Partners, we believe this is the way to help\
            our industry move forward and achieve a better and sustainable tomorrow."
                ),
                html.H3("Setting up ArchiCAD Schedule", className="display-4, mt-5"),
                html.Hr(className="mb-5"),
                html.P(
                    [
                        "To get started, open up any project with your ArchiCAD version of your choosing.\
            Once opened,",
                        html.Strong(" right click"),
                        " on",
                        html.Strong(' "Components"'),
                        "and click",
                        html.Strong(' "New Schedule…"'),
                        ". A new Scheme Settings should have opened.",
                    ]
                ),
                html.Img(
                    src="/assets/step_1.png",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    [
                        "Give the schedule it's ",
                        html.Strong("ID"),
                        " and",
                        html.Strong(" Name "),
                        "using your office standard. After which you click on the highlighted button to import a xml template.\
        The template should get you 50% there, however since most projects are vastly different\
        you may need to add more criteria to filter out more things. You can download the Template XML file below.",
                    ]
                ),
                dbc.Button(
                    "Download",
                    id="download_btn",
                    outline=True,
                    color="primary",
                    className="mb-3 d-block mx-auto",
                ),
                dcc.Download(id="download"),
                html.Img(
                    src="/assets/step_2.png",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    [
                        "Once you have set up the schedule you can save the schedule as an XLSX file or csv. To do this click ",
                        html.Strong("File > Save As"),
                        ", give the ",
                        html.Strong("schedule a name "),
                        "and do ",
                        html.Strong("not forget "),
                        "to choose",
                        html.Strong(" XLSX "),
                        "from the dropdown. After which you can click save",
                    ]
                ),
                html.Img(
                    src="/assets/step_3.png",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    "After creating a schedule, you are ready to upload. \
            You can drag the schedule into the dropzone \
            or click and navigate towards it.",
                    className="mt-5",
                ),
                html.Img(
                    src="/assets/upload.gif",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    [
                        "There are few ",
                        html.Span(
                            [
                                dmc.Tooltip(
                                    label=[
                                        dmc.Badge(
                                            "North American",
                                            variant="outline",
                                            color="yellow",
                                        ),
                                        html.Br(),
                                        dmc.Divider(class_name="my-1"),
                                        "A sudden unforeseen problem.",
                                    ],
                                    transition="fade",
                                    transitionDuration=300,
                                    transitionTimingFunction="ease",
                                    withArrow=True,
                                    children=[html.Strong("gotchas")],
                                ),
                            ]
                        ),
                        " that you may encounter when using the app and creating schedules for it.\
            The application is only as good as the model itself. A cleaner and well-maintained \
            model would make the experience seamless and better in general. \
            The most common problem is that the application ",
                        html.Strong('hates empty cells in "Building Materials (All)"'),
                        ". The best way to ensure that this does not happen is to have ",
                        html.Strong("materials assigned to all elements"),
                        ". You can also filter it out in the Components Schedule or delete it on Excel. \
            Another thing to note is that the App looks for key words such as ",
                        html.Strong("as concrete, steel and Timber"),
                        ". Because of this, materials such as sketch-black, terracotta and etc, will just be considered as concrete.",
                    ]
                ),
                html.H3("The Embodied Carbon App", className="display-4, mt-5"),
                html.Hr(className="mb-5"),
                html.P(
                    "There are 3 main pages to the application. \
            These are the Dashboard, Analysis and Comparison, \
            each of them has their unique usage and purpose. "
                ),
                html.P(
                    [
                        "To use the app, you can either drop the file in the box or click on it. \
            To upload your schedule or the ",
                        html.Strong("example schedule"),
                        " that we provided.",
                    ]
                ),
                dbc.Button(
                    "Download",
                    id="example_btn",
                    outline=True,
                    color="primary",
                    className="my-3 d-block mx-auto",
                ),
                dcc.Download(id="exmaple"),
                html.P(
                    [
                        html.Strong("Dashboard"),
                        " helps you see the overview of the whole structure's embodied carbon. \
            What material has is taking up most of the embodied carbon as well as compare the embodied \
            carbon with other databases like Green Book, Ice and EPiC.",
                    ]
                ),
                html.Img(
                    src="/assets/Dashboard.gif",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    [
                        html.Strong("Analysis"),
                        " provides an in-depth look to see the embodied \
            carbon of each floor and which material can you swap with. \
            As well as homing in or comparing to specific embodied carbon databases.",
                    ]
                ),
                html.Img(
                    src="/assets/Analysis.gif",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
                html.P(
                    [
                        "Finally ",
                        html.Strong("Comparison"),
                        ", where you can compare the project with other projects \
            or reuse the same project to see how other materials affect the carbon intensity.",
                    ]
                ),
                html.Img(
                    src="/assets/comparison.gif",
                    className="img-fluid w-75 d-block mx-auto mb-5",
                ),
            ],
            className="w-50",
            style={
                "display": "block",
                "margin": "auto",
            },
        ),
    ]
)


@callback(
    Output("download", "data"),
    Input("download_btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "./assets/Structure Schedule Template.xml",
    )


@callback(
    Output("exmaple", "data"),
    Input("example_btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "./example_schedule.xls",
    )
