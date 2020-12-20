# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
import printer
import matplotlib.pyplot as plt


def upper_z(input_file, divisions, layer):

    """
    function that returns the upper Z bound of a colour band.
    this function takes a given number of bands (divisions),
    a band number (layer) to determine the upper bound of that band
    """

    # all points that are of ground classification
    z = input_file.Z[input_file.Classification == 2]
    # the difference between the highest and lowest point
    z_delta = np.amax(z) - np.amin(z)
    # return the upper bound for the band
    return int(np.amin(z) + ((z_delta / divisions) * layer))


def get_band(input_file, divisions, layer):

    """
    function that returns the X,Y values for points within
    a specified depth band. This function takes a given
    number of divisions (total layers) and a desired layer
    index to determine the valid points that fall within
    the high/low bounds for a depth band

    """

    # the derived upper bound for the given depth band
    upper_bound = upper_z(input_file, divisions, layer)
    # boolean mask representing all ground points in file
    valid_c = input_file.Classification == 2
    # boolean mask representing all points below the upper bound
    valid_upper = input_file.Z < upper_bound

    if layer == 1:
        # boolean mask which represents all points in the band
        all_valid = np.logical_and(valid_c, valid_upper)
    else:
        # determine the lower bound for the given band
        lower_bound = upper_z(input_file, divisions, (layer - 1))
        # boolean mask representing all points above the lower bound
        valid_lower = input_file.Z > lower_bound
        # boolean mask representing all points within the bounds (all)
        valid_bounds = np.logical_and(valid_upper, valid_lower)
        # boolean mask which represents all points in the band (ground)
        all_valid = np.logical_and(valid_c, valid_bounds)

    # return the X, Y coords for all valid points in the band
    return input_file.X[all_valid], input_file.Y[all_valid]


# plot the positional data and then save as PNG
def gradient(input, output, size, dpi):

    # print console heading for process
    printer.gradient_print()

    # the name of the output file
    filename = "/gradient.png"

    # read in LAS file
    input_file = File(input, mode="r")

    # get the min/max X,Y values to normalise the plot scale
    x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
    y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

    plt.rcParams["figure.facecolor"] = "black"

    # the bands of points at various depths
    bands = (
        get_band(input_file, 10, 1),
        get_band(input_file, 10, 2),
        get_band(input_file, 10, 3),
        get_band(input_file, 10, 4),
        get_band(input_file, 10, 5),
        get_band(input_file, 10, 6),
        get_band(input_file, 10, 7),
        get_band(input_file, 10, 8),
        get_band(input_file, 10, 9),
        get_band(input_file, 10, 10),
    )

    # the colour range to be assigned to the bands
    colours = (
        (1.0, 1.0, 1.0),
        (0.8, 1.0, 1.0),
        (0.6, 1.0, 1.0),
        (0.4, 1.0, 1.0),
        (0.2, 1.0, 1.0),
        (0.0, 0.8, 1.0),
        (0.0, 0.6, 1.0),
        (0.0, 0.4, 1.0),
        (0.0, 0.2, 1.0),
        (0.0, 0.0, 1.0),
    )

    # plot the individual bands sequentially
    for b, c in zip(bands, colours):
        plt.plot(*b, color=c, linestyle="none", marker=",")

    # ensure the image is not distorted by using known file min/max
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # various output settings
    plt.margins(0, 0)
    plt.axis("off")
    plt.tight_layout(pad=0.05)

    # save the image to a given output
    fig = plt.gcf()
    fig.set_size_inches(size, size)
    fig.savefig(
        output + filename,
        dpi=dpi,
        pad_inches=-1,
        facecolor="black",
    )

    # clear the image from meory
    plt.clf()

    # print the 'saved' status in console
    printer.saved(filename)

    # indicate completion in console
    printer.complete()
