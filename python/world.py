# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

import printer, os


def make_world_file(source, destination):
    base = os.path.basename(source).split(".")[0] + ".pgw"
    f = open(os.path.join(destination, base), "w+")
    f.write("this is a test file")
    f.close()
