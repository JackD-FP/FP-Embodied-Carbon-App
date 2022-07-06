# FP Embodied Carbon App

## Introduction
Welcome to the public github repo for the app. This is a variation of our internal app that does not have The Footprint Company's Green Book Database. Reason being is that it require a license to use it. 

The Embodied Carbon App is built to help architects and designers make informed in order to design a more sustainable building. It is obvious to us that timber is far less carbon intense than concrete and steel. However, when it comes to actual buildings where mixtures of Material are necessary for structural stability, the answer is less obvious. We should all strive to minimise our design's embodied carbon, but not compromise structural stability and design excellence. 

The App can help identify which material is carbon intense and check if there are alternatives less carbon intense to the later. It can also help identify what floor is causing the issue if a redesign or alteration is required. This app free and open source for anyone. At Fitzpatrick and Partners, we believe this is the way to help our industry move forward and achieve a better and sustainable tomorrow.

## Basic Usage
The App primarily uses schedules from your BIM program of choise. The files can either be a XLSX, XLS or CSV. Schedules should also look like the table below.

|Structure Schedule|   ||||
|   --- |          --- |    --- |      --- |  --- |
| Level | Layer        | Volume | Material | Mass |
| Ground| COLUMN4 - OPTION 4 |   1234 |  Timber  | 1234 |
| Ground| WALLS4 - OPTION 4   |   1234 |   concrete  | 1234 |
| Ground| BEAM4 - OPTION 4   |   1234 |  Timber  | 1234 |

There are a few gotchas with the schedule. first of all there's a header cell that contains "Structure Schedule" on the top. Archicad will always schedule out a header row even if you specified not to. So the app will Automatically remove it, but if it's not there then it will remove the column names.

This leads in to the next gotcha. The Column names are all case sensitive and need to be those names (Level, Layer, Volume, Material, Mass). If not then the app will not work.

Now that's explained let's explain what each of those column mean. 

Level, stands for floor level of that element. in ArchiCAD level would be "Home Story Name". 

As for Layer, this is the layer which the element is on, in your BIM program. Our naming conventions maybe different but the App will look for certain keyworks in that layer name. These keywords that it looks for are words like beam, column, slab, wall, stair, conc, concrete, timber and steel. The primary purpose of this column is to distinguish what these elements are and it does not need to be case sensitive. It also picks up materials just because sometimes people leave the materials out during sketch design or picks a "sketch white" material. 

Volume is the net volume of the element.

Mass is the mass of the element. To set this you can set up the mass through density of the material in the attribute manager in ArchiCAD. The densities of materials could be found in the [EPiC's database pdf](https://melbourne.figshare.com/ndownloader/files/30569184)

## Road Map



## Issues
|Isues|Description|
|---|---|
|Cleaning data| Create modal/drawer to setup the excel upload. a ui that tells which column names are which. |
| error logs | have a way to report error better. some way to pop up or download raised errors. |
## Resources
Here are the most common resources used to build the app. However, You can join the community and chat down at the discord server.

[Join and Chat with use in discord](https://discord.gg/vEcqYpmK)


| Titles          | Links |
| -----------     | ----------- |
| FP ECA          | PLACE LINK HERE       |
| EPiC Database   | [Click Me](https://msd.unimelb.edu.au/research/projects/current/environmental-performance-in-construction/epic-database)        |
|ICE Database|[Click Me](https://circularecology.com/embodied-carbon-footprint-database.html) |
|LETI| [Click Me](https://www.leti.london/)|
|Architects Declare AU| [Click Me](https://au.architectsdeclare.com/)|