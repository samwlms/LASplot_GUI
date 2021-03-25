# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

import os

# this will vary depending on launch point (cli.py/ LASplot.py)
try:
    from python import printer
except ModuleNotFoundError:
    import printer


def make_world_file(source, destination):
    base = os.path.basename(source).split(".")[0] + ".pgw"
    f = open(os.path.join(destination, base), "w+")
    f.write("this is a test file")
    f.close()
