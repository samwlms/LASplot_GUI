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
            input_file.x[input_file.Classification == 5],
            input_file.y[input_file.Classification == 5],
            input_file.z[input_file.Classification == 5],
        ]
    ).transpose()

    ground = np.vstack(
        [
            input_file.x[input_file.Classification == 2],
            input_file.y[input_file.Classification == 2],
            input_file.z[input_file.Classification == 2],
        ]
    ).transpose()

    tree = KDTree(ground)
    for point in veg:
        closest_point = ground[tree.query(point)[1]]
        distance_from_ground = point[2] - closest_point[2]
        print("distance from ground:", distance_from_ground)
