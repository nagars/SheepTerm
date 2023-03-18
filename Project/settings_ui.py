import tkinter # Import tkinter library used to generate GUI
from tkinter import * # Import tkinter modules used to generate GUI
from tkinter.filedialog import asksaveasfile # Import tkinter file save module

import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

import copy     # Import copy module for shallow copy of objects

from datetime import datetime   #Import system date library
import os #Import directory manipulation library
from tkinter import filedialog 

import ui_objects   # custom library built to handle common UI objects
import sercomm  # custom library for sercomm api

'''
Structure and Enumerations
'''

'''
Class used as struct to store comm settings
'''
class com_struct:
    def __init__(self):
        self.port = None
        self.baud = 9600
        self.bytesize = 8
        self.paritybits = serial.PARITY_NONE
        self.stopbits = 1
        self.readtimeout = 1
        self.logfile = None   # Used to store a file object
    
    # To perform a comparison of 2 objects of this class, I
    # chose to over ride the comparison operator
    def __eq__(objA, objB): 
        if not isinstance(objB, com_struct):
            # Don't attempt to compare against unrelated types
            raise Exception ("Objects to be compared are not the same class")

        return objA.port == objB.port \
            and objA.baud == objB.baud \
            and objA.bytesize == objB.bytesize \
            and objA.paritybits == objB.paritybits \
            and objA.stopbits == objB.stopbits \
            and objA.readtimeout == objB.readtimeout \
            and objA.logfile == objB.logfile

g_com_settings = com_struct() # Object of class to store comm settings

'''
Functions
'''
def set_com_port(port):
    g_com_settings.port = port
    return

def get_sercomm_settings():
    return copy.copy(g_com_settings)

'''
Function Description: Generates a new window designed to set various
settings for communication and logging

Parameters: void 

Return: void
'''
def define_sercomm_settings_window():

    # Create new window over the main window
    global g_settings_window
    g_settings_window = Toplevel()
    g_settings_window.geometry("270x210")
    g_settings_window.resizable(width=False, height=False)
    g_settings_window.title("Shawn's COM port settings")

    # Disabled access to main terminal window
    g_settings_window.grab_set()
    g_settings_window.focus()
    # Install window close routine
    g_settings_window.protocol("WM_DELETE_WINDOW",g_settings_window.destroy)

    # Create new frames
    config_frame0 = ui_objects.define_frame(g_settings_window, 0, 0)
    config_frame0.grid(sticky=NW)
    config_frame1 = ui_objects.define_frame(g_settings_window, 0, 1)
    config_frame1.grid(sticky=NW)

    # Define UI objects

    # Define a label for baud rates
    baud_rate_label = ui_objects.define_label(config_frame0, "Baud Rate: ", 0, 0)
    baud_rate_label.grid(sticky=W)
    # Generate list of baud rates
    bauds = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 
                2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 
                460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 
                2000000, 2500000, 3000000, 3500000, 4000000]
    # Create a drop down menu with different baud rates
    global g_baud_rate_dd 
    g_baud_rate_dd = ui_objects.define_drop_down(config_frame0, bauds, 'readonly', 1, 0)
    g_baud_rate_dd.grid(sticky=W)
    # Set default value (9600) of drop down menu
    g_baud_rate_dd.current(bauds.index(int(g_com_settings.baud))) 

    # Define a label for bytesize
    bytesize_label = ui_objects.define_label(config_frame0, "Byte size: ", 0, 1)
    bytesize_label.grid(sticky=W)
    # Generate list of byte sizes
    bytesize = [5, 6, 7, 8]
    # Create a drop down menu with different settings
    global g_bytesize_dd
    g_bytesize_dd = ui_objects.define_drop_down(config_frame0, bytesize, 'readonly', 1, 1)
    g_bytesize_dd.grid(sticky=W)
    # Set default value (8 bits) of drop down menu
    g_bytesize_dd.current(bytesize.index(int(g_com_settings.bytesize)))

    # Define a label for parity bits
    paritybits_label = ui_objects.define_label(config_frame0, "Parity bits: ", 0, 2)
    paritybits_label.grid(sticky=W)
    # Generate list of parity modes
    paritybits = ["None", "Even", "Odd", "Mark", "Space"]
    # Create a drop down menu with different settings
    global g_paritybits_dd 
    g_paritybits_dd = ui_objects.define_drop_down(config_frame0, paritybits, 'readonly', 1, 2)
    g_paritybits_dd.grid(sticky=W)
    # Set default value (None) of drop down menu
    match g_com_settings.paritybits:
        case "N":
            g_paritybits_dd.current(paritybits.index("None"))
        case "E":
            g_paritybits_dd.current(paritybits.index("Even"))
        case "O":
            g_paritybits_dd.current(paritybits.index("Odd"))
        case "M":
            g_paritybits_dd.current(paritybits.index("Mark"))
        case "S":
            g_paritybits_dd.current(paritybits.index("Space"))

    # Define a label for stop bits
    stopbits_label = ui_objects.define_label(config_frame0, "Stop bits: ", 0, 3)
    stopbits_label.grid(sticky=W)
    # Generate list of parity modes
    stopbits = [1, 1.5, 2]
    # Create a drop down menu with different settings
    global g_stopbits_dd 
    g_stopbits_dd = ui_objects.define_drop_down(config_frame0, stopbits, 'readonly', 1, 3)
    g_stopbits_dd.grid(sticky=W)
    # Set default value (1) of drop down menu
    g_stopbits_dd.current(stopbits.index(float(g_com_settings.stopbits)))

    # Define Read timeout
    # Define a label for read timeout
    readtimeout_label = ui_objects.define_label(config_frame0, "Read timeout(s): ", 0, 4)
    readtimeout_label.grid(sticky=W)
    # Create a text box to get the transmit message from user
    global g_timeout_textbox
    g_timeout_textbox = ui_objects.define_entry_textbox(config_frame0, 1, 'normal', 1, 4)
    g_timeout_textbox.grid(sticky=NSEW)
    g_timeout_textbox.insert(0, g_com_settings.readtimeout)

    global g_enable_logging_flag
    # Enable logging disabled by default
    g_enable_logging_flag = FALSE
    # Define an enable logging checkbox
    enable_logging_checkbox = ui_objects.define_checkbox(config_frame0, "Enable Logging",
                        "normal", g_enable_logging_flag, enable_logging, 0, 5)
    enable_logging_checkbox.grid(sticky=W)

    # Define a set port settings button
    confirm_button = ui_objects.define_button(config_frame1, "Confirm", 'normal',
                                confirm_settings, 1, 0)
    confirm_button.grid(sticky=E)
    # Bind enter key to confirm button by default
    g_settings_window.protocol("<Return>",confirm_settings)

    # Define a cancel button
    cancel_button = ui_objects.define_button(config_frame1, "Cancel", 'normal',
                                g_settings_window.destroy, 0, 0)
    cancel_button.grid(sticky=E)

    if g_com_settings.logfile != None:
        enable_logging_checkbox['state'] = "disabled"

    return

def confirm_settings():

    global g_com_settings
    # Tracks previously set port settings
    com_settings_new = com_struct
    com_settings_new = copy.deepcopy(g_com_settings)

    # Ensure log file checkbox is selected and appropriate directory
    # has been chosen by user
    if(g_enable_logging_flag == TRUE):

        # Define the name of the log file as "log"_"Date"_"Time"_.csv
        filename = "log_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_.csv"

        com_settings_new.logfile = asksaveasfile(initialfile = filename,
        defaultextension=".csv", filetypes=[(".csv", "*.csv")])

        # Check if cancel button was clicked by user in savfileas dialog
        if com_settings_new.logfile == None:
            return -1

    elif(g_enable_logging_flag == FALSE):
       com_settings_new.logfile = None

    # Modify parity bit option to format required by function
    match g_paritybits_dd.get():
        case "None":
            parity_bit = serial.PARITY_NONE
        case "Even":
            parity_bit = serial.PARITY_EVEN
        case "Odd":
            parity_bit = serial.PARITY_ODD
        case "Mark":
            parity_bit = serial.PARITY_MARK
        case "Space":
            parity_bit = serial.PARITY_SPACE
        case _:
            return -1

    # Ensure timeout value is a valid numeric value
    if (g_timeout_textbox.get().isnumeric() == FALSE):
        g_settings_window.bell()
        return -1

    # Set value in global struct
    com_settings_new.baud = g_baud_rate_dd.get()
    com_settings_new.bytesize = g_bytesize_dd.get()
    com_settings_new.stopbits =  g_stopbits_dd.get()
    com_settings_new.paritybits = parity_bit
    com_settings_new.readtimeout = g_timeout_textbox.get()

    # Only close and reopen port if given settings have changed
    # since previous port settings
    if(com_settings_new != g_com_settings):

        sercomm.close_serial_com()

        status = sercomm.open_serial_com(g_com_settings.port, g_com_settings.baud, 
        g_com_settings.bytesize, g_com_settings.readtimeout, g_com_settings.stopbits, 
        g_com_settings.paritybits)

        # If opening the serial com port failed

        if status < 0:
            g_settings_window.bell()
            return -1

        # Update global comm settings
        g_com_settings = com_settings_new

    # close window
    g_settings_window.destroy()

    return 0


def enable_logging():
    global g_enable_logging_flag    #Define scope of variable
    #Python seems to think its a local for some reason otherwise
    
    # Enable log file textbox if checkbox is set
    if g_enable_logging_flag == TRUE:

        g_enable_logging_flag = FALSE
    else:    
        g_enable_logging_flag = TRUE

