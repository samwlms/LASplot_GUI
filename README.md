![app icon](https://github.com/samwlms/LASplot_GUI/blob/main/icon.png)
## LASplot - *Fast LIDAR visualisation and QA*

Python based GUI which utilises the Tkinter framework for application development.

This application has been built to replace the 'LASharp' LIDAR analysis application which instead used windows forms and the .NET framework to built the GUI. Rather than having to worry about complex dataflow between the C# application and the Python backend logic.

**Processing speed:**
 - avg plot time of 3.1s / 6,000,000 point file (high end PC)

## Tkinter GUI

Application user interface built using the Python Tkinter Framework. 
All data processing is also handled with Python (using Laspy + Numpy to manipulate the point data)

>**Point classification seperation and plot:**
- [x] Quickly visualise 1 file *(Normal output + QA Mode)*
- [ ] For n files: plot

>**Ground layer terrain analysis:**
- [ ] Colour banding to indicate changes in ground elevation

>**Laspy tools integration:**
- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Validate


![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/screenshot_plot.png)


**Custom output settings for image files**

User controls to change the output configuration of generated .PNG files.

Individually manange:
- 'Size' *the relative x,y pixel scale of the file*
- 'DPI' *the granular detail of the output image*


![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/screenshot_settings.png)


## Python powered data handling

Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)*