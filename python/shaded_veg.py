# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import numpy as np
from scipy.spatial.kdtree import KDTree
import printer
import time
import matplotlib.pyplot as plt


def plot_shaded(input):
    input_file = File(input, mode="r")
    veg = np.vstack(
        [
            input_file.X[input_file.Classification == 5],
            input_file.Y[input_file.Classification == 5],
            input_file.Z[input_file.Classification == 5],
        ]
    ).transpose()

    ground = np.vstack(
        [
            input_file.X[input_file.Classification == 2],
            input_file.Y[input_file.Classification == 2],
            input_file.Z[input_file.Classification == 2],
        ]
    ).transpose()

    ground_tree = KDTree(ground)

    heights = []

    for point in veg:
        height = round(get_height(ground_tree, ground, point) * 0.01, 2)
        heights.append(height)

    veg_with_height = np.vstack(
        [
            input_file.X[input_file.Classification == 5],
            input_file.Y[input_file.Classification == 5],
            heights,
        ]
    ).transpose()

    bands_required = 50

    point_bands = generate_veg_bands(veg_with_height, bands_required)
    generate_band_colours(bands_required)


def generate_veg_bands(veg_points, bands_required):
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
    for count in range(bands_required):
        height = count + 3
        # for the first band, include all points < 2m high
        if count == 0:
            valid = veg_points[:, 2] < height
            band = veg_points[valid]
            bands = bands + ((band),)
        # for the final band, include all points > height
        elif count == bands_required - 1:
            valid = veg_points[:, 2] >= height
            band = veg_points[valid]
            bands = bands + ((band),)
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

    increment = (1.0 - 0.35) / bands_required
    colours = ()

    red = 0.0
    green = 0.35
    blue = 0.0

    for count in range(bands_required):
        green = round(green + increment, 3)
        band_colour = (red, green, blue)
        print("count:", count)
        print("band_colour:", band_colour)
        colours = colours + (band_colour,)


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