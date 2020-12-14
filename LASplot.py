from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt
import time

# initialise window
root = Tk()

# input/ output variables
source_var = StringVar()
destination_var = StringVar()

# checkbox variables
plot_var = IntVar()
contour_var = IntVar()
composite_var = IntVar()

# window settings
root.title("LASplot")
root.geometry("900x500")
root.minsize(500, 350)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


def main():

    # configure background image
    # icon = PhotoImage(file="icon.png")
    # Label(root, image=icon, background="white").grid(row=2, column=1, sticky=N)

    # ---------------------------- CHOOSE INPUT / OUTPUT ----------------------------
    file_frame = LabelFrame(root, text="user input/ output")
    file_frame.rowconfigure(0, weight=1)
    file_frame.columnconfigure(0, weight=1)
    file_frame.grid(row=0, column=0, columnspan=2, sticky=N + W + E, padx=10, pady=10)

    # button to select input file
    input_btn = Button(
        file_frame,
        text="Select file",
        command=choose_source,
        foreground="black",
    )
    input_btn.grid(row=0, column=0, sticky=W, padx=5, pady=5)

    # button to select output destination
    output_btn = Button(
        file_frame,
        text="Output dir",
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

    # ---------------------------- CHOOSE IMAGE SETTINGS ----------------------------
    options_frame = LabelFrame(root, text="image options")
    options_frame.rowconfigure(0, weight=1)
    options_frame.columnconfigure(0, weight=1)
    options_frame.grid(row=3, column=0, sticky=W + S, padx=10, pady=10)

    dpi_label = Label(options_frame, text="DPI")
    dpi_label.grid(row=3, column=0, sticky=W + E, padx=10, pady=10)

    dpi_input = Entry(options_frame)
    dpi_input.grid(row=3, column=1, sticky=W + E, padx=10, pady=10)

    size_label = Label(options_frame, text="SIZE")
    size_label.grid(row=4, column=0, sticky=W + E, padx=10, pady=10)

    size_label = Entry(options_frame)
    size_label.grid(row=4, column=1, sticky=W + E, padx=10, pady=10)

    # ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------
    # frame to contain/ group user controls
    control_frame = LabelFrame(root, text="output controls")
    control_frame.rowconfigure(0, weight=1)
    control_frame.columnconfigure(0, weight=1)
    control_frame.grid(row=2, column=0, sticky=W + S, padx=10, pady=10)

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
        variable=composite_var,
    )
    composite_chk.grid(row=2, column=0, sticky=NW)

    # ---------------------------- BEGIN IMAGE PROCESSING ----------------------------
    # GO button config
    begin_btn = Button(
        root,
        text="BEGIN",
        command=handler,
        background="dodgerblue",
        foreground="white",
        padx=10,
        pady=10,
    )
    begin_btn.grid(row=1, column=1, sticky=SE, padx=10, pady=10)

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


def valid_inputs():
    if source_var.get() != "" and destination_var.get() != "":
        return True


def handler():
    if valid_inputs():
        if plot_var.get() == 1:
            plot()
        if contour_var.get() == 1:
            print("do contour stuff....")
        if composite_var.get() == 1:
            print("do composite stuff....")
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
    print("---------------------------HEADER INFORMATION--------------------------")
    print("LAS specification = " + input_file.header.version)
    print("point format = " + str(las_specification))
    print("total point count = " + str(input_file.header.count))
    print("-----------------------------------------------------------------------")


if __name__ == "__main__":
    main()
