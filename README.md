![app icon](https://github.com/samwlms/LASplot_GUI/blob/main/contour.png)

## LASplot - *LIDAR visualisation and analysis toolset*

Multipurpose LIDAR analysis GUI built using the Tkinter framework

LASplot gives users a quick and easy way to generate various types of imagery from a LAS file

>**Point classification seperation and plot:**
- [x] Quickly visualise 1 file *(Normal output + QA Mode)*
- [ ] For n files: plot

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/screenshot_plot.PNG)

>**Ground layer terrain analysis:**
- [x] Colour banding to indicate changes in ground elevation

![contour image](https://github.com/samwlms/LASplot_GUI/blob/main/screenshot_contour.PNG)

>**Laspy tools integration:**
- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Validate

**Custom output settings for image files**

User controls to change the output configuration of generated .PNG files.

Individually manange:
- 'Size' *the relative x,y pixel scale of the file*
- 'DPI' *the granular detail of the output image*

With options to generate:
- 'plots' *individual layers, seperated by classification*
- 'ground contour' *color banded imagery to reflect changes in ground elevation*
- 'file information' *general information about the file and header specifications*

![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/screenshot_settings.PNG)


## Python powered data handling

Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)*