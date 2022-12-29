import tkinter # Import tkinter library used to generate GUI
from tkinter import * # Import tkinter modules used to generate GUI
from tkinter.filedialog import asksaveasfile # Import tkinter file save module

import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

import ui_objects   # custom library built to handle common UI objects
import sercomm  

'''
Structure and Enumaerations
'''

'''
Class used as struct to store comm settings
'''
class com_struct:
    def __init__(self):
        self.baud = 9600
        self.bytesize = 8
        self.paritybits = "None"
        self.stopbits = 1
        self.readtimeout = 0
        self.logging = 0


g_com_settings = com_struct() # Object of class to store comm settings


'''
Functions
'''

def get_sercomm_settings():

    return g_com_settings

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
    g_settings_window.geometry("440x210")
    g_settings_window.resizable(width=False, height=False)
    g_settings_window.title("Shawn's COM port settings")

    # Disabled access to main terminal window
    g_settings_window.grab_set()
    g_settings_window.focus()

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
                2400, 4800, 9600, 19200, 38400, 57600, 115200,  230400, 
                460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 
                2000000, 2500000, 3000000, 3500000, 4000000]
    # Create a drop down menu with different baud rates
    global g_baud_rate_dd 
    g_baud_rate_dd = ui_objects.define_drop_down(config_frame0, bauds, 'readonly', 1, 0)
    g_baud_rate_dd.grid(sticky=W)
    # Set default value (9600) of drop down menu
    g_baud_rate_dd.current(12) 

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
    g_bytesize_dd.current(3)

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
    g_paritybits_dd.current(0)

    # Define a label for stop bits
    stopbits_label = ui_objects.define_label(config_frame0, "Stop bits: ", 0, 3)
    stopbits_label.grid(sticky=W)
    # Generate list of parity modes
    stopbits = [1, 1.5, 2]
    # Create a drop down menu with different settings
    global g_stopbits_dd 
    g_stopbits_dd = ui_objects.define_drop_down(config_frame0, stopbits, 'readonly', 1, 3)
    g_stopbits_dd.grid(sticky=W)
    # Set default value (None) of drop down menu
    g_stopbits_dd.current(0)

    # Define Read timeout
    # Define a label for read timeout
    readtimeout_label = ui_objects.define_label(config_frame0, "Read timeout(s): ", 0, 4)
    readtimeout_label.grid(sticky=W)
    # Create a text box to get the transmit message from user
    global g_timeout_textbox
    g_timeout_textbox = ui_objects.define_entry_textbox(config_frame0, 1, 'normal', 1, 4)
    g_timeout_textbox.grid(sticky=NSEW)

    # Define an enable logging checkbox
    enable_logging_checkbox = ui_objects.define_checkbox(config_frame0, "Enable Logging",
                        "normal", None, enable_logging, 0, 5)
    enable_logging_checkbox.grid(sticky=W)

    # Define a choose file button for logging
    global g_choose_file_button
    g_choose_file_button = ui_objects.define_button(config_frame0, "Choose file", 'disabled',
                                select_file, 1, 5)
    g_choose_file_button.grid(sticky=W)

    # Create a text box to get the transmit message from user
    # Defined global so toggle function can access it
    global g_logfile_textbox 
    g_logfile_textbox = ui_objects.define_entry_textbox(config_frame0, 47, 'disabled', 0, 6)
    g_logfile_textbox.grid(sticky=NSEW)

    # Define a set port settings button
    confirm_button = ui_objects.define_button(config_frame1, "Confirm", 'normal',
                                confirm_settings, 1, 0)
    confirm_button.grid(sticky=E)

    # Define a cancel button
    cancel_button = ui_objects.define_button(config_frame1, "Cancel", 'normal',
                                g_settings_window.destroy, 0, 0)
    cancel_button.grid(sticky=E)

    return

def select_file():

    return

def confirm_settings():

    # Save logging file if required
    

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


    # Set value in global struct
    g_com_settings.baud = g_baud_rate_dd.get()
    g_com_settings.bytesize = g_bytesize_dd.get()
    g_com_settings.stopbits =  g_stopbits_dd.get()
    g_com_settings.paritybits = parity_bit
    g_com_settings.readtimeout = g_timeout_textbox.get()
    #g_com_settings.logging = 

    # reopen with new values
    #sercomm.open_serial_com(com_port, g_baud_rate_dd.get(), g_bytesize_dd.get(), g_timeout_textbox.get(),
    #                        g_stopbits_dd.get(), parity_bit)

    # close window
    g_settings_window.destroy()


def enable_logging():
    # Enable log file textbox if checkbox is set
    if (g_logfile_textbox['state'] == "disabled"):
        g_logfile_textbox['state'] = "normal"
        g_choose_file_button['state'] = "normal"
    else:
        g_logfile_textbox['state'] = "disabled"
        g_choose_file_button['state'] = "disabled"


