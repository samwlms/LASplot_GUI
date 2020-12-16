# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt


# get the positional data of points in a specified classification
def get_xy(in_points, classification):
    x = in_points.X[in_points.Classification == classification]
    y = in_points.Y[in_points.Classification == classification]
    return x, y


def middle_z(input_file):
    # function that returns the mid point of the Z values
    z = input_file.Z[input_file.Classification == 2]
    z_delta = np.amax(z) - np.amin(z)
    return np.amin(z) + (z_delta / 2)


def upper_z(input_file, divisions, layer):
    # function that returns the upper Z bound of a colour band.
    # this function takes a given number of bands (divisions), a band number (layer)
    # to determine the upper bound of that specifc band
    z = input_file.Z[input_file.Classification == 2]
    z_delta = np.amax(z) - np.amin(z)
    return int(np.amin(z) + ((z_delta / divisions) * layer))


def get_band(input_file, divisions, layer):
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
def contour(input, output, size, dpi):

    print("")
    print("CONTOUR PLOT")
    print("-----------------------------------------")

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points

    # get the min/max X,Y values to normalise the plot scale
    x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
    y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

    # initialise point-variable arrays
    ground = get_xy(input_file, 2)

    # basic params for the plot function
    plt.rcParams["figure.figsize"] = [size, size]
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
    plt.gca().set_facecolor("black")
    fig = plt.gcf()

    # save the image to a given output
    fig.savefig(
        output + "/contour.png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black",
    )

    # clear the image from meory
    plt.clf()

    print("contour.png saved successfully")
    print("-----------------------------------------")
    print("process complete")
