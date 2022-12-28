import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

import sercomm      # custom library built to handle communication 
import settings_ui  # custom library built to manage the settings window 

'''
###############Functions#############
'''

'''
Function Description: Prints string to globally defined scroll terminal object

Parameters: msg - string to print to terminal 

Return: void
'''
def print_to_terminal(msg):
    terminal_box.insert(END, msg)
    terminal_box.insert(END, '\n')

    # Reset position index to have messages scroll down
    terminal_box.yview = END
    return


'''
Function Description: Generates a new window designed to set various
settings for communication and logging

Parameters: void 

Return: void
'''
def open_com_port_param_window():

    # Create new window
    settings_window = Tk()
    settings_window.geometry("500x500")
    settings_window.title("Shawn's COM port settings")

    # Create new frame

    # Define UI objects


    return

'''
Function Description: Closes come port and program.

Parameters: void

Return: void
'''
def close_window():
    
    # Close the com port
    sercomm.close_serial_com()

    # Terminate window
    window.destroy()


'''
Function Description: Clears scroll terminal screen

Parameters: void 

Return: void
'''
def clear_button_pressed():

    # Enable editing of text box
    terminal_box.config(state="normal")
    # Delete all text in display
    terminal_box.delete("1.0",END)
    # Disable editing of text box
    terminal_box.config(state="disabled")


'''
Function Description: Transmits data in transmit text box
to com port

Parameters: void 

Return: void
'''
def send_button_pressed():

    # Read message to transmit from textbox
    transmit_msg = send_message_textbox.get()
    
    # Transmit
    sercomm.serial_port.write(transmit_msg)


'''
Function Description: Opens selected com port
from drop down menu

Parameters: void 

Return: com port on success
'''
def open_com_port():

    # Extract com port value
    com_port = com_ports_menu.get()[0:4]
    
    # Open port
    status = sercomm.open_serial_com(com_port)

    #Check return value
    if status < 0:
        print_to_terminal(com_port + " is busy. Unable to open")
        return -1

    # Print COM port opened successfully.
    print_to_terminal(com_port + " opened successfully")

    # Disable open com port button
    open_com_button['state'] = 'disabled'

    # Enable send message textbox
    send_message_textbox['state'] = 'normal'

    # Enable send message button
    send_button['state'] = 'active'

    return com_port


'''Functions: Frame Definitions'''
'''
Function Description: Define a frame for the UI objects

Parameters: container - Main window object
position_y - column index for frame position
position_x - row index for frame position

Return: frame object
'''
def define_frame(container, position_y, position_x):

    frame = Frame(container)
    frame.grid(column=position_y, row=position_x)

    return frame

'''Functions: Widget Definitions'''
'''
Function Description: Define a drop down menu UI object

Parameters: container - Main window object
content_list - list of option in the drop down menu
default_state - default option selected by drop down menu
position_y - columnm index for frame position
position_x - row index for frame position

Return: drop down object
'''
def define_drop_down(container, content_list, default_state, position_y, position_x):

    menu = ttk.Combobox(container, value=content_list, state = default_state)
    menu.grid(column=position_y, row=position_x, padx=2, pady=2)

    return menu


'''
Function Description: Define a button UI object that can be used to call a function
when selected

Parameters: container - Main window object
text - label for the button
default_state - active / inactive
function_call - callback function triggered when button is pressed
position_y - columnm index for frame position
position_x - row index for frame position

Return: button object
'''
def define_button(container, text, default_state, function_call, position_y, position_x):
    
    button = ttk.Button(container, text=text,
                        command=function_call, state=default_state)
    button.grid(column=position_y, row=position_x, padx=2, pady=2)

    return button


'''
Function Description: Define a label UI object

Parameters: container - Main window object
text - label text
position_y - columnm index for frame position
position_x - row index for frame position

Return: button object
'''
def define_label(container, text, position_y, position_x):

    label = Label(container, text=text)
    label.grid(column=0, row=0, padx=2, pady=2)

    return label


'''
Function Description: Define a checkbox UI object

Parameters: container - Main window object
test - label text
default_state - active / inactive
status_variable - checked / unchecked

position_y - columnm index for frame position
position_x - row index for frame position

Return: button object
'''
def define_checkbox(container, text, default_state, status_variable, position_y, position_x):

    checkbox = Checkbutton(container, text=text, variable=status_variable, state=default_state)
    checkbox.grid(column=position_y, row=position_x, padx=2, pady=2)

    return checkbox


'''
Function Description: Define a scroll terminal

Parameters: container - Main window object
width - width of the textbox
height - height of the textbox
position_y - columnm index for frame position
position_x - row index for frame position

Return: textbox object
'''
def define_scroll_textbox(container, width, height, position_y, position_x):

    scrollbox = scrolledtext.ScrolledText(container, width=width, height=height, state="disabled")
    scrollbox.grid(column=position_y, row=position_x, padx=2, pady=2)
    scrollbox.configure(font=("Times New Roman", 10))

    return scrollbox


'''
Function Description: Define textbox to entry data into

Parameters: container - Main window object
width - width of the textbox
default_state - active / inactive
position_y - columnm index for frame position
position_x - row index for frame position

Return: entrybox object
'''
def define_entry_textbox(container, width, default_state, position_y, position_x):
    entrybox = Entry(container, width=width, state=default_state)
    entrybox.grid(column=position_y, row=position_x, padx=2, pady=2)
    entrybox.configure(font=("Times New Roman", 10))

    return entrybox


'''
Frame Definitions
'''
# Generate GUI window
window = Tk()
# Define window size
window.geometry('1000x500')
# Set title for window
window.title("Shawn's Serial Terminal")
# Create Display Configure Frame for checkbox and drop down options
config_frame = define_frame(window, 0, 1)
config_frame.grid(sticky=NW)
# Create COM Frame for COM port settings
com_frame = define_frame(window,0,0)
com_frame.grid(sticky=NW)
# Create a Terminal frame to display actual data
display_frame = define_frame(window,1,1)
display_frame.grid(sticky=NSEW)
# Create a boundary frame for the bottom
south_boundary_frame = define_frame(window,0,2)
south_boundary_frame.grid(sticky=NSEW)
#Ensure display frame expands with window
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)


''' 
Variable Definitions
'''
# Tracks if user enabled timestamping of data on terminal
timestamp_flag = tkinter.BooleanVar() 
# Tracks if user enabled NL to be appended to data sent
include_new_line_flag = tkinter.BooleanVar()
# Tracks if user enabled CR to be appended to data sent
include_carriage_return_flag = tkinter.BooleanVar()
# Tracks if user requests logging of data to file
logging_flag = tkinter.BooleanVar()


'''
Define COMM frame UI objects
'''
# Define a label for com port to be placed near text box
com_port_label = define_label(com_frame, "COM PORT", 0, 0)
# List all the available serial ports
com_ports_available = list(port_list.comports())
# Define the drop down menu for com ports
com_ports_menu = define_drop_down(com_frame, com_ports_available, 'readonly', 1, 0)
# Define Set COM port button
open_com_button = define_button(com_frame, "Open Port", 'normal',
                                open_com_port, 2, 0),
# Define a settings button for sercomm settings
settings_button = define_button(com_frame, "Settings", 'normal',
                                open_com_port_param_window, 3,0)


'''
Define config frame UI objects
'''
# Define a label for data type drop down
display_type_label = define_label(config_frame, "Display Type", 0, 0)
display_type_label.grid(sticky=W)
#Create a show timestamp checkbox
timestamp_checkbox = define_checkbox(config_frame, "Show Timestamp", 
                        "normal", timestamp_flag, 0, 2)
timestamp_checkbox.grid(sticky=W)
# Define a enable logging button
enable_logging_checkbox = define_checkbox(config_frame, "Enable Logging",
                        "normal", logging_flag, 0, 5)
enable_logging_checkbox.grid(sticky=W)
#Generate list of data types
data_types = ["STRING","ASCII","HEX"]
#Create a drop down menu with different datatypes to represent on terminal
data_types_menu = define_drop_down(config_frame, data_types, 'readonly',1,0)
data_types_menu.grid(sticky=W)
#Set default value of drop down menu
data_types_menu.current(0)      
#Create an include next line character checkbox
include_new_line_checkbox = define_checkbox(config_frame, "Include New Line Character", "normal",
                                        include_new_line_flag, 0, 3)
include_new_line_checkbox.grid(sticky=W)
#Create an include next line character checkbox
include_carriage_return_checkbox = define_checkbox(config_frame, "Include Carriage Return Character", "normal",
                                        include_carriage_return_flag, 0, 4)
include_carriage_return_checkbox.grid(sticky=W)


'''
Define Terminal frame UI objects
'''
# Create a scroll text box for the terminal
terminal_box = define_scroll_textbox(display_frame, 50, 20, 0, 0)
terminal_box.grid(sticky=NSEW)
# Create a text box to get the transmit message from user
send_message_textbox = define_entry_textbox(display_frame, 47, 'disabled', 0, 1)
send_message_textbox.grid(sticky=NSEW)
# Create a button to send data on selected port
send_button = define_button(display_frame, "Send", 'disabled',
                     send_button_pressed, 1, 1)
send_button.grid(sticky=NSEW, padx=5, pady=5)
# Create a clear terminal display button
clear_button = define_button(display_frame, "Clear", 'normal',
                     clear_button_pressed, 1, 0)
clear_button.grid(sticky=SE, padx=5, pady=5)
# Ensure the terminal box expands with the frame
display_frame.columnconfigure(0, weight=1)
display_frame.rowconfigure(0, weight=1)


'''
Define Empty frame UI objects
'''
# Define an empty label to act as a spacer for the bottom 
empty_label = define_label(south_boundary_frame, "", 0, 0)
empty_label.grid(sticky=NSEW)


'''
Main loop
'''
# Install window close routine
window.protocol("WM_DELETE_WINDOW",close_window)

window.mainloop()

