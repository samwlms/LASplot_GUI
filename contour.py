from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt


# get the positional data of points in a specified classification
def get_xy(in_points, classification):
    x = in_points.X[in_points.Classification == classification]
    y = in_points.Y[in_points.Classification == classification]
    z = in_points.Z[in_points.Classification == classification]
    z_delta = np.amax(z) - np.amin(z)
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
    upper_bound = upper_z(input_file, divisions, layer)
    valid_c = input_file.Classification == 2
    valid_upper = input_file.Z < upper_bound
    if layer == 1:
        all_valid = np.logical_and(valid_c, valid_upper)
    else:
        lower_bound = upper_z(input_file, divisions, (layer - 1))
        valid_lower = input_file.Z > lower_bound
        valid_bounds = np.logical_and(valid_upper, valid_lower)
        all_valid = np.logical_and(valid_c, valid_bounds)
    return input_file.X[all_valid], input_file.Y[all_valid]


# plot the positional data and then save as PNG
def contour(input, output, size, dpi):

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

    # the points from the input file which match our masks
    points_1 = get_band(input_file, 10, 1)
    points_2 = get_band(input_file, 10, 2)
    points_3 = get_band(input_file, 10, 3)
    points_4 = get_band(input_file, 10, 4)
    points_5 = get_band(input_file, 10, 5)
    points_6 = get_band(input_file, 10, 6)
    points_7 = get_band(input_file, 10, 7)
    points_8 = get_band(input_file, 10, 8)
    points_9 = get_band(input_file, 10, 9)
    points_10 = get_band(input_file, 10, 10)

    print("")
    print("CONTOUR PLOT")
    print("-----------------------------------------")

    plt.plot(*points_1, color=(1.0, 1.0, 1.0), linestyle="none", marker=",")
    plt.plot(*points_2, color=(0.8, 1.0, 1.0), linestyle="none", marker=",")
    plt.plot(*points_3, color=(0.6, 1.0, 1.0), linestyle="none", marker=",")
    plt.plot(*points_4, color=(0.4, 1.0, 1.0), linestyle="none", marker=",")
    plt.plot(*points_5, color=(0.2, 1.0, 1.0), linestyle="none", marker=",")
    plt.plot(*points_6, color=(0.0, 0.8, 1.0), linestyle="none", marker=",")
    plt.plot(*points_7, color=(0.0, 0.6, 1.0), linestyle="none", marker=",")
    plt.plot(*points_8, color=(0.0, 0.4, 1.0), linestyle="none", marker=",")
    plt.plot(*points_9, color=(0.0, 0.2, 1.0), linestyle="none", marker=",")
    plt.plot(*points_10, color=(0.0, 0.0, 1.0), linestyle="none", marker=",")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.margins(0, 0)
    plt.gca().set_facecolor("black")
    fig = plt.gcf()
    fig.savefig(
        output + "/contour.png",
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black",
    )
    plt.clf()
    print("contour.png saved successfully")

    print("-----------------------------------------")
    print("process complete")
