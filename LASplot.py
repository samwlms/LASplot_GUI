from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from laspy.file import File
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
import time
import plot


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
root.geometry("1920x1080")
root.minsize(800, 400)
root.rowconfigure(0, weight=1, minsize=120)
root.columnconfigure(0, weight=1, minsize=250)


def main():

    # configure background image
    # icon = PhotoImage(file="icon.png")
    # Label(root, image=icon, background="white").grid(row=2, column=1, sticky=N)

    # ------------------------- GUI FRAMES (TOP, LEFT, IMG) -------------------------
    # the top level panel (input/ output files)
    top = LabelFrame(root, text="user input/ output")
    top.rowconfigure(0, weight=1, minsize=40)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, columnspan=2, sticky=N + W + E, padx=10, pady=5)

    left = LabelFrame(root, text="options")
    left.rowconfigure(0, weight=1)
    left.columnconfigure(0, weight=1)
    left.grid(row=1, column=0, sticky=N + W + S, padx=10, pady=5)

    img = LabelFrame(root)
    img.grid(row=1, column=1, sticky=N + W + E + S, padx=10, pady=5)

    img_var = ImageTk.PhotoImage(Image.open("icon.png"))
    img_display = Label(img, image=img_var)
    img_display.grid(row=0, column=1, sticky=N + W + E + S, padx=10, pady=5)
    # ---------------------------- CHOOSE INPUT / OUTPUT ----------------------------

    # button to select input file
    input_btn = Button(
        top,
        text="Select file",
        command=choose_source,
        foreground="black",
    )
    input_btn.grid(row=0, column=0, sticky=W, padx=5, pady=5)

    # button to select output destination
    output_btn = Button(
        top,
        text="Output dir",
        command=choose_dest,
        foreground="black",
    )
    output_btn.grid(row=1, column=0, sticky=W, padx=5, pady=5)

    # label to display chosen file
    input_lbl = Label(top, textvariable=source_var)
    input_lbl.grid(row=0, column=1, sticky=E, padx=5, pady=5)

    # label to display chosen destination
    output_lbl = Label(top, textvariable=destination_var)
    output_lbl.grid(row=1, column=1, sticky=E, padx=5, pady=5)

    # ---------------------------- CHOOSE IMAGE SETTINGS ----------------------------
    options_frame = LabelFrame(left, text="image options")
    options_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=10, pady=5)

    dpi_label = Label(options_frame, text="DPI")
    dpi_label.grid(row=3, column=0, sticky=W + E, padx=5, pady=5)

    dpi_input = Entry(options_frame)
    dpi_input.grid(row=3, column=1, sticky=W + E, padx=5, pady=5)

    size_label = Label(options_frame, text="SIZE")
    size_label.grid(row=4, column=0, sticky=W + E, padx=5, pady=5)

    size_label = Entry(options_frame)
    size_label.grid(row=4, column=1, sticky=W + E, padx=5, pady=5)

    # ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------
    # frame to contain/ group user controls
    control_frame = LabelFrame(left, text="output controls")
    control_frame.grid(row=1, column=0, sticky=N + S + W + E, padx=10, pady=5)

    # output generation settings (1/0)
    plot_chk = Checkbutton(
        control_frame,
        text="Individual classification layers",
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
        left,
        text="BEGIN",
        command=handler,
        background="dodgerblue",
        foreground="white",
        padx=10,
        pady=5,
    )
    begin_btn.grid(row=2, column=0, sticky=N + S + W + E, padx=10, pady=5)

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


def valid_inputs():
    if source_var.get() != "" and destination_var.get() != "":
        return True


def handler():
    if valid_inputs():
        if plot_var.get() == 1:
            plot.plot(source_var.get(), destination_var.get(), 100, 20)
        if contour_var.get() == 1:
            print("do contour stuff....")
        if composite_var.get() == 1:
            print("do composite stuff....")
    else:
        print("please select correct input values")


if __name__ == "__main__":
    main()
