from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt


# get the positional data of points in a specified classification
def get_xy(in_points, classification):
    x = in_points.X[in_points.Classification == classification]
    y = in_points.Y[in_points.Classification == classification]
    return x, y


# plot the positional data and then save as PNG
def plot(input, output, size, dpi):

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points
    las_specification = input_file.point_format.fmt

    # get the min/max X,Y values to normalise the plot scale
    x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
    y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

    # print output of derived header information
    print_header_info(input_file, point_records, las_specification)

    # initialise point-variable arrays
    buildings = get_xy(input_file, 6)
    unclassified = get_xy(input_file, 1)
    ground = get_xy(input_file, 2)
    lowVeg = get_xy(input_file, 3)
    medVeg = get_xy(input_file, 4)
    highVeg = get_xy(input_file, 5)
    water = get_xy(input_file, 9)

    # basic params for the plot function
    plt.rcParams["figure.figsize"] = [size, size]
    plt.rcParams["figure.facecolor"] = "black"

    print("")
    print("CLASSIFICATION PLOT")
    print("-----------------------------------------")

    const_args = output, dpi, x_min, x_max, y_min, y_max

    # save the individual layer plots as .PNG
    save(*unclassified, "/unclassified.png", "m", *const_args)
    save(*ground, "/ground.png", "SaddleBrown", *const_args)
    save(*lowVeg, "/lowVeg.png", "LimeGreen", *const_args)
    save(*medVeg, "/mediumVeg.png", "Green", *const_args)
    save(*highVeg, "/highVeg.png", "DarkGreen", *const_args)
    save(*buildings, "/buildings.png", "White", *const_args)
    save(*water, "/water.png", "DodgerBlue", *const_args)

    print("-----------------------------------------")
    print("process complete")


# save the plotted images
def save(x_, y_, filename_, color_, output, dpi, x_min, x_max, y_min, y_max):
    plt.plot(x_, y_, color=color_, linestyle="none", marker=",")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.margins(0, 0)
    plt.gca().set_facecolor("black")
    fig = plt.gcf()
    fig.savefig(
        output + filename_,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black",
    )
    plt.clf()
    print(filename_, "saved successfully")


def print_header_info(input_file, point_records, las_specification):
    print("---------------------------HEADER INFORMATION--------------------------")
    print("LAS specification = " + input_file.header.version)
    print("point format = " + str(las_specification))
    print("total point count = " + str(input_file.header.count))
    print("-----------------------------------------------------------------------")
