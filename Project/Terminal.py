import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial
from serial.serialutil import STOPBITS_ONE_POINT_FIVE                       # Import pyserial library
# Import function to list serial ports.
import serial.tools.list_ports as port_list
from serial import SerialException  # Import pyserial exception handling

'''
Functions
'''
def print_to_terminal(msg):
    terminal_box.insert(END, msg)
    terminal_box.insert(END, '\n')

    # Reset position index to have messages scroll down
    terminal_box.yview = END
    return


def open_com_port():
    # Store user selected value
    com_port_selected = com_ports_menu.get()
    # Extract com port value
    com_port = com_port_selected[0:4]

    # Ensure a com port was selected
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

    # Disable open com port button
    open_com_button['state'] = 'disabled'

    # Enable send message textbox
    send_message_textbox['state'] = 'normal'

    # Enable send message button
    send_button['state'] = 'active'
    return


def send_button_pressed():

    # Read message to transmit from textbox
    transmit_msg = send_message_textbox.get()

    # Check if CRC is required
    
    # Transmit
    serial_port.write(transmit_msg)

    # Check if echo is checked


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
main_frame.columnconfigure(0, weight=4)
main_frame.rowconfigure(0, weight=4)

# Variable Definitions
echo_flag = tkinter.BooleanVar()    # Checks if echo checkbox is set/cleared
include_null_flag = tkinter.BooleanVar()
include_line_flag = tkinter.BooleanVar()

# Define Widgets #

# Define a label for com port to be placed near text box
com_port_label = Label(main_frame, text="COM PORT")
com_port_label.grid(column=0, row=0)
# Set its position in top left corner
#com_port_label.pack()

# Define Drop down Menu for COM ports
# List all the available serial ports
com_ports_available = list(port_list.comports())

# Define the drop down menu for com ports
com_ports_menu = ttk.Combobox(main_frame, value=com_ports_available, state = 'readonly')
com_ports_menu.grid(column=1, row=0)
#com_ports_menu.pack()
com_ports_menu.current()

# Define Set COM port button
open_com_button = ttk.Button(main_frame, text="Open Port",
                             command=open_com_port)
open_com_button.grid(column=2, row=0)
#open_com_button.pack()

# Create a scroll text box for the terminal
terminal_box = scrolledtext.ScrolledText(main_frame, width=47, height=20)
terminal_box.grid(column=1,row=1)
#terminal_box.pack()

# Create a text box to get the transmit message from user
send_message_textbox = Entry(main_frame, width=10, state='disabled')
send_message_textbox.grid(column=1,row=2)
#send_message_textbox.pack()

# Create a button to send data on selected port
send_button = Button(main_frame, text="Send",
                     command=send_button_pressed, state='disabled')
send_button.grid(column=2,row=2)
#send_button.pack()

#Create an echo to terminal checkbox
echo_checkbox = Checkbutton(main_frame, text="Enable Echo", variable=echo_flag)
echo_checkbox.grid(column=0,row=2)
#echo_checkbox.pack()

#Generate list of data types
data_types = ["STRING","ASCII","HEX"]

#Create a drop down menu with different datatypes to represent on terminal
data_types_menu = ttk.Combobox(main_frame, textvariable=data_types[0], values=data_types, state = 'readonly')
data_types_menu.grid(column=0,row=1)
#data_types_menu.pack()
data_types_menu.current()

#Create an include null character checkbox
include_null_checkbox = Checkbutton(main_frame, text="Include Null Character", variable=include_null_flag)
include_null_checkbox.grid(column=0,row=3)

#Create an include next line character checkbox
include_line_checkbox = Checkbutton(main_frame, text="Include Line Character", variable=include_line_flag)
include_line_checkbox.grid(column=0,row=4)

# Main loop
window.mainloop()
