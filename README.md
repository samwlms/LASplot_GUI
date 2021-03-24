# LASplot - *LiDAR Visualization Tools*
### Multipurpose LiDAR analysis software built with Python (using Tkinter framework and Laspy)

![terrain image](https://github.com/samwlms/LASplot_GUI/blob/main/images/terrain.PNG)

## Overview
LASplot is an ongoing work-in-progress and learning exercise which I have undertaken in order to improve my Python programming skills, while also learning more about LiDAR technologies. I am aware that there are many existing (more powerful) tools out there that can do much of what LASplot does. Please feel free to fork the main branch and add any features you'd like. I am more than open to feedback and collaboration.

For any questions/ concerns/ feedback about the software, shoot me an email me at: swilliams9@uon.edu.au

### Running LASplot - requirements and information

###### _**How to run the LASplot application on your machine**_

Installing and running the application on Windows operating systems is as simple as clicking **LASplot_launcher.bat**.
The launcher will check to see if the virtual environment and dependencies have been installed, and if they haven't; it will perform the necessary installation process (-m venv & pip install). If the program has previously installed these dependencies, the launcher will boot straight into LASplot.

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/installer.png)


###### _NOTE: System must have Python 3 at minimum as the installation process utilises the VENV module (included by default in Python 3). When running the program on Mac or Linux you will have to set up the virtual environment manually. Use the requirements.txt file to gather required modules and then launch the LASplot.py file found in /python._

## Visualization options

### Point classification separation and plot:
###### *Speed: fast (0.2 - 0.5s)*
Allows users the ability to quickly visualise individual classification layers for the purposes of *per tile* quality control and QA.

Use cases include:
- quickly assessing high-vegetation and building noise contamination
- viewing the relative makeup of the file (residential, rural, city, etc.)

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/plot.PNG)

### Composite image generation
###### *Speed: fast (0.3 - 0.8s)*
Using the layer selection pane, users can generate custom images with various LAS classifications included in the plot. These composite images provide a much more complete view of the tile - and allow for a quick snapshot of the file as a whole. 

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/composite.png)


### Shaded vegetation option
###### *Speed: med-slow (2 - 10s)*
LASplot can now generate shaded vegetation imagery. The algorithm will shade high vegetation points on a colour gradient by considering their individual distance from ground. This option takes a little longer to generate images (depending on number of veg points / PC compute power), but is still quite optimized for a Python approach. By utilizing the spatial query functionality of [cKDtree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html), we can bypass the Python GIL and use all available CPU cores to handle computation. With the inbuilt GUI image generation arguments (DPI + Size), it is possible to generate useful snapshots for analysis at any scale.

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/shaded_veg.png)


### Ground layer terrain analysis:
###### *Speed: med (2 - 4s)*

_**With the following options, users may visualise both relative and/ or absolute variance in terrain elevation**_

##### Gradient
_Represents the relative changes in ground elevation by marking elevation changes between the highest and lowest points on a given tile. The highest point on the tile will always be red (255, 0, 0), and conversely the lowest point will always be blue (0, 0, 255)_

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/gradient.PNG)

Using the gradient functionality / option in the GUI, users are ables to quickly evaluate the relative changes in terrain elevation. The basic theory behind the gradient function is as follows:
- The ground layer is split into X number of distinct bands determined by the Z value of each point record.
- X number of tuples are generated which contain the appropriate RGB values corresponding to the relative elevation delta of the distinct bands. (blue for low elevation | red for high elevation)
- The terrain bands and colour bands are 'zipped' and plotted to an output image of user specification (number of bands, DPI, size)

*The RGB evaluation for distinct colour bands can be loosely described with the following image*

![colour theory image](https://github.com/samwlms/LASplot_GUI/blob/main/images/RGB_value_relationships.png)

##### Contour
_Represents the elevation changes within a tile that are characterized by distinct (user defined) elevation intervals. The highest and lowest points of a file are not considered, therefore: a near flat tile will be represented using a single colour._

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/contour.png)

Using the contour function, users may specify a band height (in meters) and break the input file into distinct bands. This allows for analysis of absolute terrain height changes across the tile.

### Ground intensity analysis:
###### *Speed: med (2 - 4s)*

**With the following options, users may visualize the return intensity for point records within a file. This is useful for identifying road features and changes in ground layer terrain makeup**

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/intensity.png)


## Output settings for PNG files

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
- [x] 'shaded vegetation' *high vegetation layer with points shaded according to their distance from ground*
- [x] 'terrain gradient' *elevation gradient showing a the high and low points of the file*
- [x] 'terrain intensity' *representation of the point record intensity associated with ground classification*
- [x] 'terrain contour' *(2 color) banding to reflect relative changes in local ground elevation*
- [x] 'composite image' *main classification layers painted in appropriate colours (single image)*
- [x] 'file information' *general information about the file and header specifications*

![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_settings.PNG)

### Laspy tools integration:

_**Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)***_

- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Header validation
