import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
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

'''Functions: Frame Definitions'''
def define_frame(container, position_y, position_x):

    frame = Frame(container)
    frame.grid(column=position_y, row=position_x, sticky=(N, W, E, S))

    return frame

'''Functions: Widget Definitions'''
def define_drop_down(container, content_list, default_state, position_y, position_x):

    menu = ttk.Combobox(container, value=content_list, state = default_state)
    menu.grid(column=position_y, row=position_x)
    menu.current()

    return menu

def define_button(container, text, default_state, function_call, position_y, position_x):
    
    button = ttk.Button(container, text=text,
                        command=function_call, state=default_state)
    button.grid(column=position_y, row=position_x)

    return

def define_label(container, text, position_y, position_x):

    label = Label(container, text=text)
    label.grid(column=0,row=0)

    return label

def define_checkbox(container, text, default_state, status_variable, position_y, posiion_x):

    checkbox = Checkbutton(container, text=text, variable=status_variable, state=default_state)
    checkbox.grid(column=position_y,row=posiion_x)

    return checkbox

def define_scroll_textbox(container, width, height, position_y, position_x):

    scrollbox = scrolledtext.ScrolledText(container, width=width, height=height)
    scrollbox.grid(column=position_y, row=position_x)

    return scrollbox

def define_entry_textbox(container, width, default_state, position_y, position_x):
    entrybox = Entry(container, width=width, state=default_state)
    entrybox.grid(column=position_y, row=position_x)

    return entrybox

'''
Definitions
'''
# Generate GUI window
window = Tk()
# Define window size
window.geometry('750x500')
# Set title for window
window.title("Shawn's Serial Terminal")
#Configure its layout
window.columnconfigure(0,weight=0)
window.rowconfigure(0,weight=0)

# Variable Definitions
echo_flag = tkinter.BooleanVar()    # Checks if echo checkbox is set/cleared
timestamp_flag = tkinter.BooleanVar() 
include_null_flag = tkinter.BooleanVar()
include_line_flag = tkinter.BooleanVar()

# Create COM Frame #
com_frame = define_frame(window,0,0)
# Define a label for com port to be placed near text box
com_port_label = define_label(com_frame, "COM PORT", 0, 0)
# List all the available serial ports
com_ports_available = list(port_list.comports())
# Define the drop down menu for com ports
com_ports_menu = define_drop_down(com_frame, com_ports_available, 'readonly', 1, 0)
# Define Set COM port button
open_com_button = define_button(com_frame, "Open Port", 'normal',
                                open_com_port,2,0),


# Create Display Configure Frame #
config_frame = define_frame(window, 0, 1)
# Define a label for data type drop down
display_type_label = define_label(config_frame, "Display Type", 0, 0)
display_type_label.grid(sticky=W)
#Create an echo to terminal checkbox
echo_checkbox = define_checkbox(config_frame, "Enable Echo", "normal", echo_flag, 0, 1)
echo_checkbox.grid(sticky=W)
#Create a show timestamp checkbox
timestamp_checkbox = define_checkbox(config_frame, "Show Timestamp", 
                        "normal", timestamp_flag, 0, 2)
timestamp_checkbox.grid(sticky=W)
#Generate list of data types
data_types = ["STRING","ASCII","HEX"]
#Create a drop down menu with different datatypes to represent on terminal
data_types_menu = define_drop_down(config_frame, data_types, 'readonly',1,0)
#Create an include null character checkbox
include_null_checkbox = define_checkbox(config_frame, "Include Null Character", "normal", 
                                        include_null_flag, 0, 3)
#Create an include next line character checkbox
include_line_checkbox = define_checkbox(config_frame, "Include Line Character", "normal",
                                        include_line_flag, 0, 4)



# Create a text box to get the transmit message from user
send_message_textbox = define_entry_textbox(window, 10, 'disabled', 1, 2)

# Create a button to send data on selected port
send_button = define_button(window, "Send", 'disabled',
                     send_button_pressed, 2, 2)

# Create a scroll text box for the terminal
terminal_box = define_scroll_textbox(window, 47, 20, 1, 1)

# Main loop
window.mainloop()
