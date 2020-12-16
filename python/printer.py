# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import laspy
import numpy as np
import matplotlib.pyplot as plt


# plot the positional data and then save as PNG
def test(input):

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points
    pointformat = input_file.point_format

    print("")
    print("-----------------------------------------")
    print("----------------FILE INFO----------------")
    print("-----------------------------------------")
    print("")

    print("------ Point data format: ------")

    pointformat = input_file.point_format
    for spec in pointformat:
        print(spec.name)

    print("")

    print("------ Sample point data: ------")

    print(point_records[0])

    print("")

    print("------ Header data format: ------")

    headerformat = input_file.header.header_format
    for spec in headerformat:
        print(spec.name)

    print("")
    print("-----------------------------------------")
    print("process complete")
