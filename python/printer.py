# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import laspy
import numpy as np
import matplotlib.pyplot as plt


def saved(filename, time):
    string_time = str(round(time, 2)) + "s"
    print(filename, "saved in", string_time)


def plot_print():

    print("")
    print("-----------------------------------------")
    print("----------CLASSIFICATION PLOTS-----------")
    print("-----------------------------------------")


def shaded_print():

    print("")
    print("-----------------------------------------")
    print("-----------SHADED VEGETATION-------------")
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


def intensity_print():

    print("")
    print("-----------------------------------------")
    print("-------------INTENSITY PLOT--------------")
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

    header = input_file.header

    info_print()

    print("LAS Specification =", header.major_version, ".", header.minor_version)
    print("")

    print("------------ Point data format: ------------")
    pointformat = input_file.point_format
    for spec in pointformat:
        print(spec.name)
    print("")

    print("------------ Sample point data: ------------")
    print(point_records[0])
    print("")

    print("------------ Header data: ------------")

    header_specs = (
        "file_signature",
        "file_source_id",
        "global_encoding",
        "gps_time_type",
        "guid",
        "version_major",
        "version_minor",
        "system_id",
        "software_id",
        "header_size",
        "data_offset",
        "data_format_id",
        "data_record_length",
        "records_count",
        "point_return_count",
        "scale",
        "offset",
        "max",
        "min",
        "start_first_evlr",
    )

    for spec in header_specs:
        try:
            print(spec, ":", getattr(header, spec))
        except:
            print(spec, ": value not found")
    print("")

    print("------------ VLR's: ------------")

    for count, rec in enumerate(header.vlrs):
        print("~~~ VLR #" + str(count), "~~~")
        print("Description:", rec.description)
        print("VLR content:")
        print(rec.VLR_body)
        print("")

    print("------ EVLR's: ------")

    for rec in header.evlrs:
        print(rec)
    print("")

    complete()
