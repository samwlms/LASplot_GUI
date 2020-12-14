from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt
import time

# -----initialise window-----
root = Tk()

# -----GUI text variables-----
source_var = StringVar()

destination_var = StringVar()

plot_var = IntVar()
plot_var.set(1)

contour_var = IntVar()
contour_var.set(1)


# window settings
root.title("LASplot")
root.resizable(0, 0)
root.configure(background="white")


def main():

    # configure background image
    icon = PhotoImage(file="icon.png")
    Label(root, image=icon, background="white").grid(row=2, column=1, sticky=N)

    # ---------------------------- CHOOSE INPUT / OUTPUT ----------------------------
    file_frame = LabelFrame(root, text="output controls")
    file_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)

    # button to select input file
    input_btn = Button(
        file_frame,
        text="INPUT FILE/S",
        command=choose_source,
        foreground="black",
    )
    input_btn.grid(row=0, column=0, sticky=W, padx=5, pady=5)

    # button to select output destination
    output_btn = Button(
        file_frame,
        text="DESTINATION",
        command=choose_dest,
        foreground="black",
    )
    output_btn.grid(row=1, column=0, sticky=W, padx=5, pady=5)

    # label to display chosen file
    input_lbl = Label(file_frame, textvariable=source_var)
    input_lbl.grid(row=0, column=1, sticky=E)

    # label to display chosen destination
    output_lbl = Label(file_frame, textvariable=destination_var)
    output_lbl.grid(row=1, column=1, sticky=E)

    # ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------
    # frame to contain/ group user controls
    control_frame = LabelFrame(root, text="output controls")
    control_frame.grid(row=2, column=0, sticky=NW, padx=10, pady=10)

    # output generation settings (1/0)
    plot_chk = Checkbutton(
        control_frame,
        text="Layer seperated plot",
        variable=plot_var,
    )
    plot_chk.grid(row=0, column=0, sticky=NW)

    # output generation settings (1/0)
    contour_chk = Checkbutton(
        control_frame,
        text="Groud contour",
        variable=contour_var,
    )
    contour_chk.grid(row=1, column=0, sticky=NW)

    # output generation settings (1/0)
    composite_chk = Checkbutton(
        control_frame,
        text="Composite image",
        variable=contour_var,
    )
    composite_chk.grid(row=2, column=0, sticky=NW)

    # ---------------------------- BEGIN IMAGE PROCESSING ----------------------------
    # GO button config
    begin_btn = Button(
        root,
        text="BEGIN",
        command=handler,
        padx=10,
        pady=10,
    )
    begin_btn.grid(row=2, column=1, sticky=SE)

    # run main window
    root.mainloop()


# allows user to select a las file input
def choose_source():
    path = filedialog.askopenfilename(
        title="Select one or more .LAS files", filetypes=(("las Files", "*.las"),)
    )

    if path != "":
        source_var.set(path)


# allows user to define desired output for the files
def choose_dest():
    destination_var.set(filedialog.askdirectory())


# get the positional data of points in a specified classification
def get_xy(in_points, classification):
    x = in_points.X[in_points.Classification == classification]
    y = in_points.Y[in_points.Classification == classification]
    return x, y


def handler():
    if source_var.get() != "" and destination_var.get() != "":
        plot()
    else:
        print("please select correct input values")


# plot the positional data and then save as PNG
def plot():
    size = 100
    dpi = 20

    # read in LAS file and specify point records, las spec
    input_file = File(source_var.get(), mode="r")
    point_records = input_file.points
    las_specification = input_file.point_format.fmt

    # get the min/max X,Y values to normalise the plot scale
    x_min, x_max = np.amin(input_file.X), np.amax(input_file.X)
    y_min, y_max = np.amin(input_file.Y), np.amax(input_file.Y)

    # print output of derived header information
    print_header_info(input_file, point_records, las_specification)

    # initialise point-variable arrays
    buildings = get_xy(input_file, 6)
    unclassified = get_xy(input_file, 1)
    ground = get_xy(input_file, 2)
    lowVeg = get_xy(input_file, 3)
    medVeg = get_xy(input_file, 4)
    highVeg = get_xy(input_file, 5)
    water = get_xy(input_file, 9)

    # basic params for the plot function
    plt.rcParams["figure.figsize"] = [size, size]
    plt.rcParams["figure.facecolor"] = "black"

    print("")
    print("CLASSIFICATION PLOT")
    print("-----------------------------------------")

    const_args = dpi, x_min, x_max, y_min, y_max

    # save the individual layer plots as .PNG
    save(*unclassified, "/unclassified.png", "m", *const_args)
    save(*ground, "/ground.png", "SaddleBrown", *const_args)
    save(*lowVeg, "/lowVeg.png", "LimeGreen", *const_args)
    save(*medVeg, "/mediumVeg.png", "Green", *const_args)
    save(*highVeg, "/highVeg.png", "DarkGreen", *const_args)
    save(*buildings, "/buildings.png", "White", *const_args)
    save(*water, "/water.png", "DodgerBlue", *const_args)

    print("-----------------------------------------")
    print("process complete")


# save the plotted images
def save(x_, y_, filename_, color_, dpi, x_min, x_max, y_min, y_max):
    plt.plot(x_, y_, color=color_, linestyle="none", marker=",")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.margins(0, 0)
    plt.gca().set_facecolor("black")
    fig = plt.gcf()
    fig.savefig(
        destination_var.get() + filename_,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black",
    )
    plt.clf()
    print(filename_, "saved successfully")


def print_header_info(input_file, point_records, las_specification):
    print(
        "---------------------------------HEADER INFORMATION--------------------------------"
    )
    print("LAS specification = " + input_file.header.version)
    print("point format = " + str(las_specification))
    print("total point count = " + str(input_file.header.count))
    print("sample point array = " + str(point_records[0][0]))
    print(
        "-----------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    main()
