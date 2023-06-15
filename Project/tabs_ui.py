'''Generic Modules'''
import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
import threading                     # Imports python threading module

from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.

from datetime import datetime   # Import system date library

'''Custom Modules'''
import sercomm      # custom library built to handle communication
import settings_ui  # custom library built to manage the settings window 
import objects_ui   # custom library built to handle common UI objects

'''
Frame Position values (y,x)
'''
com_frame_pos               = 0,0
config_frame_pos            = 1,0
display_frame_pos           = 0,1
display_button_frame_pos    = 0,2

'''
Widget Position Values (y,x)
'''
# Com Frame
com_port_label_pos          = 0,0
com_ports_menu_pos          = 1,0

# Config Frame
open_com_button_pos         = 0,0
settings_button_pos         = 1,0

space_label_pos0            = 2,0
display_type_label_pos      = 3,0
data_types_dd_pos           = 4,0

space_label_pos1            = 5,0
timestamp_checkbox_pos                  = 6,0
include_new_line_checkbox_pos           = 7,0
include_carriage_return_checkbox_pos    = 8,0
echo_checkbox_pos                       = 9,0

# Display Frame
terminal_box_pos                        = 0,0
send_message_textbox_pos                = 0,1

# Button Frame
send_button_pos                         = 0,0
clear_button_pos                        = 1,0

'''
Classes
'''
class terminal_tab:
    def __init__(self, window, notebook, tab_name) -> None:

        '''
        Public Objects
        '''
        self.tab_frame = objects_ui.define_frame(notebook,0,0)    # Defines the tab for this class instance
        self.tab_frame.grid(sticky=NSEW)
        self.tab_frame.columnconfigure(1, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)
        
        self.name = tab_name                    # Tracks the name of this tab
        self.terminate_event_flag = threading.Event() # Object is used to sync receive thread with main loop
        self.receive_thread = None       # Object is assigned the receive thread handle on initialisation

        self.settings = settings_ui.settings_window_class(self.name)    # Instance of settings class

        self.window = window        # Track current window the tab is in

        '''
        Define tkinter variables
        '''
        # Tracks if user enabled timestamping of data on terminal
        self.timestamp_flag = tkinter.BooleanVar() 
        # Tracks if user enabled NL to be appended to data sent
        self.include_new_line_flag = tkinter.BooleanVar()
        # Tracks if user enabled CR to be appended to data sent
        self.include_carriage_return_flag = tkinter.BooleanVar()
        # Tracks if user wants to echo the transmitted message on terminal
        self.echo_enable_flag = tkinter.BooleanVar()

        '''
        Define frames of tab
        '''
        # Create COM Frame for COM port settings
        self.com_frame = objects_ui.define_frame(self.tab_frame,com_frame_pos[0],com_frame_pos[1],NSEW)

        # Create Display Configure Frame for checkbox
        self.config_frame = objects_ui.define_frame(self.tab_frame, config_frame_pos[0], config_frame_pos[1],NSEW)

        # Create a Terminal frame to display actual data
        self.display_frame = objects_ui.define_frame(self.tab_frame,display_frame_pos[0],display_frame_pos[1],NSEW)
        self.display_frame.grid(columnspan = 3)
        # Ensure the terminal box expands with the frame
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)

        # Create a boundary frame for the bottom
        self.display_button_frame = objects_ui.define_frame(self.tab_frame,display_button_frame_pos[0],display_button_frame_pos[1],SE)
        # Have frame cover 3 frames of space
        self.display_button_frame.grid(columnspan = 3)

        '''
        Define COMM frame UI objects
        '''
        # Define a label for com port to be placed near text box
        self.com_port_label = objects_ui.define_label(self.com_frame, com_port_label_pos[0], com_port_label_pos[1], "Com Port")

        # List all the available serial ports
        self.com_ports_available = list(port_list.comports())
        # Remove unusable com port options
        # (NULL appended com port names seem to appear. Possibly due to using
        #  virtual com ports?)
        for item in self.com_ports_available:
            print(item)
            if str(item)[0:5] == "NULL_":
                self.com_ports_available.remove(item)
        self.com_ports_available.append("COM8") #REMOVE POST TESTING!@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.com_ports_available.append("COM9") #REMOVE POST TESTING!@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Define the drop down menu for com ports
        self.com_ports_menu = objects_ui.define_drop_down(self.com_frame, com_ports_menu_pos[0], com_ports_menu_pos[1], 
                                                          self.com_ports_available, 'readonly')
        # Set width to 20 Characters
        self.com_ports_menu.config(width=20)

        '''
        Define onfig frame UI objects
        '''
        # Define Set COM port button
        self.open_com_button = objects_ui.define_button(self.config_frame, open_com_button_pos[0], 
                                            open_com_button_pos[1], "Open Port", lambda: type(self).open_com_port(self), 'normal')

        # Define a settings button for sercomm settings
        self.settings_button = objects_ui.define_button(self.config_frame, settings_button_pos[0], 
                                            settings_button_pos[1], "Settings", lambda: type(self).open_settings_window(self), 'disabled')

        # Define a label to act as a spacer
        self.space_label0 = objects_ui.define_label(self.config_frame, space_label_pos0[0], space_label_pos0[1], "|")
        self.space_label0.grid(padx = 10, pady = 0)
        self.space_label0.configure(font=(NONE,15), foreground="#808080")

        # Define a label for data type drop down
        self.display_type_label = objects_ui.define_label(self.config_frame, display_type_label_pos[0], 
                                                          display_type_label_pos[1], "Display Type")

        #Generate list of data types
        self.data_types = ["STRING","ASCII","HEX", "BINARY"]
        #Create a drop down menu with different datatypes to represent on terminal
        self.data_types_dd = objects_ui.define_drop_down(self.config_frame, data_types_dd_pos[0], data_types_dd_pos[1], 
                                                         self.data_types, 'readonly')
        # Set width to 7 characters
        self.data_types_dd.config(width=7)
        #Set default value of drop down menu
        self.data_types_dd.current(0)   

        # Define a label to act as a spacer
        self.space_label1 = objects_ui.define_label(self.config_frame, space_label_pos1[0], space_label_pos1[1], "|")
        self.space_label1.grid(padx = 10, pady = 0)
        self.space_label1.configure(font=(NONE,15), foreground="#808080")

        #Create a show timestamp checkbox
        self.timestamp_checkbox = objects_ui.define_checkbox(self.config_frame, timestamp_checkbox_pos[0], timestamp_checkbox_pos[1], 
                                                "Show Timestamp", self.timestamp_flag, None, 'normal', 'round-toggle')

        #Create an include next line character checkbox
        self.include_new_line_checkbox = objects_ui.define_checkbox(self.config_frame, include_new_line_checkbox_pos[0], 
                                                include_new_line_checkbox_pos[1], "Include New Line Character",
                                                self.include_new_line_flag, None, "normal", 'round-toggle')

        #Create an include carriage return character checkbox
        self.include_carriage_return_checkbox = objects_ui.define_checkbox(self.config_frame, include_carriage_return_checkbox_pos[0], 
                                                include_carriage_return_checkbox_pos[1], "Include Carriage Return Character",
                                                self.include_carriage_return_flag, None, "normal", 'round-toggle')

        #Create a echo checkbox
        self.echo_checkbox = objects_ui.define_checkbox(self.config_frame, echo_checkbox_pos[0], echo_checkbox_pos[1], "Enable Echo",
                                                self.echo_enable_flag, None, "normal", 'round-toggle')

        '''
        Define Terminal frame UI objects
        '''
        # Create a scroll text box for the terminal
        self.terminal_box = objects_ui.define_scroll_textbox(self.display_frame, terminal_box_pos[0], terminal_box_pos[1], 50, 20)
        self.terminal_box.grid(sticky=NSEW)
        self.terminal_box.configure(font=('Times New Roman',11))

        # Create a text box to get the transmit message from user
        self.send_message_textbox = objects_ui.define_entry_textbox(self.display_frame, send_message_textbox_pos[0], 
                                                                    send_message_textbox_pos[1], 47, 'disabled')
        self.send_message_textbox.grid(sticky=NSEW)
        self.send_message_textbox.configure(font=('Times New Roman',11))

        '''
        Define Button frame UI objects
        '''
        # Create a button to send data on selected port
        self.send_button = objects_ui.define_button(self.display_button_frame, send_button_pos[0], send_button_pos[1], "Send",
                           lambda:  type(self).send_button_pressed(self), 'disabled')
        self.send_button.grid(padx=5, pady=5)
        
        # Create a clear terminal display button
        self.clear_button = objects_ui.define_button(self.display_button_frame, clear_button_pos[0], clear_button_pos[1], 
                                                     "Clear", lambda: type(self).clear_button_pressed(self), 'normal')
        self.clear_button.grid(padx=5, pady=5)


        return


    '''
    Instance Methods
    '''

    '''
    Function Description: Closes come port, file pointer
    to log file (If open) and program.
    Ensures recieve_thread terminate gracefully

    Parameters: void

    Return: void
    '''
    def close_tab(self):

        # Check if the receive thread was started
        # If not, directly terminate program
        # else terminate the thread and then the program 
        if self.receive_thread is None:
            pass

        else:
            # Set terminate flag for receive thread
            self.terminate_event_flag.set()

            # Cancel any pending read
            sercomm.abort_serial_read(self.settings.com_settings.serialport)

            # wait till receive thread is terminated
            self.receive_thread.join()

        # Close the com port
        sercomm.close_serial_com(self.settings.com_settings.serialport)

        # Close file pointer for logger
        self.settings.logger.close_csv()

        return


    '''
    Class Methods
    '''

    '''
    Function Description: Opens selected com port
    from drop down menu. Creates receive thread if
    com port opened successfully. Modifies UI to
    represent opened com port.

    Parameters: tab - Instance of terminal_tab 

    Return: com port name on Success / False on Failure
    '''
    @classmethod
    def open_com_port(cls, tab):

        # Ensure a com port was selected
        if tab.com_ports_menu.get() == '':
            type(tab).print_to_terminal(tab, "No COM port selected!\n")
            return False

        # Extract com port name from drop down string
        com_port = tab.com_ports_menu.get().split()[0]

        # Get a copy of com port settings
        sercomm_settings = tab.settings.get_sercomm_settings()

        # Open port
        serial_port = sercomm.open_serial_com(com_port, sercomm_settings.baud, 
                                            sercomm_settings.bytesize, sercomm_settings.readtimeout,
                                            sercomm_settings.stopbits, sercomm_settings.paritybits)

        #Check return value
        if serial_port == False:
            type(tab).print_to_terminal(tab, com_port + " is busy. Unable to open\n")
            return False

        # Print COM port opened successfully.
        type(tab).print_to_terminal(tab, com_port + " opened successfully\n")

        # Disable open com port button
        tab.open_com_button['state'] = 'disabled'

        # Enable send message textbox
        tab.send_message_textbox['state'] = 'normal'

        # Enable send message button
        tab.send_button['state'] = 'active'

        # Disable settings button
        tab.settings_button['state'] = 'normal'

        # Disable drop down menu for com ports
        tab.com_ports_menu['state'] = 'disabled'

        # Set current com port variable in com settings struct
        tab.settings.com_settings.portname = com_port

        # save valid serial port to class variable
        tab.settings.com_settings.serialport = serial_port

        # Create receive thread to print to terminal
        tab.receive_thread = threading.Thread(target= lambda: type(tab).receive_thread(tab))
        tab.receive_thread.start()

        # Bind enter key to send button
        #tab.window.bind("<Return>", lambda event=None: terminal_tab.send_button_pressed(tab))

        return com_port


    '''
    Function Description: Transmits data in transmit text box
    to com port. Clears the send text box

    Parameters: tab - Instance of terminal_tab 

    Return: void
    '''
    @classmethod
    def send_button_pressed(cls, tab, event=None):

        # Read message to transmit from textbox
        transmit_msg = tab.send_message_textbox.get()

        # If Carriage return check box is selected, append \r
        if tab.include_carriage_return_flag.get() == True:
            transmit_msg += '\r'

        # If Next line check box is selected, append \n
        if tab.include_new_line_flag.get() == True:
            transmit_msg += '\n'

        # Check is msg is empty
        if transmit_msg == '':
            return False

        # Transmit
        sercomm.write_serial_com(tab.settings.com_settings.serialport, transmit_msg)

        # If echo_enable flag is set
        if tab.echo_enable_flag.get() == True:
            
            # Time stamp when data was received
            logtime = datetime.now().strftime('%H:%M:%S.%f')[:-3]

            # Update message data type for printing based on drop down
            print_msg = type(tab).update_msg_datatype(tab.data_types_dd.get(),transmit_msg)
            # Remove the \r and \n characters when printing to terminal and logging
            print_msg = print_msg.strip('\r\n')

            #Check if timestamp is required. Append to message
            if (tab.timestamp_flag.get() == True):
                type(tab).print_to_terminal(tab,'\n' + logtime + " :\t\tTX: " + print_msg)

            else:
                type(tab).print_to_terminal(tab,'\n' + "TX: " + print_msg)

            # Log data if required. Check that empty messages dont get logged
            #curr_sercom_settings = tab.settings.get_sercomm_settings()
            if ((tab.settings.logger.file_obj != None) & (print_msg != '')):
                if tab.echo_enable_flag.get() == True:
                    tab.settings.logger.write_row_csv([logtime,"TX",print_msg])    
                else:
                    # Write to .csv file
                    tab.settings.logger.write_row_csv([logtime,print_msg])

        # Delete all text in display
        tab.send_message_textbox.delete("0",END)

        return

    '''
    Function Description: Terminates the receive thread and calls
    function to open the serial settings window. Waits for settings 
    window to close, checks if serial port is open and creates a new
    receive thread. If not open, disables operations until same or
    another port is opened by the user.

    Parameters: tab - Instance of terminal_tab 

    Return: True on Success / False on Failure
    '''
    @classmethod
    def open_settings_window(cls, tab):

        # Terminate receive thread 
        # to prevent a read operation while
        # the user closes and reopens the 
        # serial port with new settings

        # Set terminate flag for receive thread
        tab.terminate_event_flag.set()

        # Abort any read operation
        sercomm.abort_serial_read(tab.settings.com_settings.serialport)

        # Wait till receive thread is terminated
        tab.receive_thread.join()

        # Call open settings window function
        tab.settings.create_window()

        # Wait for the settings window to close
        tab.window.wait_window(tab.settings.window)

        # Ensure serial port is open successfully
        if sercomm.check_serial_port_status(tab.settings.com_settings.serialport) == True:

            # Once settings are confirmed, 
            # Clear terminate_event flag and start receive thread again
            tab.terminate_event_flag.clear()

            tab.receive_thread = threading.Thread(target= lambda: type(tab).receive_thread(tab))
            tab.receive_thread.start()

        else:
            type(tab).print_to_terminal("Port is busy. Unable to open\n")

            # Return UI to original state so user can retry
            # opening the port or select a new port

            # Enable open com port button
            tab.open_com_button['state'] = 'normal'

            # Disable send message textbox
            tab.send_message_textbox['state'] = 'disabled'

            # Disable send message button
            tab.send_button['state'] = 'disabled'

            # Disable settings button
            tab.settings_button['state'] = 'disabled'

            return False

        return True



    '''
    Function Description: Updates message data types based on 
    the current selected data type in drop down menu of terminal

    Paramete:   dislay_type - selection to convert message to 
                msg - string to be converted into string of new data type

    Return: New message string
    '''
    @classmethod
    def update_msg_datatype(cls, display_type, msg):
        
        print_msg = ''

        # Change data format based on drop down menu selection
        match display_type:
            case "STRING":
                print_msg = msg    
                
            case "ASCII":
                for i in msg:
                    print_msg += str(ord(i)) + ' '
            
            case "HEX":
                for i in msg:
                    print_msg += str(hex(ord(i))[2:]) + ' '
            
            case "BINARY":
                for i in msg:
                    print_msg += str(bin(ord(i))[2:]) + ' '

            case _:
                return False
        
        return print_msg


    '''
    Function Description: Function to be called as separate thread. Receives data
    from serial port, logs if required, converts to selected display format
    and prints to terminal. Checks if a read timeout has occurred and 
    appends new lines + timestamp if required.

    Parameters: tab - Instance of terminal_tab 

    Return: True - Successful / False - Failure
    '''
    @classmethod
    def receive_thread(cls, tab):

        # Flag to track if a read timeout has occurred
        serial_timout_occurred = False
        # Initialise log_msg variable
        log_msg = ''    

        # Maintain the thread until the terminate event flag is set
        # flag is set when the user attempts to close the window and
        # terminate the program or to change settings of the serial port
        while not tab.terminate_event_flag.is_set():
            # Get data from serial port
            # Convert to string from bytes
            msg = (sercomm.read_serial_com(tab.settings.com_settings.serialport)).decode("UTF-8")
            # If length of msg is 0, a timeout has occurred with no data received
            if len(msg) == 0:
                serial_timout_occurred = True
                continue

            # Time stamp when data was received
            logtime = datetime.now().strftime('%H:%M:%S.%f')[:-3]

            # Update message data type for printing based on drop down
            msg = type(tab).update_msg_datatype(tab.data_types_dd.get(), msg)
            
            # Check if a timeout has occurred, print to new line
            if serial_timout_occurred == True:

                #Check if timestamp is required. Append to message
                if (tab.timestamp_flag.get() == True):
                    type(tab).print_to_terminal(tab, '\n' + logtime + " :\t\tRX: " + msg)

                else:
                    type(tab).print_to_terminal(tab, '\n' + "RX: " + msg)

                # Log data if required. Check that empty messages dont get logged
                curr_logfile = tab.settings.logger.file_obj
                if ((curr_logfile != None) & (log_msg != '')):
                    # Write to file
                    tab.settings.logger.write_row_csv([logtime,"RX",log_msg])    

                    # Reset log_msg
                    log_msg = ''

                # Reset timeout flag
                serial_timout_occurred = False

            else:
                
                # Print to terminal. If no timeout occurs, then
                # messages should be written to same line
                type(tab).print_to_terminal(tab, msg)           
                log_msg += msg
                
        return True


    '''
    Function Description: Prints string to globally defined scroll terminal object
    Auto scrolls to end of the box if user scrolls down. Else stays at same position.

    Parameters:     tab - Instance of terminal_tab 
                    msg - string to print to terminal 

    Return: void
    '''
    @classmethod
    def print_to_terminal(cls, tab, msg):

        # Enable editing of text box
        tab.terminal_box.config(state="normal")

        tab.terminal_box.insert(END, msg)
        
        # Check if user is looking at previous printed data
        # If not, autoscroll to latest data, else maintain 
        # current y position
        if tab.terminal_box.yview()[1] >= 0.9:  
            # Reset position index to have messages scroll down
            tab.terminal_box.see('end')

        # Disable editing of text box
        tab.terminal_box.config(state="disabled")
        return

    '''
    Function Description: Clears scroll terminal screen

    Parameters: tab - Instance of terminal_tab  

    Return: void
    '''
    @classmethod
    def clear_button_pressed(cls, tab):

        # Enable editing of text box
        tab.terminal_box.config(state="normal")
        # Delete all text in display
        tab.terminal_box.delete("1.0",END)
        # Disable editing of text box
        tab.terminal_box.config(state="disabled")
        return
