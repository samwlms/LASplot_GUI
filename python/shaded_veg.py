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

    for count, point in enumerate(veg):
        height = round(get_height(ground_tree, ground, point) * 0.01, 2)
        heights.append(height)
    max_height = np.amax(heights)
    min_height = np.amin(heights)
    print("max height:", max_height)
    print("min height:", min_height)


def get_height(ground_tree, ground, point):
    closest_point = ground[ground_tree.query(point)[1]]
    distance_from_ground = point[2] - closest_point[2]
    return distance_from_ground