from dash import dcc, html

markdown_layout = dcc.Markdown(
    """
        # Introduction
        Welcome to F+P Embodied Carbon Structure Calculator. This is a variation of our internal app that does not have The Footprint Company's Green Book Database, due to licensing requirements. 

        The Embodied Carbon App is built to help architects and designers make informed in order to design a more sustainable building. It is obvious to us that timber is far less carbon intense than concrete and steel. However, when it comes to actual buildings where mixtures of Material are necessary for structural stability, the answer is less obvious. We should all strive to minimise our design's embodied carbon, but not compromise structural stability and design excellence. 

        The App can help identify which material is carbon intense and check if there are alternatives less carbon intense to the latter. It can also help identify what floor is causing the issue, if a redesign or alteration is required. This app is free and open source for anyone. At Fitzpatrick and Partners, we believe this is the way to help our industry move forward and achieve a better and sustainable tomorrow.

        # The Purpose of the Tool
        This tool aims to achieve a number of things;
        1.	Grow the general knowledge of Embodied Carbon within the architectural community.
        2.	Compare early stage design options for the embodied carbon of different structural solutions.
        3.	Cause individual users to ask further questions about where the carbon is and what to do about reducing it.
        4.	Help to build an industry wide conversation on how to build better now!

        # A note about data sets
        You will notice once you extract data from this tool that the two data bases give markedly different data. 
        In light of the above aims the differences between the two data sets are less important than if we were seeking to benchmark or contrast numbers from one to the other. (this is not an aim of this tool).
        Below we give some pointers as to why and where to from here;

        # EPIC Database
        Developed by researchers at The University of Melbourne
        Published in 2019 
        The EPIC database uses a Hybrid method to arrive at an EPiC coefficient to define the kgCO2e/m2 of a given material;
        This Hybrid seeks to capture both bottom up process input and output data together with macro-economic impacts by sector.

        # ICE Database (Inventory of Carbon & Energy)
        Originally published in 2005 and last updated in Nov 2019
        Developed by researchers at the University of Bath in the UK
        The data in the ICE database is A1-A3 Cradle to Gate and is based on EN15804 data which harmonises the structure of EPD’s for all construction products.

        # F+P’s view
        Both data sets are generic in nature (they use aggregate data from multiple sources to generate an average) and as such cannot represent accurately the final numbers for a given project in a given location at a given point in time.
        In the upfront stages of developing a design our view is that due to the above there is no single source of truth, as early in the project so much of the buildings specific supply chain is unknown.
        Later on in the design development and procurement phases of a project, individual EPD’s based on internationally agreed standards such as ISO or EN standards can be used to build out a much more robust embodied carbon number, based on actuals specific to a given project.

        The industry has many voices dedicated to the discussion of the pro’s and cons of each methodology including industry groups such as BIPC, ALCAS, GBCA, RICS and MECLA to name a few.
        A local data set of generic data based on globally accepted methods such as EN 15804 or ISO 21930 standards would be ideal and we understand may be in the works.
        However this dataset doesn’t currently exist in Australia to the best of our knowledge. (If you know otherwise we would love to hear from you).

        Therefore in the absence of this current Australian data set we are showing both ICE and EPiC outputs in this tool. 
        We note that the methodology in ICE conforms to EN 15804 where EPiC has taken a different approach. 
        We hope that the above gives you some insight into our methodology and thought process to date.


        # Further Reading
        We would recommend;
        - Check out the datasets and backgrounds to both the ICE Database and EPiC and pick through their methodologies, 
        - Form your own view of the pros and cons,
        - Contrast their numbers for specific products with EPD’s for those products from manufacturers,
        - If you cannot find data from your preferred manufacturer ask them why not,
        - Take part in industry discussions with NABERS or MELCA or others,
        - Question everything.

    """,
    className="py-3",
)
