# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
import printer
import matplotlib.pyplot as plt


# get the positional data of points in a specified classification
def get_xy(in_points, classification):
    x = in_points.X[in_points.Classification == classification]
    y = in_points.Y[in_points.Classification == classification]
    return x, y


# plot the positional data and then save as PNG
def plot(input, output, size, dpi, classifications):

    # print console heading for process
    printer.plot_print()

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points
    las_specification = input_file.point_format.fmt

    # get the min/max X,Y values to normalise the plot scale
    x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
    y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

    # basic params for the plot function
    plt.rcParams["figure.facecolor"] = "black"

    # constant arguments used in the plot function (packed/ unpacked with '*')
    const_args = output, dpi, x_min, x_max, y_min, y_max, size

    for arg in classifications:
        if arg == 1:
            unclassified = get_xy(input_file, arg)
            save_plot(*unclassified, "/unclassified.png", "m", *const_args)
        elif arg == 2:
            ground = get_xy(input_file, 2)
            save_plot(*ground, "/ground.png", "SaddleBrown", *const_args)
        elif arg == 3:
            lowVeg = get_xy(input_file, 3)
            save_plot(*lowVeg, "/lowVeg.png", "LimeGreen", *const_args)
        elif arg == 4:
            medVeg = get_xy(input_file, 4)
            save_plot(*medVeg, "/mediumVeg.png", "Green", *const_args)
        elif arg == 5:
            highVeg = get_xy(input_file, 5)
            save_plot(*highVeg, "/highVeg.png", "DarkGreen", *const_args)
        elif arg == 6:
            buildings = get_xy(input_file, 6)
            save_plot(*buildings, "/buildings.png", "White", *const_args)
        elif arg == 9:
            water = get_xy(input_file, 9)
            save_plot(*water, "/water.png", "DodgerBlue", *const_args)

    # indicate completion in console
    printer.complete()


# save the plotted images
def save_plot(x_, y_, filename_, color_, output, dpi, x_min, x_max, y_min, y_max, size):
    plt.plot(x_, y_, color=color_, linestyle="none", marker=",")

    # ensure the image is not distorted by using known file min/max
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # various output settings
    plt.margins(0, 0)
    plt.axis("off")
    plt.tight_layout(pad=0.05)
    plt.gca().set_facecolor("black")

    # save the image to a given output
    fig = plt.gcf()
    fig.set_size_inches(size, size)
    fig.savefig(
        output + filename_,
        dpi=dpi,
        bbox_inches=0,
        pad_inches=-1,
        facecolor="black",
    )
    plt.clf()

    # print the 'saved' status for file
    printer.saved(filename_)
