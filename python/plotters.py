# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
from scipy.spatial.kdtree import KDTree
import printer
import time
import matplotlib.pyplot as plt


class VegShader:
    def __init__(self, input, output, size, dpi):
        self.input = input
        self.output = output
        self.size = size
        self.dpi = dpi
        self.las = File(self.input, mode="r")
        self.colours = None
        self.bands = None
        self.filename = "/shaded_veg.png"

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

    def generate_veg_bands(self, veg_points, bands_required):
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
        for height in range(bands_required):
            # for the first band, include all points < 2m high
            if height == 0:
                valid = veg_points[:, 2] < height
            # for the final band, include all points > height
            elif height == bands_required - 1:
                valid = veg_points[:, 2] >= height
            else:
                upper_limit = veg_points[:, 2] < height + 1
                lower_limit = veg_points[:, 2] >= height
                valid = np.logical_and(upper_limit, lower_limit)
            band = veg_points[valid]
            bands = bands + ((band),)

        self.bands = bands

    def generate_band_colours(self, bands_required):
        """
        green RGB range will be from:
        [0, 100, 0](light green) -> [0, 255, 0](dark green)

        expressed using matplotlib's plot parameters, this (roughly) maps to:
        [0.0, 0.35, 0.0](light green) -> [0.0, 1.0, 0.0](dark green)

        therefore, the incriment increase for the green value can be expressed as:
        1.0 - 0.35 / number of bands
        """

        increment = (1.0 - 0.3) / bands_required
        colours = ()

        red = 0.1
        green = 1.0
        blue = 0.1

        for count in range(bands_required):
            green = round(green - increment, 3)
            band_colour = (red, green, blue)
            colours = colours + (band_colour,)

        self.colours = colours

    def plot_bands(self):
        # get the min/max X,Y values to normalise the plot scale
        x_min, x_max = np.amin(self.las.X), np.amax(self.las.X)
        y_min, y_max = np.amin(self.las.Y), np.amax(self.las.Y)

        # plot the individual bands sequentially
        for b, c in zip(self.bands, self.colours):
            try:
                plt.plot(b[:, 0], b[:, 1], color=c, linestyle="none", marker=",")
            except Exception as e:
                print(e)

        # ensure the image is not distorted by using known file min/max
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        # various output settings
        plt.margins(0, 0)
        plt.axis("off")
        plt.tight_layout(pad=0.05)

        # save the image to a given output
        fig = plt.gcf()
        fig.set_size_inches(self.size, self.size)
        fig.savefig(
            self.output + self.filename,
            dpi=self.dpi,
            pad_inches=-1,
            facecolor="black",
        )

        # clear the image from meory
        plt.clf()

    def plot_shaded(self):
        start = time.time()
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

        ground_tree = KDTree(ground)

        heights = []

        for point in veg:
            height = round(self.get_height(ground_tree, ground, point) * 0.01, 2)
            heights.append(height)

        veg_with_height = np.vstack(
            [
                self.las.X[self.las.Classification == 5],
                self.las.Y[self.las.Classification == 5],
                heights,
            ]
        ).transpose()

        bands_required = 15

        self.generate_veg_bands(veg_with_height, bands_required)
        self.generate_band_colours(bands_required)

        self.plot_bands()

        time_output = time.time() - start

        # print the 'saved' status in console
        printer.saved(self.filename, time_output)

        # indicate completion in console
        printer.complete()
