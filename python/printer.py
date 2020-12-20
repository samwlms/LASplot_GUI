# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import laspy
import numpy as np
import matplotlib.pyplot as plt


def saved(filename):
    print(filename, "saved successfully")


def plot_print():

    print("")
    print("-----------------------------------------")
    print("----------CLASSIFICATION PLOTS-----------")
    print("-----------------------------------------")


def contour_print():

    print("")
    print("-----------------------------------------")
    print("--------------CONTOUR PLOT---------------")
    print("-----------------------------------------")


def gradient_print():

    print("")
    print("-----------------------------------------")
    print("-------------GRADIENT PLOT---------------")
    print("-----------------------------------------")


def info_print():

    print("")
    print("-----------------------------------------")
    print("----------------FILE INFO----------------")
    print("-----------------------------------------")


def complete():

    print("-----------------------------------------")
    print("process complete")


def format(input):

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points
    pointformat = input_file.point_format

    info_print()

    print("------ Point data format: ------")
    pointformat = input_file.point_format
    for spec in pointformat:
        print(spec.name)

    print("------ Sample point data: ------")
    print(point_records[0])

    print("------ Header data format: ------")
    headerformat = input_file.header.header_format
    for spec in headerformat:
        print(spec.name)

    complete()
