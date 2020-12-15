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

    mid_z = middle_z(input_file)

    # bool masks for the input points that meet our conditions
    l_mask = np.logical_and(input_file.Classification == 2, input_file.Z < mid_z)
    h_mask = np.logical_and(input_file.Classification == 2, input_file.Z > mid_z)

    # the points from the input file which match our masks
    low_points = input_file.X[l_mask], input_file.Y[l_mask]
    high_points = input_file.X[h_mask], input_file.Y[h_mask]

    print(low_points)
    print(high_points)

    print("")
    print("CONTOUR PLOT")
    print("-----------------------------------------")

    plt.plot(*low_points, color="DodgerBlue", linestyle="none", marker=",")
    plt.plot(*high_points, color="LimeGreen", linestyle="none", marker=",")
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
