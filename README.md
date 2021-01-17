# LASplot - *LIDAR visualisation tools*
## Multipurpose LIDAR analysis GUI built using the Python (Tkinter framework)

### Overview
LASplot is an ongoing work-in-progress and learning excersize which I have undertaken in order to improve my Python programming skills, while also learning more about LIDAR technologies. I am aware that there are many existing (more powerful) tools out there that can do much of what LASplot does. Please feel free to fork the main branch and add any features you'd like. I am more than open to feedback and collaboration.

For any questions/ concerns/ feedback about the software, shoot me an email me at: swilliams9@uon.edu.au

![app icon](https://github.com/samwlms/LASplot_GUI/blob/main/images/contour.png)

### Point classification separation and plot:
Allows users the ability to quickly visualise individual classification layers for the purposes of *per tile* quality control and QA. Use cases include:
- quickly assessing high-vegetation and building noise contamination
- viewing the relative 

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_plot.PNG)

### Ground layer terrain analysis:

##### With the following options, users may visualise both relative and/ or absolute variance in terrain elevation

> #### Gradient
###### Represents the relative changes in ground elevation by marking elevation changes between the highest and lowest points on a given tile. The highest point on the tile will always be red (255, 0, 0), and conversely the lowest point will always be blue (0, 0, 255)

![gradient image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_contour.PNG)

Using the gradient functionality / option in the GUI, users are ables to quickly evaluate the relative changes in terrain elevation. The basic theory behind the gradient function is as follows:
- The ground layer is split into X number of distinct bands determined by the Z value of each point record.
- X number of tuples are generated which contain the appropriate RGB values corresponding to the relative elevation delta of the distinct bands. (blue for low elevation | red for high elevation)
- The terrain bands and colour bands are 'zipped' and plotted to an output image of user specification (number of bands, DPI, size)

*The RGB evaluation for distinct colour bands can be loosely described with the following image*

![colour theory image](https://github.com/samwlms/LASplot_GUI/blob/main/images/RGB_value_relationships.png)

> #### Contour
###### Represents the elevation changes within a tile that are characterised by distinct (user defined) elevation intervals. The highest and lowest points of a file are not considered, therefore: a near flat tile will be represented using a single colour.


### Custom output settings for PNG files

User controls to change the output configuration of generated images

General image options:
- 'Size' *the output size of the file (in inches)*
- 'DPI' *the detail of the output image*
- 'Preview size' *the size of the image rendered in the window (in pixels)*

Plot options:
- Select which layers to plot *(based on LAS point record classification)*

With options to generate the following image files:
- [x] 'plots' *individual layers, seperated by LAS classification*
- [x] 'terrain gradient' *elevation gradient showing a the high and low points of the file*
- [ ] 'terrain contour' *(2 color) banding to reflect relative changes in local ground elevation*
- [ ] 'composite image' *main classification layers painted in appropriate colours (single image)*
- [x] 'file information' *general information about the file and header specifications*

![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_settings.PNG)

### Laspy tools integration:

Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)*

- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Header validation
