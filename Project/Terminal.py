'''Generic Modules'''
import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException          # Import pyserial exception handling

from datetime import datetime   #Import system date library

import threading                #Imports python threading module

'''Custom Modules'''
import sercomm      # custom library built to handle communication
import settings_ui  # custom library built to manage the settings window 
import ui_objects   # custom library built to handle common UI objects

'''
Function Description: Function to be called as separate thread. Receives data
from serial port, logs if required, converts to selected display format
and prints to terminal. Checks if a read timeout has occurred and 
appends new lines + timestamp if required.

Parameters: void

Return: True - Successful / False - Failure
'''
def receive_thread():

    # Flag to track if a read timeout has occurred
    serial_timout_occurred = False

    # Maintain the thread until the terminate event flag is set
    # flag is set when the user attempts to close the window and
    # terminate the program or to change settings of the serial port
    while not g_terminate_event.is_set():
        # Get data from serial port
        # Convert to string from bytes
        msg = (sercomm.read_serial_com()).decode("UTF-8")
        # If length of msg is 0, a timeout has occurred with no data received
        if len(msg) == 0:
            serial_timout_occurred = True
            continue

        # Change data format based on drop down menu selection
        match data_types_dd.get():
            case "STRING":
                print_msg = msg    
            
            case "ASCII":
                for i in msg:
                    print_msg = str(ord(i)) + ' '
           
            case "HEX":
                for i in msg:
                    print_msg = str(hex(ord(i))[2:]) + ' '
            
            case _:
                return False

        # Log data if required
        curr_sercom_settings = settings_ui.get_sercomm_settings()
        if curr_sercom_settings.logfile != None:
            # Write to .csv file

            # Append new line character
            pass
        
        # Check if a timeout has occurred, print to new line
        if serial_timout_occurred == True:

            #Check if timestamp is required. Append to message
            if (timestamp_flag.get() == True):
                print_msg = datetime.now().strftime('%H:%M:%S.%f')[:-3] + " :\t\t" + print_msg

            # Reset timeout flag
            serial_timout_occurred = False

            print_to_terminal('\n' + print_msg)
            continue

        # Print to terminal
        print_to_terminal(print_msg)

    return True

'''
Function Description: Prints string to globally defined scroll terminal object

Parameters: msg - string to print to terminal 

Return: void
'''
def print_to_terminal(msg):

    # Enable editing of text box
    terminal_box.config(state="normal")

    terminal_box.insert(END, msg)
    
    # Reset position index to have messages scroll down
    terminal_box.yview = END

    # Disable editing of text box
    terminal_box.config(state="disabled")
    return


'''
Function Description: Closes come port, file pointer
to log file (If open) and program.
Ensures recieve_thread terminate gracefully

Parameters: void

Return: void
'''
def close_window():
    
    # Check if the receive thread was started
    try:
        g_receive_thread

    # If not, terminate program
    except NameError:
        pass

    # Terminate receive thread, then terminate program
    else:
        # Set terminate flag for receive thread
        g_terminate_event.set()

        # Cancel any pending read
        sercomm.abort_serial_read()

        # wait till receive thread is terminated
        g_receive_thread.join()

    # Close the com port
    sercomm.close_serial_com()

    # Close file pointer for logger

    # Terminate window
    window.destroy()
    return


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
    return


'''
Function Description: Transmits data in transmit text box
to com port. Clears the send text box

Parameters: void 

Return: void
'''
def send_button_pressed():

    # Read message to transmit from textbox
    transmit_msg = send_message_textbox.get()

    # If Carriage return check box is selected, append \r
    if include_carriage_return_flag.get() == True:
        transmit_msg += '\r'

    # If Next line check box is selected, append \n
    if include_new_line_flag.get() == True:
        transmit_msg += '\n'
    
    # Transmit
    sercomm.write_serial_com(transmit_msg)

    # Delete all text in display
    send_message_textbox.delete("0",END)

    return


'''
Function Description: Opens selected com port
from drop down menu. Creates receive thread if
com port opened successfully. Modifies UI to
represent opened com port.

Parameters: void 

Return: com port name on Success / False on Failure
'''
def open_com_port():

    # Extract com port value
    com_port = com_ports_menu.get()[0:4]
    '''TESTING ONLY. REMOVE FOR PRODUCTION'''
    com_port = 'COM8'
    '''****************'''
    #Ensure a com port was selected
    if com_port == '':
        print_to_terminal("No COM port selected!\n")
        return False
    
    # Get a copy of com port settings
    sercomm_settings = settings_ui.get_sercomm_settings()

    # Open port
    status = sercomm.open_serial_com(com_port, sercomm_settings.baud, 
                                        sercomm_settings.bytesize, sercomm_settings.readtimeout,
                                        sercomm_settings.stopbits, sercomm_settings.paritybits)

    #Check return value
    if status == False:
        print_to_terminal(com_port + " is busy. Unable to open\n")
        return False

    # Print COM port opened successfully.
    print_to_terminal(com_port + " opened successfully\n")

    # Disable open com port button
    open_com_button['state'] = 'disabled'

    # Enable send message textbox
    send_message_textbox['state'] = 'normal'

    # Enable send message button
    send_button['state'] = 'active'

    # Disable settings button
    settings_button['state'] = 'normal'

    # Disable drop down menu for com ports
    com_ports_menu['state'] = 'disabled'

    # Set current com port variable in com settings struct
    settings_ui.set_com_port(com_port)

    # Create an event variable to sync termination of the main loop and receive thread
    global g_terminate_event
    g_terminate_event = threading.Event()

    # Create receive thread to print to terminal
    global g_receive_thread
    g_receive_thread = threading.Thread(target=receive_thread)
    g_receive_thread.start()

    return com_port

'''
Function Description: Terminates the receive thread and calls
function to open the serial settings window. Waits for settings 
window to close, checks if serial port is open and creates a new
receive thread. If not open, disables operations until same or
another port is opened by the user.

Parameters: void

Return: True on Success / False on Failure
'''
def open_settings_window():

    # Terminate receive thread 
    # to prevent a read operation while
    # the user closes and reopens the 
    # serial port with new settings

    # Set terminate flag for receive thread
    global g_terminate_event
    g_terminate_event.set()

    # Abort any read operation
    sercomm.abort_serial_read()

    # Wait till receive thread is terminated
    global g_receive_thread
    g_receive_thread.join()

    # Call open settings window function
    settings_window = settings_ui.define_sercomm_settings_window()
    
    # Wait for the settings window to close
    window.wait_window(settings_window)

    # Ensure serial port is open successfully
    if sercomm.check_serial_port_status() == True:

        # Once settings are confirmed, 
        # Clear terminate_event flag and start receive thread again
        g_terminate_event.clear()

        g_receive_thread = threading.Thread(target=receive_thread)
        g_receive_thread.start()

    else:
        print_to_terminal("Port is busy. Unable to open\n")

        # Return UI to original state so user can retry
        # opening the port or select a new port

        # Enable open com port button
        open_com_button['state'] = 'normal'

        # Disable send message textbox
        send_message_textbox['state'] = 'disabled'

        # Disable send message button
        send_button['state'] = 'disabled'

        # Disable settings button
        settings_button['state'] = 'disabled'

        return False

    return True
    


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
config_frame = ui_objects.define_frame(window, 0, 1)
config_frame.grid(sticky=NW)
# Create COM Frame for COM port settings
com_frame = ui_objects.define_frame(window,0,0)
com_frame.grid(sticky=NW)
# Create a Terminal frame to display actual data
display_frame = ui_objects.define_frame(window,1,1)
display_frame.grid(sticky=NSEW)
# Create a boundary frame for the bottom
south_boundary_frame = ui_objects.define_frame(window,0,2)
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


'''
Define COMM frame UI objects
'''
# Define a label for com port to be placed near text box
com_port_label = ui_objects.define_label(com_frame, "COM PORT", 0, 0)
# List all the available serial ports
com_ports_available = list(port_list.comports())
# Remove unusable com port options
# (NULL appended com port names seem to appear. Possibly due to using
#  virtual com ports?)
for item in com_ports_available:
    print(item)
    if str(item)[0:5] == "NULL_":
        com_ports_available.remove(item)

# Define the drop down menu for com ports
com_ports_menu = ui_objects.define_drop_down(com_frame, com_ports_available, 'readonly', 1, 0)
# Define Set COM port button
open_com_button = ui_objects.define_button(com_frame, "Open Port", 'normal',
                                open_com_port, 2, 0)
# Define a settings button for sercomm settings
settings_button = ui_objects.define_button(com_frame, "Settings", 'disabled',
                                open_settings_window, 3, 0)


'''
Define config frame UI objects
'''
# Define a label for data type drop down
display_type_label = ui_objects.define_label(config_frame, "Display Type", 0, 0)
display_type_label.grid(sticky=W)
#Create a show timestamp checkbox
timestamp_checkbox = ui_objects.define_checkbox(config_frame, "Show Timestamp", 
                        "normal", timestamp_flag, None, 0, 2)
timestamp_checkbox.grid(sticky=W)
#Generate list of data types
data_types = ["STRING","ASCII","HEX"]
#Create a drop down menu with different datatypes to represent on terminal
data_types_dd = ui_objects.define_drop_down(config_frame, data_types, 'readonly',1,0)
data_types_dd.grid(sticky=W)
#Set default value of drop down menu
data_types_dd.current(0)      
#Create an include next line character checkbox
include_new_line_checkbox = ui_objects.define_checkbox(config_frame, "Include New Line Character", "normal",
                                        include_new_line_flag, None, 0, 3)
include_new_line_checkbox.grid(sticky=W)
#Create an include next line character checkbox
include_carriage_return_checkbox = ui_objects.define_checkbox(config_frame, "Include Carriage Return Character", "normal",
                                        include_carriage_return_flag, None, 0, 4)
include_carriage_return_checkbox.grid(sticky=W)


'''
Define Terminal frame UI objects
'''
# Create a scroll text box for the terminal
terminal_box = ui_objects.define_scroll_textbox(display_frame, 50, 20, 0, 0)
terminal_box.grid(sticky=NSEW)
# Create a text box to get the transmit message from user
send_message_textbox = ui_objects.define_entry_textbox(display_frame, 47, 'disabled', 0, 1)
send_message_textbox.grid(sticky=NSEW)
# Create a button to send data on selected port
send_button = ui_objects.define_button(display_frame, "Send", 'disabled',
                     send_button_pressed, 1, 1)
send_button.grid(sticky=NSEW, padx=5, pady=5)
# Bind Enter key to send button
window.bind('<Return>', send_button_pressed)
# Create a clear terminal display button
clear_button = ui_objects.define_button(display_frame, "Clear", 'normal',
                     clear_button_pressed, 1, 0)
clear_button.grid(sticky=SE, padx=5, pady=5)
# Ensure the terminal box expands with the frame
display_frame.columnconfigure(0, weight=1)
display_frame.rowconfigure(0, weight=1)


'''
Define Empty frame UI objects
'''
# Define an empty label to act as a spacer for the bottom 
empty_label = ui_objects.define_label(south_boundary_frame, "", 0, 0)
empty_label.grid(sticky=NSEW)


'''
Main loop
'''
# Install window close routine
window.protocol("WM_DELETE_WINDOW",close_window)
window.mainloop()

