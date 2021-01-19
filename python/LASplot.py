# Written by: Sam Williams
# Contact: Swilliams9@uon.edu.au
# Project is open for use/ collaboration by all!

from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import plot, printer, gradient, intensity, os


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
    # ensure input and output variables have a value
    s_bool = source_var.get() != ""
    d_bool = destination_var.get() != ""

    # ensure the input for size and dpi are valid
    dpi_bool = dpi_var.get().isnumeric()
    size_bool = preview_size_var.get().isnumeric()

    if all([s_bool, d_bool, dpi_bool, size_bool]):
        return True


def change_img(event):
    # when the file selection is updated - update image
    img_index = file_box.curselection()[0]
    img_display.configure(image=images[img_index])
    img_display.update()


def handler():
    if valid_inputs():
        # user variables
        source = source_var.get()
        destination = destination_var.get()
        size_int = int(size_var.get())
        preview_size_int = int(preview_size_var.get())
        dpi_int = int(dpi_var.get())

        # delete existing filenames in the listbox
        file_box.delete(0, END)

        # delete existing images in image list
        images.clear()

        # if 'layer' option is selected
        if plot_var.get() == 1:
            # plot the images to PNG
            plot.plot(source, destination, size_int, dpi_int)

        # if 'coutour' option is selected
        if gradient_var.get() == 1:
            gradient.gradient(source, destination, size_int, dpi_int)

        # if 'composite' option is selected
        if composite_var.get() == 1:
            print("")
            print("(composite image stuff goes here)")
            print("")

        # if 'print info' option is selected
        if print_var.get() == 1:
            printer.format(source_var.get())

        # if 'ground intensity' option is selected
        if ground_intensity_var.get() == 1:
            intensity.intensity(source, destination, size_int, dpi_int, 2)

        # if 'highVeg intensity' option is selected
        if highVeg_intensity_var.get() == 1:
            intensity.intensity(source, destination, size_int, dpi_int, 5)

        # get all image files at the output dir and make a list
        for the_file in os.listdir(destination_var.get()):

            if the_file.endswith("png"):
                # make a list of 'PIL photoImage' objects
                img_path = destination_var.get() + "/" + the_file
                img = Image.open(img_path).resize((preview_size_int, preview_size_int))
                images.append(ImageTk.PhotoImage(img))

                # insert the image name into the GUI listbox
                file_box.insert(END, the_file)

        # update the GUI image box with an image from the output dir
        img_display.configure(image=images[0])
        img_display.update()

    else:
        print("please select correct input values")


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
preview_size_var = StringVar()
size_var = StringVar()
dpi_var.set("25")
preview_size_var.set("800")
size_var.set("60")

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
composite_var = IntVar()
print_var = IntVar()
ground_intensity_var = IntVar()
highVeg_intensity_var = IntVar()

# window settings
root.title("LASplot")
root.geometry("1920x1080")
root.minsize(800, 400)
root.rowconfigure(0, weight=0)
root.columnconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

# a list of images that exist in the ouptu directory after plot
images = []

options_frame = LabelFrame(root, text="options")
options_frame.columnconfigure(0, weight=1)
options_frame.grid(row=0, column=0, rowspan=2, sticky=W + N, padx=5, pady=5)

img = LabelFrame(root)
img.grid(row=1, column=1, sticky=S + N + W + E, padx=5, pady=5)

img_display = Label(img, background="black")
img_display.pack(fill="both", expand=True)

# ---------------------------- CHOOSE INPUT / OUTPUT ----------------------------

# FRAME
top = LabelFrame(root, text="select file")
top.rowconfigure(0, weight=5, minsize=40)
top.columnconfigure(0, weight=1)
top.grid(row=0, column=1, sticky=N + W + E, padx=5, pady=5)
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
input_lbl = Label(top, textvariable=source_var, fg="blue")
input_lbl.grid(row=0, column=1, sticky=E, padx=5, pady=5)

# label to display chosen destination
output_lbl = Label(top, textvariable=destination_var, fg="blue")
output_lbl.grid(row=1, column=1, sticky=E, padx=5, pady=5)

# ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------

# FRAME
control_frame = LabelFrame(options_frame, text="operations")
control_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=5)

# CONTROLS
plot_chk = Checkbutton(
    control_frame,
    text="classification view",
    variable=plot_var,
)
plot_chk.grid(row=0, column=0, sticky=NW)

gradient_chk = Checkbutton(
    control_frame,
    text="ground gradient",
    variable=gradient_var,
)
gradient_chk.grid(row=1, column=0, sticky=NW)

ground_intensity_chk = Checkbutton(
    control_frame,
    text="ground intensity",
    variable=ground_intensity_var,
)
ground_intensity_chk.grid(row=2, column=0, sticky=NW)

highVeg_intensity_chk = Checkbutton(
    control_frame,
    text="highVeg intensity",
    variable=highVeg_intensity_var,
)
highVeg_intensity_chk.grid(row=3, column=0, sticky=NW)

composite_chk = Checkbutton(
    control_frame,
    text="composite image",
    variable=composite_var,
)
composite_chk.grid(row=4, column=0, sticky=NW)

print_chk = Checkbutton(
    control_frame,
    text="print info to console",
    variable=print_var,
)
print_chk.grid(row=5, column=0, sticky=NW)

# ---------------------------- CHOOSE IMAGE SETTINGS ----------------------------

# FRAME
img_settings_frame = LabelFrame(options_frame, text="image")
img_settings_frame.columnconfigure(0, weight=1)
img_settings_frame.columnconfigure(1, weight=0)
img_settings_frame.grid(row=1, column=0, sticky=N + S + W + E, padx=5, pady=5)

# CONTROLS
dpi_label = Label(img_settings_frame, text="output DPI")
dpi_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)

dpi_input = Entry(img_settings_frame, textvariable=dpi_var, width=7)
dpi_input.grid(row=3, column=1, sticky=E, padx=5, pady=5)

size_label = Label(img_settings_frame, text="output size")
size_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)

size_label = Entry(img_settings_frame, textvariable=size_var, width=7)
size_label.grid(row=4, column=1, sticky=E, padx=5, pady=5)

preview_size_label = Label(img_settings_frame, text="preview size")
preview_size_label.grid(row=5, column=0, sticky=W, padx=5, pady=5)

preview_size_label = Entry(img_settings_frame, textvariable=preview_size_var, width=7)
preview_size_label.grid(row=5, column=1, sticky=E, padx=5, pady=5)

# ---------------------------- CHOOSE PLOT SETTINGS ----------------------------

# FRAME
plot_frame = LabelFrame(options_frame, text="plot")
plot_frame.columnconfigure(0, weight=1)
plot_frame.columnconfigure(1, weight=0)
plot_frame.grid(row=2, column=0, sticky=N + S + W + E, padx=5, pady=5)

# CONTROLS
plot_chk = Checkbutton(
    plot_frame,
    text="ground",
    variable=ground_var,
)
plot_chk.grid(row=0, column=0, sticky=NW)

gradient_chk = Checkbutton(
    plot_frame,
    text="buildings",
    variable=buildings_var,
)
gradient_chk.grid(row=1, column=0, sticky=NW)

composite_chk = Checkbutton(
    plot_frame,
    text="unclassified",
    variable=unclassified_var,
)
composite_chk.grid(row=2, column=0, sticky=NW)

print_chk = Checkbutton(
    plot_frame,
    text="water",
    variable=water_var,
)
print_chk.grid(row=3, column=0, sticky=NW)

print_chk = Checkbutton(
    plot_frame,
    text="low veg",
    variable=lowVeg_var,
)
print_chk.grid(row=4, column=0, sticky=NW)

print_chk = Checkbutton(
    plot_frame,
    text="medium veg",
    variable=mediumVeg_var,
)
print_chk.grid(row=5, column=0, sticky=NW)

print_chk = Checkbutton(
    plot_frame,
    text="high veg",
    variable=highVeg_var,
)
print_chk.grid(row=6, column=0, sticky=NW)


# ---------------------------- BEGIN IMAGE PROCESSING ----------------------------
# GO button config
begin_btn = Button(
    top,
    text="BEGIN",
    command=handler,
    background="dodgerblue",
    foreground="white",
    padx=5,
    pady=5,
)
begin_btn.grid(row=0, column=3, rowspan=2, sticky=N + S + W + E, padx=5, pady=5)

# ---------------------------- CHOOSE IMAGE TO VIEW ----------------------------
# FRAME
control_frame = LabelFrame(options_frame, text="view image")
control_frame.grid(row=4, column=0, sticky=N + S + W + E, padx=5, pady=5)

# LISTBOX
file_box = Listbox(control_frame)
file_box.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=5)

# update the image to match selection
file_box.bind("<<ListboxSelect>>", change_img)

if __name__ == "__main__":
    # run main window
    root.mainloop()
