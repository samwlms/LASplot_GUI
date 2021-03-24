# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from laspy.file import File
import laspy
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, init


def saved(filename, time):

    init()
    string_time = str(round(time, 2)) + "s"
    print(Fore.YELLOW + filename, "saved in", string_time)


def plot_print():

    init()
    print("")
    print(Fore.CYAN + "|||||||||| CLASSIFICATION PLOTS |||||||||||")
    print("")


def contour_print():

    init()
    print("")
    print(Fore.CYAN + "|||||||||||||| CONTOUR PLOT |||||||||||||||")
    print("")


def composite_print():

    init()
    print("")
    print(Fore.CYAN + "|||||||||||| COMPOSITE IMAGERY ||||||||||||")
    print("")


def shaded_print():

    init()
    print("")
    print(Fore.CYAN + "||||||||||| SHADED VEGETATION |||||||||||||")
    print("")


def contour_print():

    init()
    print("")
    print(Fore.CYAN + "|||||||||||||| CONTOUR PLOT |||||||||||||||")
    print("")


def gradient_print():

    init()
    print("")
    print(Fore.CYAN + "||||||||||||| GRADIENT PLOT |||||||||||||||")
    print("")


def intensity_print():

    init()
    print("")
    print(Fore.CYAN + "||||||||||||| INTENSITY PLOT ||||||||||||||")
    print("")


def info_print():

    init()
    print("")
    print(Fore.CYAN + "|||||||||||||||| FILE INFO ||||||||||||||||")
    print("")


def complete():

    init()
    print()
    print(Fore.GREEN + "process complete")
    print("")


def format(input):

    # read in LAS file and specify point records, las spec
    input_file = File(input, mode="r")
    point_records = input_file.points
    pointformat = input_file.point_format

    header = input_file.header

    info_print()

    print(
        Fore.YELLOW + "LAS Specification =",
        Fore.GREEN + str(header.major_version) + str(header.minor_version),
    )
    print("")

    print(Fore.CYAN + "||||||| Point format: |||||||")
    pointformat = input_file.point_format
    for spec in pointformat:
        print(Fore.YELLOW + spec.name)
    print("")

    print(Fore.CYAN + "||||||| Sample points: |||||||")
    print(Fore.YELLOW + str(point_records[0]))
    print("")

    print(Fore.CYAN + "||||||| Header data: |||||||")

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
        "scale",
        "offset",
        "max",
        "min",
        "start_first_evlr",
    )

    for spec in header_specs:
        try:
            print(Fore.YELLOW + spec, ":", Fore.GREEN + getattr(header, spec))
        except:
            print(Fore.YELLOW + spec, ":", Fore.RED + "value not found")
    print("")

    print(Fore.CYAN + "||||||| VLR's: |||||||")

    for count, rec in enumerate(header.vlrs):
        print(Fore.WHITE + "~~~ VLR #" + str(count), "~~~")
        print(Fore.YELLOW + "Description:")
        print(Fore.GREEN + rec.description)
        print(Fore.YELLOW + "VLR content:")
        print(Fore.GREEN + str(rec.VLR_body))
        print("")

    print(Fore.CYAN + "|||||| EVLR's: ||||||")

    for rec in header.evlrs:
        print(Fore.YELLOW + rec)
    print("")

    complete()
