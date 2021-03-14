# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
from scipy.spatial.kdtree import KDTree
import printer
import time
import matplotlib.pyplot as plt


class WindowSelections:
    def __init__(self, input, output, size, dpi):
        self.input = input
        self.output = output
        self.size = size
        self.dpi = dpi
        self.las = File(self.input, mode="r")


class LayerPlotter(WindowSelections):
    def __init__(self, input, output, size, dpi, plot_args):
        super().__init__(input, output, size, dpi)
        self.plot_args = plot_args

    # plot the positional data and then save as PNG
    def plot(self):
        printer.plot_print()
        for arg in self.plot_args:
            if arg == 1:
                self.save_plot(*self.get_xy(arg), "/unclassified.png", "m")
            elif arg == 2:
                self.save_plot(*self.get_xy(arg), "/ground.png", "SaddleBrown")
            elif arg == 3:
                self.save_plot(*self.get_xy(arg), "/lowVeg.png", "LimeGreen")
            elif arg == 4:
                self.save_plot(*self.get_xy(arg), "/mediumVeg.png", "Green")
            elif arg == 5:
                self.save_plot(*self.get_xy(arg), "/highVeg.png", "DarkGreen")
            elif arg == 6:
                self.save_plot(*self.get_xy(arg), "/buildings.png", "White")
            elif arg == 9:
                self.save_plot(*self.get_xy(arg), "/water.png", "DodgerBlue")
        printer.complete()

    def get_xy(self, classification):
        """
        get the X/Y positional data for points of a specified classification
        """
        x = self.las.X[self.las.Classification == classification]
        y = self.las.Y[self.las.Classification == classification]
        return x, y

    # save the plotted images
    def save_plot(self, x_, y_, filename, color):
        plt.plot(x_, y_, color=color, linestyle="none", marker=",")

        start = time.time()

        # ensure the image is not distorted by using known file min/max
        plt.xlim(np.amin(self.las.X), np.amax(self.las.X))
        plt.ylim(np.amin(self.las.Y), np.amax(self.las.Y))

        # various output settings
        plt.margins(0, 0)
        plt.axis("off")
        plt.tight_layout(pad=0.05)

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
        printer.saved(filename, time_output)


class VegShader(WindowSelections):
    def __init__(self, input, output, size, dpi):
        super().__init__(input, output, size, dpi)
        self.colours = None
        self.bands = None
        self.bands_required = 15

    def plot_shaded(self):
        printer.shaded_print()
        start = time.time()

        # make some 2D arrays representing high vegetation and ground points
        veg = np.vstack(
            [
                self.las.X[self.las.Classification == 5],
                self.las.Y[self.las.Classification == 5],
                self.las.Z[self.las.Classification == 5],
            ]
        ).transpose()
        ground = np.vstack(
            [
                self.las.X[self.las.Classification == 2],
                self.las.Y[self.las.Classification == 2],
                self.las.Z[self.las.Classification == 2],
            ]
        ).transpose()

        # generate a KD Tree of the ground points
        ground_tree = KDTree(ground)

        # get the Z scale of the las file for height calculation
        scale = self.las.header.scale[2]

        # 2D array with the Z component representing relative height from ground
        veg_with_height = np.vstack(
            [
                self.las.X[self.las.Classification == 5],
                self.las.Y[self.las.Classification == 5],
                [self.get_height(ground_tree, ground, point) * scale for point in veg],
            ]
        ).transpose()

        self.generate_veg_bands(veg_with_height)
        self.generate_band_colours()
        self.plot_bands()

        time_output = time.time() - start
        printer.saved("/shaded_veg.png", time_output)
        printer.complete()

    def get_height(self, ground_tree, ground, point):
        """
        function that runs a spatial query using the scipy.spatial.kdtree library.
        The query checks for the closest point of ground classification to any given
        high vegetation point. The vertical (z) distance between these points is then
        returned
        """
        closest_point = ground[ground_tree.query(point)[1]]
        distance_from_ground = point[2] - closest_point[2]
        return distance_from_ground

    def generate_veg_bands(self, veg_points):
        """
        function that generates n number of bands (containing sorted high veg points).
        The metric that determines band assignment is the vertical (z) distance from
        the nearest ground point.

        note: it is unlikely that the nearest ground point will contain matching X,Y values
        and thus the 'distance from ground' value is only a relative approximation rather than
        a precise measurement. Triangulation and averaging of the 3 nearest ground points is
        a potential solution to this problem.
        """
        bands = ()
        for height in range(self.bands_required):
            # for the first band, include all points < 2m high
            if height == 0:
                valid = veg_points[:, 2] < height
            # for the final band, include all points > height
            elif height == self.bands_required - 1:
                valid = veg_points[:, 2] >= height
            else:
                upper_limit = veg_points[:, 2] < height + 1
                lower_limit = veg_points[:, 2] >= height
                valid = np.logical_and(upper_limit, lower_limit)
            band = veg_points[valid]
            bands = bands + ((band),)

        self.bands = bands

    def generate_band_colours(self):
        """
        green RGB range will be from:
        [0, 100, 0](light green) -> [0, 255, 0](dark green)

        expressed using matplotlib's plot parameters, this (roughly) maps to:
        [0.0, 0.35, 0.0](light green) -> [0.0, 1.0, 0.0](dark green)

        therefore, the incriment increase for the green value can be expressed as:
        1.0 - 0.35 / number of bands
        """

        increment = (1.0 - 0.3) / self.bands_required
        colours = ()

        red = 0.1
        green = 1.0
        blue = 0.1

        for count in range(self.bands_required):
            green = round(green - increment, 3)
            band_colour = (red, green, blue)
            colours = colours + (band_colour,)

        self.colours = colours

    def plot_bands(self):
        # ensure the image is not distorted by using known file min/max
        plt.xlim(np.amin(self.las.X), np.amax(self.las.X))
        plt.ylim(np.amin(self.las.Y), np.amax(self.las.Y))

        # plot the individual bands sequentially
        for b, c in zip(self.bands, self.colours):
            try:
                plt.plot(b[:, 0], b[:, 1], color=c, linestyle="none", marker=",")
            except Exception as e:
                print(e)

        # various output settings
        plt.margins(0, 0)
        plt.axis("off")
        plt.tight_layout(pad=0.05)

        # save the image to a given output
        fig = plt.gcf()
        fig.set_size_inches(self.size, self.size)
        fig.savefig(
            self.output + "/shaded_veg.png",
            dpi=self.dpi,
            pad_inches=-1,
            facecolor="black",
        )
        plt.clf()
