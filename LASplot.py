from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import plot
import os


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
            for the_file in os.listdir(destination_var.get()):
                if the_file.endswith("png"):
                    img_path = destination_var.get() + "/" + the_file
                    print("img_path: ", img_path)
                    images.append(
                        ImageTk.PhotoImage(Image.open(img_path).resize((1000, 1000)))
                    )
            img_display.configure(image=images[0])
            img_display.update()
        if contour_var.get() == 1:
            print("do contour stuff....")
        if composite_var.get() == 1:
            print("do composite stuff....")

    else:
        print("please select correct input values")


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
options_frame = LabelFrame(left, text="image options")
options_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=10, pady=5)

# CONTROLS
dpi_label = Label(options_frame, text="DPI")
dpi_label.grid(row=3, column=0, sticky=W + E, padx=5, pady=5)

dpi_input = Entry(options_frame)
dpi_input.grid(row=3, column=1, sticky=W + E, padx=5, pady=5)

size_label = Label(options_frame, text="SIZE")
size_label.grid(row=4, column=0, sticky=W + E, padx=5, pady=5)

size_label = Entry(options_frame)
size_label.grid(row=4, column=1, sticky=W + E, padx=5, pady=5)

# ---------------------------- CHOOSE OUTPUT SETTINGS ----------------------------

# FRAME
control_frame = LabelFrame(left, text="Images to generate")
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
