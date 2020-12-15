from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import plot, printer, contour, os


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
    size_bool = size_var.get().isnumeric()

    if all([s_bool, d_bool, dpi_bool, size_bool]):
        return True


def handler():
    if valid_inputs():
        # user variables
        source = source_var.get()
        destination = destination_var.get()
        size_int = int(size_var.get())
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
        if contour_var.get() == 1:
            contour.contour(source, destination, size_int, dpi_int)

        # if 'composite' option is selected
        if composite_var.get() == 1:
            print("do composite stuff....")

        # if 'print info' option is selected
        if print_var.get() == 1:
            printer.test(source_var.get())

        # get all image files at the output dir and make a list
        for the_file in os.listdir(destination_var.get()):

            if the_file.endswith("png"):
                # make a list of 'PIL photoImage' objects
                img_path = destination_var.get() + "/" + the_file
                img = Image.open(img_path).resize((1000, 1000))
                images.append(ImageTk.PhotoImage(img))

                # insert the image name into the GUI listbox
                file_box.insert(END, the_file)

        # update the GUI image box with an image from the output dir
        img_display.configure(image=images[0])
        img_display.update()

    else:
        print("please select correct input values")


# initialise window
root = Tk()

# input/ output variables
source_var = StringVar()
destination_var = StringVar()

# image settings variables
dpi_var = StringVar()
size_var = StringVar()
dpi_var.set("25")
size_var.set("100")

# checkbox variables
plot_var = IntVar()
contour_var = IntVar()
composite_var = IntVar()
print_var = IntVar()

# window settings
root.title("LASplot")
root.geometry("1100x950")
root.minsize(800, 400)
root.rowconfigure(0, weight=0, minsize=120)
root.columnconfigure(0, weight=0, minsize=250)
root.rowconfigure(1, weight=0)
root.columnconfigure(1, weight=1)

# a list of images that exist in the ouptu directory after plot
images = []

# ------------------------- GUI FRAMES (TOP, LEFT, IMG) -------------------------
# the top level panel (input/ output files)
top = LabelFrame(root, text="user input/ output")
top.rowconfigure(0, weight=5, minsize=40)
top.columnconfigure(0, weight=1)
top.grid(row=0, column=0, columnspan=2, sticky=N + W + E, padx=10, pady=5)

left = LabelFrame(root, text="options")
left.rowconfigure(0, weight=1)
left.columnconfigure(0, weight=1)
left.grid(row=1, column=0, sticky=W + N, padx=10, pady=5)

img = LabelFrame(root)
img.grid(row=1, column=1, sticky=S + N + W + E, padx=10, pady=5)

img_display = Label(img)
img_display.pack(fill="both", expand=True)
# grid(row=0, column=1, sticky=S + N + W + E, padx=10, pady=5)

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

# FRAME
options_frame = LabelFrame(left, text="image")
options_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=10, pady=5)

# CONTROLS
dpi_label = Label(options_frame, text="DPI")
dpi_label.grid(row=3, column=0, sticky=W + E, padx=5, pady=5)

dpi_input = Entry(options_frame, textvariable=dpi_var)
dpi_input.grid(row=3, column=1, sticky=W + E, padx=5, pady=5)

size_label = Label(options_frame, text="SIZE")
size_label.grid(row=4, column=0, sticky=W + E, padx=5, pady=5)

size_label = Entry(options_frame, textvariable=size_var)
size_label.grid(row=4, column=1, sticky=W + E, padx=5, pady=5)

# ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------

# FRAME
control_frame = LabelFrame(left, text="output")
control_frame.grid(row=1, column=0, sticky=N + S + W + E, padx=10, pady=5)

# CONTROLS
plot_chk = Checkbutton(
    control_frame,
    text="Individual classification layers",
    variable=plot_var,
)
plot_chk.grid(row=0, column=0, sticky=NW)

contour_chk = Checkbutton(
    control_frame,
    text="Groud contour",
    variable=contour_var,
)
contour_chk.grid(row=1, column=0, sticky=NW)

composite_chk = Checkbutton(
    control_frame,
    text="Composite image",
    variable=composite_var,
)
composite_chk.grid(row=2, column=0, sticky=NW)

print_chk = Checkbutton(
    control_frame,
    text="Print file info to console",
    variable=print_var,
)
print_chk.grid(row=3, column=0, sticky=NW)

# ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------
# FRAME
control_frame = LabelFrame(left, text="view image")
control_frame.grid(row=3, column=0, sticky=N + S + W + E, padx=10, pady=5)

# LISTBOX
file_box = Listbox(control_frame)
file_box.grid(row=0, column=0, sticky=NW)


def change_img(event):
    img_index = file_box.curselection()[0]
    img_display.configure(image=images[img_index])
    img_display.update()


file_box.bind("<<ListboxSelect>>", change_img)

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


if __name__ == "__main__":
    # run main window
    root.mainloop()
