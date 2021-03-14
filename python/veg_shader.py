# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
from scipy.spatial.kdtree import KDTree
import printer
import time
import matplotlib.pyplot as plt


class veg_shader:
    def __init__(self, input, output, size, dpi):
        self.input = input
        self.output = output
        self.size = size
        self.dpi = dpi
        self.file = File(self.input, mode="r")

    def plot_shaded(self):
        start = time.time()
        las = self.file
        veg = np.vstack(
            [
                las.X[las.Classification == 5],
                las.Y[las.Classification == 5],
                las.Z[las.Classification == 5],
            ]
        ).transpose()

        ground = np.vstack(
            [
                las.X[las.Classification == 2],
                las.Y[las.Classification == 2],
                las.Z[las.Classification == 2],
            ]
        ).transpose()

        ground_tree = KDTree(ground)

        heights = []

        for point in veg:
            height = round(get_height(ground_tree, ground, point) * 0.01, 2)
            heights.append(height)

        veg_with_height = np.vstack(
            [
                las.X[las.Classification == 5],
                las.Y[las.Classification == 5],
                heights,
            ]
        ).transpose()

        bands_required = 15

        bands = generate_veg_bands(veg_with_height, bands_required)
        colours = generate_band_colours(bands_required)

        filename = "/shaded_veg.png"

        plot_bands(input_file, filename, bands, colours, output, size_int, dpi_int)

        time_output = time.time() - start

        # print the 'saved' status in console
        printer.saved(filename, time_output)

        # indicate completion in console
        printer.complete()

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
        return bands

    def generate_band_colours(bands_required):
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

        return colours

    def get_height(ground_tree, ground, point):
        """
        function that runs a spatial query using the scipy.spatial.kdtree library.
        The query checks for the closest point of ground classification to any given
        high vegetation point. The vertical (z) distance between these points is then
        returned
        """
        closest_point = ground[ground_tree.query(point)[1]]
        distance_from_ground = point[2] - closest_point[2]
        return distance_from_ground

    def plot_bands(file, filename, bands, colours, output, size, dpi):

        # get the min/max X,Y values to normalise the plot scale
        x_min, x_max = np.amin(file.X), np.amax(file.X)
        y_min, y_max = np.amin(file.Y), np.amax(file.Y)

        # plot the individual bands sequentially
        for b, c in zip(bands, colours):
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
        fig.set_size_inches(size, size)
        fig.savefig(
            output + filename,
            dpi=dpi,
            pad_inches=-1,
            facecolor="black",
        )

        # clear the image from meory
        plt.clf()
