import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial                       # Import pyserial library
# Import function to list serial ports.
import serial.tools.list_ports as port_list
from serial import SerialException  # Import pyserial exception handling

'''
Functions
'''
def print_to_terminal(msg):
    terminal_box.insert(END, msg)
    terminal_box.insert(END,'\n')

    #Reset position index to have messages scroll down
    terminal_box.yview = END
    return

def open_com_port():
    # Store user selected value
    com_port_selected = com_ports_menu.get()
    # Extract com port value
    com_port = com_port_selected[0:4]

    #Ensure a com port was selected
    if(com_port == ''):
        return
    
    global serial_port
    # Open selected com port with default parameters. Returned port handle is set as global variable
    try:
        serial_port = serial.Serial(port=com_port, baudrate=9600,
                                    bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE,
                                    parity=serial.PARITY_NONE)
    # Check if COM port failed to open. Print error message
    except SerialException:
        print_to_terminal(com_port + " is busy. Unable to open")
        return
  
    # Print COM port opened successfully.
    print_to_terminal(com_port + " opened successfully")

    #Disable open com port button
    open_com_button['state'] = 'disabled'
    return

'''
Definitions
'''
# Generate GUI window
window = Tk()
# Define window size
window.geometry('750x500')
# Set title for window
window.title("Shawn's Serial Terminal")

# Define a frame
main_frame = Frame(window)
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

# Define Widgets #

# Define a label for com port to be placed near text box
com_port_label = Label(main_frame, text="COM PORT")
# Set its position in top left corner
com_port_label.pack()

# Define Drop down Menu for COM ports
# List all the available serial ports
com_ports_available = list(port_list.comports())

# Define the drop down menu
com_ports_menu = ttk.Combobox(main_frame, value=com_ports_available)
com_ports_menu.pack()
com_ports_menu.current()

# Define Set COM port button
open_com_button = ttk.Button(main_frame, text="Open Port",
                             command=open_com_port)
open_com_button.pack()

# Create a scroll text box for the terminal
terminal_box = scrolledtext.ScrolledText(main_frame, width=47, height=20)
terminal_box.pack()

# Main loop
window.mainloop()
