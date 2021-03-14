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

    def save_png(self, filename):
        # ensure the image is not distorted by using known file min/max
        plt.xlim(np.amin(self.las.X), np.amax(self.las.X))
        plt.ylim(np.amin(self.las.Y), np.amax(self.las.Y))

        # various output settings
        plt.margins(0, 0)
        plt.axis("off")
        plt.tight_layout(pad=0.05)

        fig = plt.gcf()
        fig.set_size_inches(self.size, self.size)
        fig.savefig(
            self.output + filename,
            dpi=self.dpi,
            pad_inches=-1,
            facecolor="black",
        )
        plt.clf()


class GradientPlotter(WindowSelections):
    def __init__(self, operation, input, output, size, dpi, marker):
        super().__init__(input, output, size, dpi)
        self.operation = operation
        self.filename = "/" + operation + ".png"
        self.marker = marker
        self.num_bands = 25
        self.bands = None
        self.colours = None

    # plot the positional data and then save as PNG
    def plot_gradient(self):
        start = time.time()

        if self.operation == "gradient":
            printer.gradient_print()
        elif self.operation == "intensity":
            printer.intensity_print()

        self.generate_bands()
        self.generate_colours()

        # plot the individual bands sequentially
        for b, c in zip(self.bands, self.colours):
            plt.plot(*b, color=c, linestyle="none", marker=self.marker)

        # save the image to a given output
        self.save_png(self.filename)

        time_output = time.time() - start
        printer.saved(self.filename, time_output)
        printer.complete()

    def upper_limit(self, layer):

        """
        function that returns the upper Z bound of a colour band.
        this function takes a given number of bands (divisions),
        a band number (layer) to determine the upper bound of that band
        """

        if self.operation == "gradient":
            metric = self.las.Z[self.las.Classification == 2]
        elif self.operation == "intensity":
            metric = self.las.intensity[self.las.Classification == 2]

        # the difference between the highest and lowest point
        metric_delta = np.amax(metric) - np.amin(metric)

        # return the upper bound for the band
        return int(np.amin(metric) + ((metric_delta / self.num_bands) * layer))

    def get_band(self, layer):

        """
        function that returns the X,Y values for points within
        a specified depth band. This function takes a given
        number of divisions (total layers) and a desired layer
        index to determine the valid points that fall within
        the high/low bounds for a depth band
        """

        if self.operation == "gradient":
            metric = self.las.Z
        elif self.operation == "intensity":
            metric = self.las.intensity

        # the derived upper bound for the given depth band
        upper_bound = self.upper_limit(layer)
        # boolean mask representing all ground points in file
        valid_c = self.las.Classification == 2
        # boolean mask representing all points below the upper bound
        valid_upper = metric < upper_bound

        if layer == 1:
            # boolean mask which represents all points in the band
            all_valid = np.logical_and(valid_c, valid_upper)
        else:
            # determine the lower bound for the given band
            lower_bound = self.upper_limit(layer - 1)
            # boolean mask representing all points above the lower bound
            valid_lower = metric > lower_bound
            # boolean mask representing all points within the bounds (all)
            valid_bounds = np.logical_and(valid_upper, valid_lower)
            # boolean mask which represents all points in the band (ground)
            all_valid = np.logical_and(valid_c, valid_bounds)

        # return the X, Y coords for all valid points in the band
        return self.las.X[all_valid], self.las.Y[all_valid]

    def generate_colours(self):

        """
        generate a tuple (of tuples) containing RGB values for individual colour bands.
        rather than using a sine wave function to calculate RGB values, a simpler method
        was implemented.See the documentation for a visual representation of the colour value theory.
        """

        colours = ()
        bands = self.num_bands

        # the distinct quartered disvisons used to evaluate RGB values
        Q1 = bands / 4.0
        Q2 = bands / 2.0
        Q3 = Q1 + Q2
        Q4 = bands

        for count in range(0, bands):
            # (1/4) red to yellow
            if count <= Q1:
                red = 0.0
                green = round(count / (bands / 4), 1)
                blue = 1.0
            # (2/4) yellow to green
            elif count > Q1 and count <= Q2:
                red = 0.0
                blue = round(2 - (count / (bands / 4)), 1)
                green = 1.0
            # (3/4) green to aqua
            elif count > Q2 and count <= Q3:
                red = round((count / (bands / 4) - 2), 1)
                green = 1.0
                blue = 0.0
            # (4/4) aqua to blue
            elif count > Q3:
                red = 1.0
                green = round(4 - (count / (bands / 4)), 1)
                blue = 0.0

            colours = colours + ((red, green, blue),)
        self.colours = colours

    def generate_bands(self):
        final_bands = ()
        for count in range(0, self.num_bands):
            current_band = self.get_band(count)
            final_bands = final_bands + ((current_band),)
        self.bands = final_bands


class LayerPlotter(WindowSelections):
    def __init__(self, input, output, size, dpi, marker, plot_args):
        super().__init__(input, output, size, dpi)
        self.plot_args = plot_args
        self.marker = marker

    def plot(self):
        printer.plot_print()

        # dict containing the names/ colours of various classification
        # layers, where the key maps with the LAS spec classification.
        names_colours = {
            "1": ["/unclassified.png", "m"],
            "2": ["/ground.png", "SaddleBrown"],
            "3": ["/lowVeg.png", "LimeGreen"],
            "4": ["/mediumVeg.png", "Green"],
            "5": ["/highVeg.png", "DarkGreen"],
            "6": ["/buildings.png", "White"],
            "9": ["/water.png", "DodgerBlue"],
        }

        for arg in self.plot_args:
            start = time.time()
            val = names_colours[str(arg)]

            # save the image to a given output
            plt.plot(
                *self.get_xy(arg), color=val[1], linestyle="none", marker=self.marker
            )
            self.save_png(val[0])

            time_output = time.time() - start
            printer.saved(val[0], time_output)
        printer.complete()

    def get_xy(self, classification):
        """
        get the X/Y positional data for points of a specified classification
        """
        x = self.las.X[self.las.Classification == classification]
        y = self.las.Y[self.las.Classification == classification]
        return x, y


class VegShader(WindowSelections):
    def __init__(self, input, output, size, dpi, marker):
        super().__init__(input, output, size, dpi)
        self.marker = marker
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

        red = 0.3
        green = 1.0
        blue = 0.0

        for count in range(self.bands_required):
            green = round(green - increment, 3)
            red = round(red - increment / 3, 3)
            band_colour = (red, green, blue)
            colours = colours + (band_colour,)

        self.colours = colours

    def plot_bands(self):

        # plot the individual bands sequentially
        for b, c in zip(self.bands, self.colours):
            try:
                plt.plot(
                    b[:, 0], b[:, 1], color=c, linestyle="none", marker=self.marker
                )
            except Exception as e:
                print(e)

        # save the image to a given output
        self.save_png("/shaded_veg.png")