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



    ground=np.vstack([input_file.X[input_file.Classification == 2], input_file.Y[input_file.Classification ==
                     2], input_file.Z[input_file.Classification == 2], ]).transpose()

    a_veg_point=veg[100]
    closest_point=ground[KDTree(ground).query(a_veg_point)[1]]
    print("closest point", closest_point)
    print(closest_point)
