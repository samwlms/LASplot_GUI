# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
from pathlib import Path
import printer, plotters, world
from tempfile import TemporaryDirectory

# allows user to select a las file input
def choose_source():
    path = Path(
        filedialog.askopenfilename(
            title="Select a LAS file", filetypes=(("las Files", "*.las"),)
        )
    )

    if path.is_file():
        source_var.set(path)


# allows user to define desired output for the files
def choose_dest():
    dest = Path(filedialog.askdirectory())

    if dest.is_dir() and dest.is_absolute():
        destination_var.set(dest)


# upon selection of the 'classification view' or 'composite'
# checkbox, toggle the state of classification options
def plot_checked():
    if plot_var.get() or composite_var.get() == 1:
        ground_chk.configure(state="normal")
        buildings_chk.configure(state="normal")
        unclassified_chk.configure(state="normal")
        water_chk.configure(state="normal")
        lowVeg_chk.configure(state="normal")
        mediumVeg_chk.configure(state="normal")
        highVeg_chk.configure(state="normal")
    else:
        ground_var.set(0)
        buildings_var.set(0)
        unclassified_var.set(0)
        water_var.set(0)
        lowVeg_var.set(0)
        mediumVeg_var.set(0)
        highVeg_var.set(0)

        ground_chk.configure(state="disabled")
        buildings_chk.configure(state="disabled")
        unclassified_chk.configure(state="disabled")
        water_chk.configure(state="disabled")
        lowVeg_chk.configure(state="disabled")
        mediumVeg_chk.configure(state="disabled")
        highVeg_chk.configure(state="disabled")


def get_plot_args():
    arguments = []
    if ground_var.get() == 1:
        arguments.append(2)
    if water_var.get() == 1:
        arguments.append(9)
    if lowVeg_var.get() == 1:
        arguments.append(3)
    if mediumVeg_var.get() == 1:
        arguments.append(4)
    if buildings_var.get() == 1:
        arguments.append(6)
    if unclassified_var.get() == 1:
        arguments.append(1)
    if highVeg_var.get() == 1:
        arguments.append(5)

    return arguments


def valid_inputs():
    # check to see if the input arguments are correct before proceeding
    # with any plotting. (checks input dir and > 1 plot options)
    input_bool = any(
        [
            gradient_var.get() == 1,
            contour_var.get() == 1,
            ground_intensity_var.get() == 1,
            world_var.get() == 1,
            highVeg_shaded_var.get() == 1,
            print_var.get() == 1,
            ground_var.get() == 1,
            water_var.get() == 1,
            lowVeg_var.get() == 1,
            mediumVeg_var.get() == 1,
            buildings_var.get() == 1,
            unclassified_var.get() == 1,
            highVeg_var.get() == 1,
        ]
    )
    return all(
        [
            input_bool,
            source_var.get() != "",
            dpi_var.get().isnumeric(),
            size_var.get().isnumeric(),
            preview_size_var.get().isnumeric(),
            contour_height_var.get().isnumeric(),
        ]
    )


def change_img(event):
    try:
        # when the file selection is updated - update image
        img_index = file_box.curselection()[0]
        img_display.configure(image=images[img_index])
        img_display.update()
    except Exception as e:
        print("ERROR: no images to select ({})".format(e))


def handler():
    if not valid_inputs():
        print("ERROR: please select valid input and/or plot options")
        return

    td = TemporaryDirectory()
    # user variables
    src = source_var.get()
    out = destination_var.get()
    size = int(size_var.get())
    preview_size = int(preview_size_var.get())
    dpi = int(dpi_var.get())
    marker = marker_var.get()
    contour_height = int(contour_height_var.get())
    layers = get_plot_args()

    if out == "" or out == "NO OUTPUT":
        if out == "":
            destination_var.set("NO OUTPUT")
        out = td.name
        print("INFO: No output selected - using temp directory")

    args = src, out, size, dpi, marker

    # delete existing filenames in the listbox
    file_box.delete(0, END)

    # delete existing images in image list
    images.clear()

    # if 'layer' option is selected
    if plot_var.get() == 1:
        plotters.LayerPlotter("plot", *args, layers).plot()
    # if 'gradient' option is selected
    if gradient_var.get() == 1:
        plotters.GradientPlotter("gradient", *args).plot_gradient()
    # if 'contour' option is selected
    if contour_var.get() == 1:
        plotters.ContourPlotter(*args, contour_height).plot_contour()
    # if 'composite' option is selected
    if composite_var.get() == 1:
        plotters.LayerPlotter("composite", *args, layers).plot()
    # if 'ground intensity' option is selected
    if ground_intensity_var.get() == 1:
        plotters.GradientPlotter("intensity", *args).plot_gradient()
    # if 'generate world files' option is selected
    if world_var.get() == 1:
        world.make_world_file(src, out)
    # if 'highVeg shaded' option is selected
    if highVeg_shaded_var.get() == 1:
        plotters.VegShader(*args).plot_shaded()
    # if 'print info' option is selected
    if print_var.get() == 1:
        printer.format(src)

    # get all image files at the output dir and make a list
    for the_file in Path(out).glob("*.png"):
        img = Image.open(the_file).resize((preview_size, preview_size))
        images.append(ImageTk.PhotoImage(img))
        file_box.insert(END, the_file.name)

    if len(images) != 0:
        img_display.configure(image=images[0])
        img_display.update()


# set the style for the application
def set_style(parent):
    for child in parent.winfo_children():
        c_class = child.winfo_class()
        name = child.winfo_name()
        if c_class == "Checkbutton" or c_class == "Radiobutton":
            child.configure(selectcolor="black")
        if name != "top_panel" and name != "png_display":
            child.configure(fg="white")
            if c_class != ("Button" or "Listbox"):
                child.configure(bg="gray20")
            if c_class == "Listbox":
                child.configure(bg="gray30")

            set_style(child)


# -----------------------------------------------------------------------------
# --------------------------GUI CONFIGURATION AND LAYOUT-----------------------
# -----------------------------------------------------------------------------

# having all this graphical code just thrown in to one file isn't ideal
# TO DO: investigate ways so split it up and make it more readable. Maybe OOP

# initialise window
root = Tk()

# input/ output variables
source_var = StringVar()
destination_var = StringVar()

# image settings variables
dpi_var = StringVar()
dpi_var.set("20")
preview_size_var = StringVar()
preview_size_var.set("850")
size_var = StringVar()
size_var.set("50")
marker_var = StringVar()
marker_var.set(".")

# contour settings variables
contour_height_var = StringVar()
contour_height_var.set("2")

# GIS settings variables
world_var = IntVar()

# plot settings variables
buildings_var = IntVar()
ground_var = IntVar()
unclassified_var = IntVar()
lowVeg_var = IntVar()
mediumVeg_var = IntVar()
highVeg_var = IntVar()
water_var = IntVar()

# checkbox variables
plot_var = IntVar()
gradient_var = IntVar()
contour_var = IntVar()
composite_var = IntVar()
print_var = IntVar()
ground_intensity_var = IntVar()
highVeg_shaded_var = IntVar()

# window settings
root.title("LASplot")
root.geometry("1920x1080")
root.configure(bg="black")
root.minsize(800, 400)
root.rowconfigure(0, weight=0)
root.columnconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

# a list of images that exist in the ouptu directory after plot
images = []

options_frame = LabelFrame(
    root, fg="white", bg="gray20", borderwidth=0, highlightthickness=0
)
options_frame.columnconfigure(0, weight=1)
options_frame.grid(row=0, column=0, rowspan=2, sticky=W + N + S, padx=5, pady=5)

img = LabelFrame(root, borderwidth=0, highlightthickness=0)
img.grid(row=1, column=1, sticky=S + N + W + E, padx=5, pady=5)

img_display = Label(img, bg="black", name="png_display")
img_display.pack(fill="both", expand=True)

# ---------------------------- CHOOSE INPUT / OUTPUT ----------------------------

# FRAME
top = LabelFrame(
    root, bg="black", borderwidth=0, highlightthickness=0, name="top_panel"
)
top.columnconfigure(0, weight=1)
top.grid(row=0, column=1, sticky=N + W + E, padx=5, pady=5)
# button to select input file
Button(
    top,
    text="SELECT FILE",
    command=choose_source,
    fg="black",
    bg="orange",
).grid(row=0, column=0, sticky=W + N + S, padx=5, pady=5)

# button to select output destination
Button(top, text="OUTPUT DIR", command=choose_dest, fg="black", bg="orange").grid(
    row=1, column=0, sticky=W + N + S, padx=5, pady=5
)

# label to display chosen file
input_lbl = Label(top, textvariable=source_var, fg="cyan", bg="black")
input_lbl.grid(row=0, column=1, sticky=E, padx=5, pady=5)

# label to display chosen destination
output_lbl = Label(top, textvariable=destination_var, fg="cyan", bg="black")
output_lbl.grid(row=1, column=1, sticky=E, padx=5, pady=5)

# ---------------------------- BEGIN IMAGE PROCESSING ----------------------------
# GO button config
Button(
    top,
    text="BEGIN",
    command=handler,
    bg="dodgerblue",
    fg="white",
    font=10,
).grid(row=0, column=3, rowspan=2, sticky=N + S + W + E, padx=5, pady=5)


# ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------

# FRAME
control_frame = LabelFrame(
    options_frame,
    text="Operations",
    borderwidth=0,
    font=10,
)
control_frame.pack(pady=10, padx=5, fill="both")

# CONTROLS
Checkbutton(
    control_frame,
    text="classification view",
    variable=plot_var,
    command=plot_checked,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="ground gradient",
    variable=gradient_var,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="ground contour",
    variable=contour_var,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="ground intensity",
    variable=ground_intensity_var,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="shaded veg",
    variable=highVeg_shaded_var,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="composite image",
    variable=composite_var,
    command=plot_checked,
).pack(anchor=W)
Checkbutton(
    control_frame,
    text="print file info",
    variable=print_var,
).pack(anchor=W)

# ---------------------------- CHOOSE PLOT SETTINGS ----------------------------

# FRAME
plot_frame = LabelFrame(
    options_frame,
    text="Layers",
    borderwidth=0,
    font=10,
)
plot_frame.pack(pady=10, padx=5, fill="both")

# CONTROLS
ground_chk = Checkbutton(
    plot_frame,
    text="ground",
    variable=ground_var,
    state=DISABLED,
)
ground_chk.pack(anchor=W)
buildings_chk = Checkbutton(
    plot_frame,
    text="buildings",
    variable=buildings_var,
    state=DISABLED,
)
buildings_chk.pack(anchor=W)
unclassified_chk = Checkbutton(
    plot_frame,
    text="unclassified",
    variable=unclassified_var,
    state=DISABLED,
)
unclassified_chk.pack(anchor=W)
water_chk = Checkbutton(
    plot_frame,
    text="water",
    variable=water_var,
    state=DISABLED,
)
water_chk.pack(anchor=W)
lowVeg_chk = Checkbutton(
    plot_frame,
    text="low veg",
    variable=lowVeg_var,
    state=DISABLED,
)
lowVeg_chk.pack(anchor=W)
mediumVeg_chk = Checkbutton(
    plot_frame,
    text="medium veg",
    variable=mediumVeg_var,
    state=DISABLED,
)
mediumVeg_chk.pack(anchor=W)
highVeg_chk = Checkbutton(
    plot_frame,
    text="high veg",
    variable=highVeg_var,
    state=DISABLED,
)
highVeg_chk.pack(anchor=W)


# ---------------------------- GIS SPECIFIC SETTINGS ----------------------------

# FRAME
gis_frame = LabelFrame(
    options_frame, text="GIS", fg="white", bg="gray20", borderwidth=0, font=10
)
gis_frame.pack(pady=10, padx=5, fill="both")

Checkbutton(
    gis_frame,
    text="generate world file",
    variable=world_var,
).pack(anchor=W)

# ---------------------------- CHOOSE MARKER SETTINGS ----------------------------

# FRAME (marker stype)
marker_frame = LabelFrame(
    options_frame,
    text="Marker style",
    borderwidth=0,
    font=10,
)
marker_frame.pack(pady=10, padx=5, fill="both")

Radiobutton(
    marker_frame,
    text="pixel (small)",
    variable=marker_var,
    value=",",
).pack(anchor=W)
Radiobutton(
    marker_frame,
    text="point (medium)",
    variable=marker_var,
    value=".",
).pack(anchor=W)
Radiobutton(
    marker_frame,
    text="circle (large)",
    variable=marker_var,
    value="o",
).pack(anchor=W)
Radiobutton(
    marker_frame,
    text="square (large)",
    variable=marker_var,
    value="s",
).pack(anchor=W)

# ---------------------------- CHOOSE CONTOUR HEIGHT ----------------------------

# FRAME
contour_frame = LabelFrame(
    options_frame,
    text="Contour height",
    borderwidth=0,
    font=10,
)
contour_frame.pack(pady=10, padx=5, fill="both")


# CONTROLS
Label(
    contour_frame,
    text="meters",
).grid(row=0, column=1, sticky=W)
contour_input = Entry(
    contour_frame,
    textvariable=contour_height_var,
    width=5,
)
contour_input.grid(row=0, column=0, sticky=E, padx=5, pady=5)


# ---------------------------- CHOOSE IMAGE SETTINGS ----------------------------

# FRAME
settings_frame = LabelFrame(
    options_frame,
    text="Size options",
    borderwidth=0,
    font=10,
)
settings_frame.pack(pady=10, padx=5, fill="both")


# CONTROLS
Label(
    settings_frame,
    text="output DPI",
).grid(row=3, column=1, sticky=W)
dpi_input = Entry(
    settings_frame,
    textvariable=dpi_var,
    width=5,
)
dpi_input.grid(row=3, column=0, sticky=E, padx=5, pady=5)
Label(
    settings_frame,
    text="output size",
).grid(row=4, column=1, sticky=W)
size_input = Entry(
    settings_frame,
    textvariable=size_var,
    width=5,
)
size_input.grid(row=4, column=0, sticky=E, padx=5, pady=5)
Label(
    settings_frame,
    text="preview size",
).grid(row=5, column=1, sticky=W)
preview_size_input = Entry(
    settings_frame,
    textvariable=preview_size_var,
    width=5,
)
preview_size_input.grid(row=5, column=0, sticky=E, padx=5, pady=5)


# ---------------------------- CHOOSE IMAGE TO VIEW ----------------------------
# FRAME
list_frame = LabelFrame(
    options_frame,
    text="Choose image",
    borderwidth=0,
    font=10,
    relief="flat",
    highlightthickness=0,
)
list_frame.pack(pady=10, padx=5, fill="both", side=BOTTOM)

# LISTBOX
file_box = Listbox(
    list_frame,
    borderwidth=0,
    relief="flat",
    highlightthickness=0,
)
file_box.pack(fill=X)

# update the image to match selection
file_box.bind("<<ListboxSelect>>", change_img)


if __name__ == "__main__":
    # set the style for the main window
    set_style(root)
    # run main window
    root.mainloop()
