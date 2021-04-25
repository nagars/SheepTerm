import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial                       # Import pyserial library
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

# Generate GUI window
window = Tk()
# Define window size
window.geometry('750x500')
# Set title for window
window.title("Shawn's Serial Terminal")

# Define a frame
main_frame = Frame(window)
main_frame.grid(column = 0, row = 0, sticky = (N,W,E,S))
main_frame.columnconfigure(0, weight = 1)
main_frame.rowconfigure(0, weight = 1)

# Define Widgets #

# Define a label for com port to be placed near text box
com_port_label = Label(main_frame, text="COM PORT")
# Set its position in top left corner
com_port_label.pack()

# Define Drop down Menu for COM ports
# List all the available serial ports
com_ports_available = list(port_list.comports())
num_ports = len(com_ports_available)
com_ports_val = ""
if(num_ports > 0):
    n = 0
    while(n < num_ports):
        com_ports_val = com_ports_available[n][1:3]

#Define the drop down menu
com_ports_menu = ttk.Combobox(main_frame, value = com_ports_val)
com_ports_menu.pack()
#Store user selected value
com_port_selected = com_ports_menu.get()

# Define Set COM port button

# 

#Main loop
window.mainloop()
