# LASplot - *LiDAR visualisation tools*
## Multipurpose LiDAR analysis software built with Python (using Tkinter framework and Laspy)

![terrain image](https://github.com/samwlms/LASplot_GUI/blob/main/images/terrain.PNG)

## Overview
LASplot is an ongoing work-in-progress and learning exercise which I have undertaken in order to improve my Python programming skills, while also learning more about LiDAR technologies. I am aware that there are many existing (more powerful) tools out there that can do much of what LASplot does. Please feel free to fork the main branch and add any features you'd like. I am more than open to feedback and collaboration.

For any questions/ concerns/ feedback about the software, shoot me an email me at: swilliams9@uon.edu.au

## Running LASplot - requirements and information

_**How to run the LASplot application on your machine**_

### Installation

If you are running the application for the first time, simply click on **'install.bat'** to initialise the application virtual environment, and install necessary dependencies.

### Running the application
Once installed, the standard launch point for the application is **'run_program.bat'**. Using this method will run LASplot from the python virtual environment and help ensure cross-system compatibility.

##### _NOTE: System must have Python 3 at minimum as the installation process utilises the VENV module (included by default in Python 3)_

## Point classification separation and plot:
Allows users the ability to quickly visualise individual classification layers for the purposes of *per tile* quality control and QA. Use cases include:
- quickly assessing high-vegetation and building noise contamination
- viewing the relative makeup of the file (residential, rural, city, etc.)

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/plot.PNG)

## Shaded vegetation option

LASplot can now generate shaded vegetation imagery. The algorithm will shade high vegetation points on a colour gradient by considering their individual distance from ground. This option takes a little longer to generate images (approx 10 seconds, depending on specified output arguments), but is still quite optimized for a Python approach. Using the inbuilt GUI image generation arguments (DPI + Size), it is possible to generate useful snapshots for analysis at any scale.

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/shaded_veg.png)


## Ground layer terrain analysis:

_**With the following options, users may visualise both relative and/ or absolute variance in terrain elevation**_

#### Gradient
_Represents the relative changes in ground elevation by marking elevation changes between the highest and lowest points on a given tile. The highest point on the tile will always be red (255, 0, 0), and conversely the lowest point will always be blue (0, 0, 255)_

![gradient image](https://github.com/samwlms/LASplot_GUI/blob/main/images/gradient.PNG)

Using the gradient functionality / option in the GUI, users are ables to quickly evaluate the relative changes in terrain elevation. The basic theory behind the gradient function is as follows:
- The ground layer is split into X number of distinct bands determined by the Z value of each point record.
- X number of tuples are generated which contain the appropriate RGB values corresponding to the relative elevation delta of the distinct bands. (blue for low elevation | red for high elevation)
- The terrain bands and colour bands are 'zipped' and plotted to an output image of user specification (number of bands, DPI, size)

*The RGB evaluation for distinct colour bands can be loosely described with the following image*

![colour theory image](https://github.com/samwlms/LASplot_GUI/blob/main/images/RGB_value_relationships.png)

#### Contour
_Represents the elevation changes within a tile that are characterised by distinct (user defined) elevation intervals. The highest and lowest points of a file are not considered, therefore: a near flat tile will be represented using a single colour._

## Ground intensity analysis:

**With the following options, users may visualise the return intensity for point records within a file. This is useful for identifying road features and changes in ground layer terrain makeup**

![intensity image](https://github.com/samwlms/LASplot_GUI/blob/main/images/intensity.png)


## Custom output settings for PNG files

_**User controls to change the output configuration of generated images**_

General image options:
- 'Size' *the output size of the file (in inches)*
- 'DPI' *the detail of the output image*
- 'Preview size' *the size of the image rendered in the window (in pixels)*

Plotting marker options:
- Pixel (plot each point as a single pixel)
- Point (plot each point as a small, fixed size point)
- Circle (larger plots in shape of a circle)
- Square (larger points in shape of a square)

Plot options:
- Select which layers to plot *(based on LAS point record classification)*

With options to generate the following image files:
- [x] 'plots' *individual layers, separated by LAS classification*
- [x] 'terrain gradient' *elevation gradient showing a the high and low points of the file*
- [x] 'terrain intensity' *representation of the point record intensity associated with ground classification*
- [ ] 'terrain contour' *(2 color) banding to reflect relative changes in local ground elevation*
- [ ] 'composite image' *main classification layers painted in appropriate colours (single image)*
- [x] 'file information' *general information about the file and header specifications*

![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_settings.PNG)

### Laspy tools integration:

_**Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)***_

- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Header validation

