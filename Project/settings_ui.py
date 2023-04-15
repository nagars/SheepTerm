from tkinter import *   # Import tkinter modules used to generate GUI

import serial           # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
#from serial import SerialException          # Import pyserial exception handling

import copy     # Import copy module for shallow copy of objects
import math     # Import math for floats comparison

from datetime import datetime   # Import system date library

''' Custom Modules'''
import ui_objects   # custom library built to handle common UI objects
import sercomm      # custom library for sercomm api
import csvlogger as log   # custom library for logging data to .csv file

'''
Structure and Enumerations
'''
class comm_settings_class:
    def __init__(self) -> None:
        self.portname = None
        self.baud : int = 9600
        self.bytesize : int = 8
        self.paritybits = serial.PARITY_NONE
        self.stopbits : float = 1.0
        self.readtimeout : float = 1.0
    
    def __eq__(objA, objB):
        if not isinstance(objB, comm_settings_class):
            # Don't attempt to compare against unrelated types
            raise Exception ("Objects to be compared are not the same class")
       
        return objA.portname == objB.portname \
            and objA.baud == objB.baud \
            and objA.bytesize == objB.bytesize \
            and objA.paritybits == objB.paritybits \
            and math.isclose(objA.stopbits,objB.stopbits) \
            and math.isclose(objA.readtimeout,objB.readtimeout) \


'''
Class used as struct to store comm settings
'''
class settings_window_class(comm_settings_class):
    def __init__(self) -> None:

        self.com_settings = comm_settings_class()   # Instance of comm settings struct
        self.logger = log.csvlogger_class()

        self.window = None
        self.__baud_rate_dd = None        # Object to baud rate drop down menu
        self.__bytesize_dd = None         # Object to byte size drop down menu
        self.__paritybits_dd = None       # Object to parity bits drop down menu
        self.__stopbits_dd = None         # Object to stop bits drop down menu
        self.__timeout_textbox_dd = None     # Object to timeout input text box
        self.__enable_logging_flag = None # Tracks if csv logger should be called or not
        return
    
    '''
    Function Description: Generates a new window designed to set various
    settings for communication and logging. 

    Parameters: void 

    Return: Identifier for tkinter settings window
    '''
    def create_window(self):

        # Create new window over the main window
        self.window = Toplevel()
        self.window.geometry("341x258")
        self.window.resizable(width=False, height=False)
        self.window.title("Sheep Settings")

        # Disabled access to main terminal window
        self.window.grab_set()
        self.window.focus()
        # Install window close routine
        self.window.protocol("WM_DELETE_WINDOW",self.window.destroy)

        # Create new frames
        config_frame0 = ui_objects.define_frame(self.window, 0, 0)
        config_frame0.grid(sticky=NW)
        config_frame1 = ui_objects.define_frame(self.window, 0, 1)
        config_frame1.grid(sticky=NW)

        # Define UI objects

        # Define a label for baud rates
        baud_rate_label = ui_objects.define_label(config_frame0, 0, 0, "Baud Rate: ")
        baud_rate_label.grid(sticky=W)
        # Generate list of baud rates
        bauds = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 
                    2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 
                    460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 
                    2000000, 2500000, 3000000, 3500000, 4000000]
        # Create a drop down menu with different baud rates
        self.__baud_rate_dd = ui_objects.define_drop_down(config_frame0, 1, 0, bauds, 'readonly')
        self.__baud_rate_dd.grid(sticky=W)
        # Set default value (9600) of drop down menu
        self.__baud_rate_dd.current(bauds.index(int(self.com_settings.baud))) 

        # Define a label for bytesize
        bytesize_label = ui_objects.define_label(config_frame0, 0, 1, "Byte size: ")
        bytesize_label.grid(sticky=W)
        # Generate list of byte sizes
        bytesize = [5, 6, 7, 8]
        # Create a drop down menu with different settings
        self.__bytesize_dd = ui_objects.define_drop_down(config_frame0, 1, 1, bytesize, 'readonly')
        self.__bytesize_dd.grid(sticky=W)
        # Set default value (8 bits) of drop down menu
        self.__bytesize_dd.current(bytesize.index(int(self.com_settings.bytesize)))

        # Define a label for parity bits
        paritybits_label = ui_objects.define_label(config_frame0, 0, 2, "Parity bits: ")
        paritybits_label.grid(sticky=W)
        # Generate list of parity modes
        paritybits = ["None", "Even", "Odd", "Mark", "Space"]
        # Create a drop down menu with different settings
        self.__paritybits_dd = ui_objects.define_drop_down(config_frame0, 1, 2, paritybits, 'readonly')
        self.__paritybits_dd.grid(sticky=W)
        # Set default value (None) of drop down menu
        match self.com_settings.paritybits:
            case "N":
                self.__paritybits_dd.current(paritybits.index("None"))
            case "E":
                self.__paritybits_dd.current(paritybits.index("Even"))
            case "O":
                self.__paritybits_dd.current(paritybits.index("Odd"))
            case "M":
                self.__paritybits_dd.current(paritybits.index("Mark"))
            case "S":
                self.__paritybits_dd.current(paritybits.index("Space"))

        # Define a label for stop bits
        stopbits_label = ui_objects.define_label(config_frame0, 0, 3, "Stop bits: ")
        stopbits_label.grid(sticky=W)
        # Generate list of parity modes
        stopbits = [1, 1.5, 2]
        # Create a drop down menu with different settings
        self.__stopbits_dd = ui_objects.define_drop_down(config_frame0, 1, 3, stopbits, 'readonly')
        self.__stopbits_dd.grid(sticky=W)
        # Set default value (1) of drop down menu
        self.__stopbits_dd.current(stopbits.index(float(self.com_settings.stopbits)))

        # Define Read timeout
        # Define a label for read timeout
        readtimeout_label = ui_objects.define_label(config_frame0, 0, 4, "Read timeout(s): ")
        readtimeout_label.grid(sticky=W)
        # Create a text box to get the transmit message from user
        self.__timeout_textbox_dd = ui_objects.define_entry_textbox(config_frame0, 1, 4, 1, 'normal')
        self.__timeout_textbox_dd.grid(sticky=NSEW)
        self.__timeout_textbox_dd.insert(0, self.com_settings.readtimeout)

        #global g_enable_logging_flag
        # Enable logging disabled by default
        self.__enable_logging_flag = False
        # Define an enable logging checkbox
        enable_logging_checkbox = ui_objects.define_checkbox(config_frame0, 0, 5, "Enable Logging",
                            self.__enable_logging_flag, self.enable_logging, "normal", "success-round-toggle")
        enable_logging_checkbox.grid(sticky=W)

        # Define a set port settings button
        confirm_button = ui_objects.define_button(config_frame1, 1, 0, "Confirm",
                                    self.confirm_settings, 'normal')
        confirm_button.grid(sticky=E)
        # Bind enter key to confirm button by default
        self.window.protocol("<Return>",self.confirm_settings)

        # Define a cancel button
        cancel_button = ui_objects.define_button(config_frame1, 0, 0, "Cancel",
                                    self.window.destroy, 'normal')
        cancel_button.grid(sticky=E)

        if self.logger.file_obj != None:
            enable_logging_checkbox['state'] = "disabled"

        return self.window

    '''
    Function Description: Accepts new settings, checks
    if they are valid. Ensures the new settings are different from the 
    previous settings before closing adn opening serial port
    with new settings. If the enable log checkbox is selected,
    calls a savefile dialog

    Paramters: void

    Return: True on success / False on Failure
    '''

    def confirm_settings(self, event=None):

        #global g_com_settings
        # Tracks previously set port settings
        com_settings_new = copy.copy(self.com_settings)

        # Ensure log file checkbox is selected and appropriate directory
        # has been chosen by user
        if(self.__enable_logging_flag == True):

            # Define the name of the log file as "log"_"Date"_"Time"_.csv
            filename = "log_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".csv"

            self.logger.file_obj = self.logger.create_csv(filename)

            # Check if cancel button was clicked by user in savfileas dialog
            if  self.logger.file_obj is None:
                return False
            
            # Write the header fields in the log file
            self.logger.logger.write_row_csv(['Timestamp','RX/TX','Data'])

        # Modify parity bit option to format required by function
        match self.__paritybits_dd.get():
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
                return False

        # Set value in global struct
        com_settings_new.baud = int(self.__baud_rate_dd.get())
        com_settings_new.bytesize = int(self.__bytesize_dd.get())
        com_settings_new.stopbits =  float(self.__stopbits_dd.get())
        com_settings_new.paritybits = parity_bit
        # Ensure that the timeout value entered by the user is a valid number
        try:
            com_settings_new.readtimeout = float(self.__timeout_textbox_dd.get())
        except ValueError:
            self.window.bell()
            return False

        # Ensure timeout is not negative
        if(com_settings_new.readtimeout < 0):
            self.window.bell()
            return False

        # Only close and reopen port if given settings have changed
        # since previous port settings
        if(com_settings_new != self.com_settings):

            status = sercomm.close_serial_com()
            # Check if serial port was closed
            if status  == False:
                self.window.bell()
                return False

            status = sercomm.open_serial_com(com_settings_new.portname, com_settings_new.baud, 
            com_settings_new.bytesize, com_settings_new.readtimeout, com_settings_new.stopbits, 
            com_settings_new.paritybits)

            # If opening the serial com port failed
            if status < False:
                self.window.bell()
                return False

            # Update global comm settings
            self.com_settings = copy.copy(com_settings_new)

        # close window
        self.window.destroy()

        return True
    '''    
        # To perform a comparison of 2 objects of this class, I
        # chose to over ride the comparison operator
        def __eq__(objA, objB): 
            if not isinstance(objB, settings_class):
                # Don't attempt to compare against unrelated types
                raise Exception ("Objects to be compared are not the same class")

            return objA.com_settings == objB.com_settings \
                and objA.logger == objB.logger \
                and objA.term_theme == objB.term_theme
    '''

    '''
    Functions
    '''

    '''
    Function Description: Setter function for portname in global settings_class

    Parameters: portname - Name of com port

    Return: void
    '''
    def set_com_port(self, portname):
        self.com_settings.portname = copy.copy(portname)
        return

    '''
    Function Description: Getter for global serial com settings

    Parameters: void

    Return: copy of global com struct
    '''
    def get_sercomm_settings(self):
        return self.com_settings



    '''
    Function Description: Toggles the enable logging flag.
    Called when action on logging checkbox by user

    Parameters: void

    Return: void
    '''
    def enable_logging(self):
        #global g_enable_logging_flag    #Define scope of variable
        #Python seems to think its a local for some reason otherwise
        
        # Enable log file textbox if checkbox is set
        if self.__enable_logging_flag == True:

            self.__enable_logging_flag = False
        else:    
            self.__enable_logging_flag = True

