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
    print("FILE INFO")
    print("-----------------------------------------")
    print("")

    print("")
    print("")
    print("----------------------------------")
    print("evlrs:")
    print("----------------------------------")
    evlrs = input_file.header.evlrs
    for elvr in evlrs:
        print(evlr)

    print("")
    print("")
    print("----------------------------------")
    print("global_encoding:")
    print("----------------------------------")
    global_encoding = input_file.header.global_encoding
    print(global_encoding)

    print("")
    print("")
    print("----------------------------------")
    print("WKT:")
    print("----------------------------------")
    wkt = input_file.header.wkt
    print(wkt)

    print("")
    print("")
    print("----------------------------------")
    print("guid's:")
    print("----------------------------------")
    guid = input_file.header.guid
    print(guid)

    print("")
    print("")
    print("----------------------------------")
    print("Point data format:")
    print("----------------------------------")
    pointformat = input_file.point_format
    for spec in pointformat:
        print(spec.name)

    print("")
    print("")
    print("----------------------------------")
    print("Sample point data:")
    print("----------------------------------")
    print(point_records[0])

    print("")
    print("")
    print("----------------------------------")
    print("Header data format:")
    print("----------------------------------")
    headerformat = input_file.header.header_format
    for spec in headerformat:
        print(spec.name)

    print("-----------------------------------------")
    print("process complete")
