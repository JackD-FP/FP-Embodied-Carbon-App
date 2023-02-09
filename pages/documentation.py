import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html
from dash_iconify import DashIconify

header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Levels"),
                html.Th("Layer"),
                html.Th("Mass"),
                html.Th("Volume"),
                html.Th("Materials"),
            ]
        )
    )
]


row1 = html.Tr(
    [
        html.Td("Ground Level"),
        html.Td("Column - Timber"),
        html.Td("123456"),
        html.Td("123456"),
        html.Td("TIMBER - STRUCTURAL"),
    ]
)
row2 = html.Tr(
    [
        html.Td("Ground Level"),
        html.Td("Column - Timber"),
        html.Td("123456"),
        html.Td("123456"),
        html.Td("TIMBER - STRUCTURAL"),
    ]
)
row3 = html.Tr(
    [
        html.Td("Ground Level"),
        html.Td("Column - Timber"),
        html.Td("123456"),
        html.Td("123456"),
        html.Td("TIMBER - STRUCTURAL"),
    ]
)
row4 = html.Tr(
    [
        html.Td("Ground Level"),
        html.Td("Column - Timber"),
        html.Td("123456"),
        html.Td("123456"),
        html.Td("TIMBER - STRUCTURAL"),
    ]
)
row5 = html.Tr(
    [
        html.Td("Ground Level"),
        html.Td("Column - Timber"),
        html.Td("123456"),
        html.Td("123456"),
        html.Td("TIMBER - STRUCTURAL"),
    ]
)

body = [html.Tbody([row1, row2, row3, row4, row5])]


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
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5(
                                    "Download Example Schedule File:",
                                    className="display-5 mt-5 fs-4",
                                    style={"textAlign": "center"},
                                ),
                                dbc.Button(
                                    "All Concrete Schedule.xlsx",
                                    id="all_concrete_btn",
                                    outline=True,
                                    color="primary",
                                    className="my-3 d-block mx-auto",
                                    style={"display": "block", "margin": "Auto"},
                                ),
                                dbc.Button(
                                    "All Timber Schedule.xlsx",
                                    id="all_timber_btn",
                                    outline=True,
                                    color="primary",
                                    className="my-3 d-block mx-auto",
                                    style={"display": "block", "margin": "Auto"},
                                ),
                                dbc.Button(
                                    "Concrete & Timber Schedule.xlsx",
                                    id="mix_btn",
                                    outline=True,
                                    color="primary",
                                    className="my-3 d-block mx-auto",
                                    style={"display": "block", "margin": "Auto"},
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H5(
                                    "Download Example Archicad Template File:",
                                    className="display-5 mt-5 fs-4",
                                    style={"textAlign": "center"},
                                ),
                                dbc.Button(
                                    "Example Archicad Template.yml",
                                    id="download2_btn",
                                    outline=True,
                                    color="primary",
                                    className="my-3 d-block mx-auto",
                                    style={"display": "block", "margin": "Auto"},
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Download(id="download_all_concrete"),
                dcc.Download(id="download_all_timber"),
                dcc.Download(id="download_mix"),
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
                        html.Strong('hates empty cells in "Material"'),
                        ". The best way to ensure that this does not happen is to have ",
                        html.Strong("materials assigned to all elements"),
                        ". You can also filter it out in the Components Schedule or delete it on Excel. \
            Another thing to note is that the App looks for key words such as ",
                        html.Strong("as concrete, steel and timber"),
                        ". Because of this, materials such as sketch-black, terracotta and etc, will just be considered as concrete.",
                    ]
                ),
                html.H3("The Embodied Carbon App", className="display-4, mt-5"),
                html.Hr(className="mb-5"),
                dmc.Blockquote(
                    "**We've tried to make this as generic as possible so that it can be adapted to any BIM software. However, as a disclaimer – we work in ArchiCAD, so please forgive the vocabulary!",
                    cite="- Wiley the office puppy",
                ),
                html.P(
                    "In order for the App to be correctly read, your dataset should be formatted as below:  "
                ),
                dmc.Table(header + body),
                dmc.Blockquote(
                    children=[
                        html.H3("Important Notes"),
                        dcc.Markdown(
                            """
                            the first two rows are headers, with the actual data starting in the third row 
                            - Columns must have identical headings to the above (case sensitive) 
                            - **Level** - Used for floor-by-floor analysis 
                            - **Layer** - Each element must contain one of the following in its name: 'Beam', 'Column', 'Slab', 'Wall' or 'Stair'. (not case sensitive) Note: For some software this could be the element classification 
                            - **Mass** & **Volume** - Both columns are used for calculations as sometimes the databases use differing units 
                            - **Material** - Used to separate out elements in addition to Classification
                            """
                        ),
                    ],
                    icon=[DashIconify(icon="akar-icons:triangle-alert", width=30)],
                    color="red",
                    class_name="my-5",
                ),
                dcc.Markdown(
                    """
                    The Embodied Carbon App results will only ever be as accurate as your data/model. So to maximise accuracy, we'd recommend conducting some model audits before exporting.  
                    Exactly how this is done is very dependent on your software, but as a quick guide, this is what we did (in ArchiCAD): 
                    - Isolate the materials in the model to more easily conduct a visual check of steel/concrete/timber. This was done with a series of corresponding layer combinations
                    - Set up a series of schedules and 3d views (based on same layer combinations) with graphic overrides ato easily conduct a visual check of the structural elements
                    Some specific things you might need to look out for: 
                    - Overlapping elements - eg slabs/beams/columns - are they being calculated more than once?
                    - Objects on incorrect layers/classification/etc - depending on how your final schedule is collated, there may be extraneous or missing items 
                    - Consistent material names
                    **A few things to note **
                    Staging/renovation status: demolished/existing/new elements are not differentiated. So, to separate these out youlll need to have separate datasets.  
                    """
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
    Input("download2_btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n, n2):
    return dcc.send_file(
        "./assets/Structure Schedule Template.xml",
    )


@callback(
    Output("download_all_concrete", "data"),
    Input("all_concrete_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_schedule_conc(n_conc):
    if n_conc:
        return dcc.send_file("./assets/Option 1 - All Concrete.xlsx")


@callback(
    Output("download_all_timber", "data"),
    Input("all_timber_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_schedule_timber(n_timber):
    if n_timber:
        return dcc.send_file("./assets/Option 2 - All Timber.xlsx")


@callback(
    Output("download_mix", "data"),
    Input("mix_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_schedule(n_mix):

    if n_mix:
        return dcc.send_file(
            "./assets/Option 3 - Timber Structure, Conc Core 6x8.5 Grid).xlsx"
        )
