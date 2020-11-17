from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt
import time
import threading

#-----initialise window-----
root = Tk()

#-----GUI text variables-----
source_var = StringVar()
source_var.set("select source...")
destination_var = StringVar()
destination_var.set("select destination...")


def main():
        
    #window settings
    root.title("LASplot")
    root.resizable(0,0)
    root.configure(background="black")
    #source input config
    Button(root, text="INPUT FILE/S", command= choose_source, background = "black", foreground="white").grid(row = 0, column = 0, sticky = W)
    Label(root, textvariable=source_var, background = "black", foreground="white").grid(row=0,column=0,sticky=E)
    #destination input config
    Button(root, text="DESTINATION", command= choose_dest, background = "black", foreground="white").grid(row = 1, column = 0, sticky = W)
    Label(root, textvariable=destination_var, background = "black", foreground="white").grid(row=1,column=0,sticky=E)
    #configure background image
    icon = PhotoImage(file="icon.png")
    Label(root, image = icon, background = "black").grid(row = 2, column = 0, sticky = N)
    #.world file generation settings (1/0)
    Checkbutton(root, text="Generate '.world' context files",  background = "black", foreground="white").grid(row = 2, column = 0, sticky = NW)
    #GO button config
    Button(root, text="BEGIN", command= (threading.Thread(target=plot).start), background = "deepskyblue", foreground="black", padx=10, pady=10).grid(row = 2, column = 0, sticky = SE)
    
    #run main window
    root.mainloop()

def choose_source():
    source_var.set(filedialog.askopenfilename(title = "Select one or more .LAS files" ,filetypes = (("las Files", "*.las"),)))

def choose_dest():    
    destination_var.set(filedialog.askdirectory())

def print_header(file_input): #Print basic header information to the terminal
    point_records = file_input.points
    fmat = file_input.point_format.fmt

    print('--------------------------HEADER INFORMATION-------------------------')
    print('LAS specification = ' + file_input.header.version)
    print('point format = ' + str(fmat))
    print('total point count = ' + str(file_input.header.count))
    print('sample point array = ' + str(point_records[0]))
    print("---------------------------------------------------------------------")

def classification_index(file_input):
    las_format = file_input.point_format.fmt
    if las_format == '1':
        return 5
    elif las_format == '6':
        return 6
    else:
        messagebox.showerror(title="POINT FORMAT ERROR", message="ERROR: unrecognised point format.")

def save_figure(x_,y_,filename_,color_):
    # plot ground points
    plt.rcParams["figure.figsize"] = [50, 50]
    plt.rcParams['figure.facecolor'] = 'black'
    plt.plot(x_,y_, color= color_, linestyle='none', marker='.')
    plt.margins(0,0)
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.gca().set_axis_off()
    fig = plt.gcf()
    fig.savefig(destination_var.get() + filename_, dpi=50, bbox_inches = 'tight', pad_inches = 0, facecolor=fig.get_facecolor())
    plt.clf()

def plot(): 
    input_LAS = File(source_var.get(), mode='r')
    c_index = classification_index(input_LAS)
    print_header(input_LAS)
    point_records = np.array(input_LAS.points)
    
    #progress bar config
    progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=630, mode="determinate", maximum=input_LAS.header.count / 10000)
    progress_bar.grid(row = 2, column = 0, sticky = SW)
    root.update()

    #-----Point Classifications-----
    #unclassified
    unclassified_x = []
    unclassified_y = []
    #ground
    ground_x = []
    ground_y = []
    #low veg
    lowVeg_x = []
    lowVeg_y = []
    #med veg
    medVeg_x = []
    medVeg_y = []
    #high veg
    highVeg_x = []
    highVeg_y = []
    #buildings
    buildings_x = []
    buildings_y = []
    #water
    water_x = []
    water_y = [] 

    #loop through point records and seperate by classification
    for count, record in enumerate(point_records):
        if record[0][c_index] == 2:
            ground_x.append(record[0][0])
            ground_y.append(record[0][1])
        elif record[0][c_index] == 1:
            unclassified_x.append(record[0][0])
            unclassified_y.append(record[0][1])
        elif record[0][c_index] == 3:
            lowVeg_x.append(record[0][0])
            lowVeg_y.append(record[0][1])
        elif record[0][c_index] == 4:
            medVeg_x.append(record[0][0])
            medVeg_y.append(record[0][1])          
        elif record[0][c_index] == 5:
            highVeg_x.append(record[0][0])
            highVeg_y.append(record[0][1])       
        elif record[0][c_index] == 6:
            buildings_x.append(record[0][0])
            buildings_y.append(record[0][1])         
        elif record[0][c_index] == 9:
            water_x.append(record[0][0])
            water_y.append(record[0][1])            
        
        if count % 10000 == 0:
            progress_bar['value'] += 1
            root.update_idletasks() 

    save_figure(unclassified_x,unclassified_y, '/unclassified.png', 'm')
    save_figure(ground_x,ground_y, '/ground.png', 'SaddleBrown')
    save_figure(lowVeg_x,lowVeg_y, '/lowVeg.png', 'LimeGreen')
    save_figure(medVeg_x,medVeg_y, '/mediumVeg.png', 'Green')
    save_figure(highVeg_x,highVeg_y, '/highVeg.png', 'DarkGreen')
    save_figure(buildings_x,buildings_y, '/buildings.png', 'White')
    save_figure(water_x,water_y, '/water.png', 'DodgerBlue')

if __name__ == "__main__":
    main()