# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
import printer, time
import matplotlib.pyplot as plt


class ClassificationPlotter:
    def __init__(self, input, output, size, dpi, plot_args):
        self.input = input
        self.output = output
        self.size = size
        self.dpi = dpi
        self.plot_args = plot_args
        self.las = File(self.input, mode="r")

    # get the positional data of points in a specified classification
    def get_xy(self, classification):
        x = in_points.X[in_points.Classification == classification]
        y = in_points.Y[in_points.Classification == classification]
        return x, y

    # plot the positional data and then save as PNG
    def plot(input, output, size, dpi, classifications):

        # print console heading for process
        printer.plot_print()

        # read in LAS file and specify point records, las spec
        point_records = input_file.points
        las_specification = input_file.point_format.fmt

        # get the min/max X,Y values to normalise the plot scale
        x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
        y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

        # basic params for the plot function
        plt.rcParams["figure.facecolor"] = "black"

        for arg in self.plot_args:
            if arg == 1:
                save_plot(*get_xy(arg), "/unclassified.png", "m")
            elif arg == 2:
                save_plot(*get_xy(arg), "/ground.png", "SaddleBrown")
            elif arg == 3:
                save_plot(*get_xy(arg), "/lowVeg.png", "LimeGreen")
            elif arg == 4:
                save_plot(*get_xy(arg), "/mediumVeg.png", "Green")
            elif arg == 5:
                save_plot(*get_xy(arg), "/highVeg.png", "DarkGreen")
            elif arg == 6:
                save_plot(*get_xy(arg), "/buildings.png", "White")
            elif arg == 9:
                save_plot(*get_xy(arg), "/water.png", "DodgerBlue")

        # indicate completion in console
        printer.complete()

    # save the plotted images
    def save_plot(x_, y_, filename, color):
        plt.plot(x_, y_, color=color, linestyle="none", marker=",")

        start = time.time()

        # get the min/max X,Y values to normalise the plot scale
        x_min, x_max = np.amin(self.las.X), np.amax(self.las.X)
        y_min, y_max = np.amin(self.las.Y), np.amax(self.las.Y)

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
        fig.set_size_inches(self.size, self.size)
        fig.savefig(
            self.output + filename,
            dpi=self.dpi,
            bbox_inches=0,
            pad_inches=-1,
            facecolor="black",
        )
        plt.clf()

        time_output = time.time() - start

        # print the 'saved' status for file
        printer.saved(filename_, time_output)
