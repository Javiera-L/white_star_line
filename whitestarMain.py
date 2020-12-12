#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 18:25:49 2020

@author: Javi
"""
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
import sys
import numpy as np
import icebergidentifier
import ice
from tkinter import Tk, Menu, Canvas
from PIL import Image, ImageTk

def open_file(file):
    """
    Open files and return an array of the data it reads.

    Parameters
    ----------
    file : .txt or .csv file
        File must contain equal amount of rows as columns.

    Returns
    -------
    Numpy array of the data it has read from the file.

    """
    list_data = []
    # note that "in.txt" needs to be a square matrix
    # (same number of rows as cols)
    f = open(file, newline='')
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:  # A list of rows
        rowlist = []
        for value in row:  # A list of value
            rowlist.append(value)
        list_data.append(rowlist)
    f.close()  # Don't close until you are done with the reader;
    # the data is read on request.
    print(f"Loading {file}...")
    return(np.array(list_data))

def save_data(array):
    """
    Save iceberg towability map to a .txt file.

    Parameters
    ----------
    array : np.array
        Iceberg towability (as a coloured map).

    Returns
    -------
    None.

    """
    outfile = open('colour_map.txt', 'w')
    for line in array:
        for value in line:
            outfile.write(str(value))
            outfile.write(', ')
    outfile.close()


def create_tow_map():
    """
    Modify the empty colour_map array by calling the tow_map function of
    each iceberg.

    Returns
    -------
    None.

    """
    for i in range(count):
        icebergs[i].tow_map()
        # updates colour map so they all appear in same figure

def save_loc_array():
    """
    Save the array containing the location of each of the icebergs. This
    array identifies each iceberg by its unique number.

    Returns
    -------
    None.

    """
    np.savetxt('loc_array.txt', loc_array, fmt='%d')

def save_data_to_file():
    """
    Save object data to a file.
    Example line:
    "Mass: 52661700.0, Volume: 5851.3, Number: 2, is_towable = False "

    Returns
    -------
    None.

    """
    with open('iceberg_data.txt', 'w') as f:
        for berg in icebergs:
            f.write(repr(berg))

def print_iceberg_data():
    """
    Print iceberg object data on the interpreter.

    Returns
    -------
    None.

    """
    print(icebergs)

def save_image(filename):
    """
    Save image of icebergs and whether they are towable or not (green or red)
    to a file called "towability_map.jpg".

    Parameters
    ----------
    filename : PIL.Image.Image
        Image of towability of the icebergs.

    Returns
    -------
    None.

    """
    filename = filename.save("towability_map.jpg")

def quitProgram():
    """
    Quit Tkinter loop.

    Returns
    -------
    None.

    """
    gui.quit()
    gui.destroy()


if __name__ == "__main__":

    if len(sys.argv) == 3:
        radar = open_file(sys.argv[1])    
        lidar = open_file(sys.argv[2]) 
    else:
        sys.exit('Need to specify radar and lidar files as command line \
                  arguments. Example (in terminal): python whitestarMain.py radar2.txt lidar2.txt')
        
    #radar = open_file('radar2.txt')
    #lidar = open_file('lidar2.txt')

    # print(np.all(lidar==0))
    # plt.imshow(radar)

    identifier = icebergidentifier.IcebergIdentifier(radar, lidar)

    count, volumes, masses, loc_array = identifier.collect_data()
    # print(np.nonzero(loc_array))
    # plt.imshow(loc_array)
    row = len(loc_array)
    col = len(loc_array[0])
    # empty map full of zeroes, same size as loc_array with each entry having
    # 3 more entries for each RGB value
    colour_map = np.zeros((row, col, 3))
    icebergs = []

    # this for loop assigns data to iceberg object to store it
    for i in range(count):
        # print(i)
        icebergs.append(ice.Iceberg(volumes[i], masses[i], i + 1,
                                    loc_array, colour_map))
        # need num to be i +1 to distinguish from 0, the background

    # fig = plt.figure(frameon=False)

    # create our green and red map (updates our empty colourmap)
    create_tow_map()

    # print(type(colour_map))
    colour_map = np.asarray(colour_map, dtype=np.float32) / 255
    image = Image.fromarray((colour_map * 255).astype(np.uint8), 'RGB')
    # print(type(image))

    # Main window
    gui = Tk()
    canvas = Canvas(gui, width=300, height=300)
    canvas.pack()
    # Inside the main gui window
    # Creating an object containing an image
    # A canvas with borders that adapt to the image within it
    img = ImageTk.PhotoImage(master=gui, image=image)
    canvas.image = img
    canvas.create_image(0, 0, anchor='nw', image=img)
    gui.title('Towability Map')
    # Menu bar
    menubar = Menu(gui)
    # Adding a cascade to the menu bar:
    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Options", menu=filemenu)
    # filemenu.add_command(label="Open iceberg map", command=loadImage)
    filemenu.add_command(label="Save image", command=save_image(image))
    # filemenu.add_command(label="Delete image", command=deleteImage)
    filemenu.add_command(label="Print iceberg data",
                         command=print_iceberg_data)
    filemenu.add_command(label="Save iceberg data to file",
                         command=save_data_to_file)
    filemenu.add_command(label="Save location array to file",
                         command=save_loc_array)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=quitProgram)
    menubar.add_separator()
    menubar.add_cascade(label="?")
    # Display the menu bar
    gui.config(menu=menubar)
    gui.mainloop()
