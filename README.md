
# LASplot - *LIDAR visualisation tools*

### Multipurpose LIDAR analysis GUI built using the Tkinter framework


![app icon](https://github.com/samwlms/LASplot_GUI/blob/main/images/contour.png)

>## **Point classification seperation and plot:**
- [x] Quickly visualise 1 file

![GUI image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_plot.PNG)

>## **Ground layer terrain analysis:**
- [x] Colour banding to indicate changes in ground elevation

![gradient image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_contour.PNG)

>## **Laspy tools integration:**
- [ ] Compress/ Decompress data (LAS <-> LAZ)
- [ ] Validate

**Custom output settings for PNG files**

User controls to change the output configuration of generated images

General image options:
- 'Size' *the output size of the file (in inches)*
- 'DPI' *the detail of the output image*
- 'Preview size' *the size of the image rendered in the window (in pixels)*

Plot options:
- *Select which layers to plot*



With options to generate:
- 'plots' *individual layers, seperated by classification*
- 'ground gradient' *elevation gradient showing a the high and low points of the file*
- 'ground contour' *(2 color) banding to reflect relative changes in local ground elevation*
- 'composite image' *main classification layers painted in appropriate colours (single image)*
- 'file information' *general information about the file and header specifications*

![controls image](https://github.com/samwlms/LASplot_GUI/blob/main/images/screenshot_settings.PNG)


## Python powered data handling

Las specific data processing is handled by *[Laspy](https://laspy.readthedocs.io/en/latest/)*