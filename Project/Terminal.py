'''Generic Modules'''
import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI

from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.

from datetime import datetime   # Import system date library
import threading                # Imports python threading module

import json     # Import json module
import os       # For directory manipulation

'''Custom Modules'''
import sercomm      # custom library built to handle communication
import settings_ui  # custom library built to manage the settings window 
import ui_objects   # custom library built to handle common UI objects
import csvlogger as log    # custom library for logging data to .csv file

'''
Global Variables
'''
g_tab_list = []    # Store all the tabs currently active

theme_dir_path = ".theme"   # Saves the folder and file to store theme settings in
theme_file_path = theme_dir_path + "/theme.json"

'''
Classes
'''
class terminal_tab:
    def __init__(self, notebook, tab_name) -> None:

        '''
        Public Objects
        '''
        self.tab_frame = ui_objects.define_frame(notebook,0,0,NSEW)    # Defines the tab for this class instance
        self.tab_frame.columnconfigure(1, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)
        
        self.name = tab_name                    # Tracks the name of this tab
        self.terminate_event_flag = threading.Event() # Object is used to sync receive thread with main loop
        self.receive_thread = None       # Object is assigned the receive thread handle on initialisation

        self.settings = settings_ui.settings_window_class(self.name)    # Instance of settings class

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
        self.com_frame = ui_objects.define_frame(self.tab_frame,0,0,NW)

        # Create Display Configure Frame for checkbox and drop down options
        self.config_frame = ui_objects.define_frame(self.tab_frame, 0, 1, NW)
        
        # Create a Terminal frame to display actual data
        self.display_frame = ui_objects.define_frame(self.tab_frame,1,1,NSEW)
        # Ensure the terminal box expands with the frame
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)

        # Create a boundary frame for the bottom
        self.south_boundary_frame = ui_objects.define_frame(self.tab_frame,0,2,NW)

        '''
        Define COMM frame UI objects
        '''
        # Define a label for com port to be placed near text box
        self.com_port_label = ui_objects.define_label(self.com_frame, 0, 0, "COM PORT")
        self.com_port_label.grid(sticky=NW)
        # List all the available serial ports
        self.com_ports_available = list(port_list.comports())
        # Remove unusable com port options
        # (NULL appended com port names seem to appear. Possibly due to using
        #  virtual com ports?)
        for item in self.com_ports_available:
            print(item)
            if str(item)[0:5] == "NULL_":
                self.com_ports_available.remove(item)
        self.com_ports_available = ["COM8", "COM9"]#REMOVE POST TESTING!@!!!!!!!!!!!!!!!

        # Define the drop down menu for com ports
        self.com_ports_menu = ui_objects.define_drop_down(self.com_frame, 1, 0, self.com_ports_available, 'readonly')
        self.com_ports_menu.grid(sticky=NW)
        # Define Set COM port button
        self.open_com_button = ui_objects.define_button(self.com_frame, 2, 0, "Open Port", lambda: open_com_port(self), 'normal')
        self.open_com_button.grid(sticky=NW)
        # Define a settings button for sercomm settings
        self.settings_button = ui_objects.define_button(self.com_frame, 3, 0, "Settings", 
                                        lambda: open_settings_window(self), 'disabled')
        self.settings_button.grid(sticky=NW)


        '''
        Define config frame UI objects
        '''
        # Define a label for data type drop down
        self.display_type_label = ui_objects.define_label(self.config_frame, 0, 0, "Display Type")
        self.display_type_label.grid(sticky=NW)
        #Create a show timestamp checkbox
        self.timestamp_checkbox = ui_objects.define_checkbox(self.config_frame, 0, 1, "Show Timestamp", 
                            self.timestamp_flag, None, 'normal', 'round-toggle')
        self.timestamp_checkbox.grid(sticky=NW)
        #Generate list of data types
        self.data_types = ["STRING","ASCII","HEX"]
        #Create a drop down menu with different datatypes to represent on terminal
        self.data_types_dd = ui_objects.define_drop_down(self.config_frame, 1,0, self.data_types, 'readonly')
        self.data_types_dd.grid(sticky=NW)
        #Set default value of drop down menu
        self.data_types_dd.current(0)      
        #Create an include next line character checkbox
        self.include_new_line_checkbox = ui_objects.define_checkbox(self.config_frame, 0, 2, "Include New Line Character",
                                                self.include_new_line_flag, None, "normal", 'round-toggle')
        self.include_new_line_checkbox.grid(sticky=NW)
        #Create an include carriage return character checkbox
        self.include_carriage_return_checkbox = ui_objects.define_checkbox(self.config_frame, 0, 3, "Include Carriage Return Character",
                                                self.include_carriage_return_flag, None, "normal", 'round-toggle')
        self.include_carriage_return_checkbox.grid(sticky=NW)
        #Create a echo checkbox
        self.echo_checkbox = ui_objects.define_checkbox(self.config_frame, 0, 4, "Enable Echo",
                                                self.echo_enable_flag, None, "normal", 'round-toggle')
        self.echo_checkbox.grid(sticky=NW)


        '''
        Define Terminal frame UI objects
        '''
        # Create a scroll text box for the terminal
        self.terminal_box = ui_objects.define_scroll_textbox(self.display_frame, 0, 0, 50, 20)
        self.terminal_box.grid(sticky=NSEW)
        self.terminal_box.configure(font=('Times New Roman',13))

        # Create a text box to get the transmit message from user
        self.send_message_textbox = ui_objects.define_entry_textbox(self.display_frame, 0, 1, 47, 'disabled')
        self.send_message_textbox.grid(sticky=NSEW)
        self.send_message_textbox.configure(font=('Times New Roman',13))
        # Create a button to send data on selected port
        self.send_button = ui_objects.define_button(self.display_frame, 1, 1, "Send",
                           lambda:  send_button_pressed(self), 'disabled')
        self.send_button.grid(sticky=NSEW, padx=5, pady=5)
        
        # Create a clear terminal display button
        self.clear_button = ui_objects.define_button(self.display_frame, 1, 0, "Clear", lambda: clear_button_pressed(self), 'normal')
        self.clear_button.grid(sticky=SE, padx=5, pady=5)

        '''
        Define Empty frame UI objects
        '''
        # Define an empty label to act as a spacer for the bottom 
        self.empty_label = ui_objects.define_label(self.south_boundary_frame, 0, 0, "")
        self.empty_label.grid(sticky=NSEW)



'''
Function Description: Opens selected com port
from drop down menu. Creates receive thread if
com port opened successfully. Modifies UI to
represent opened com port.

Parameters: void 

Return: com port name on Success / False on Failure
'''
def open_com_port(tab:terminal_tab):

    # Ensure a com port was selected
    if tab.com_ports_menu.get() == '':
        print_to_terminal(tab, "No COM port selected!\n")
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
        print_to_terminal(tab, com_port + " is busy. Unable to open\n")
        return False

    # Print COM port opened successfully.
    print_to_terminal(tab, com_port + " opened successfully\n")

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
    tab.receive_thread = threading.Thread(target= lambda: receive_thread(tab))
    tab.receive_thread.start()

    return com_port


'''
Function Description: Transmits data in transmit text box
to com port. Clears the send text box

Parameters: void 

Return: void
'''
def send_button_pressed(tab : terminal_tab, event=None):

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
        print_msg = update_msg_datatype(tab.data_types_dd.get(),transmit_msg)
        # Remove the \r and \n characters when printing to terminal and logging
        print_msg = print_msg.strip('\r\n')

        #Check if timestamp is required. Append to message
        if (tab.timestamp_flag.get() == True):
            print_to_terminal(tab,'\n' + logtime + " :\t\tTX: " + print_msg)

        else:
            print_to_terminal(tab,'\n' + "TX: " + print_msg)

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

Parameters: void

Return: True on Success / False on Failure
'''
def open_settings_window(tab : terminal_tab):

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
    window.wait_window(tab.settings.window)

    # Ensure serial port is open successfully
    if sercomm.check_serial_port_status(tab.settings.com_settings.serialport) == True:

        # Once settings are confirmed, 
        # Clear terminate_event flag and start receive thread again
        tab.terminate_event_flag.clear()

        tab.receive_thread = threading.Thread(target= lambda: receive_thread(tab))
        tab.receive_thread.start()

    else:
        print_to_terminal("Port is busy. Unable to open\n")

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

Paramete: msg - string to be converted into string of new data type

Return: New message string
'''
def update_msg_datatype(display_type, msg):
    
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
            
        case _:
            return False
    
    return print_msg


'''
Function Description: Function to be called as separate thread. Receives data
from serial port, logs if required, converts to selected display format
and prints to terminal. Checks if a read timeout has occurred and 
appends new lines + timestamp if required.

Parameters: void

Return: True - Successful / False - Failure
'''
def receive_thread(tab: terminal_tab):

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
        msg = update_msg_datatype(tab.data_types_dd.get(), msg)
        
        # Check if a timeout has occurred, print to new line
        if serial_timout_occurred == True:

            #Check if timestamp is required. Append to message
            if (tab.timestamp_flag.get() == True):
                print_to_terminal(tab, '\n' + logtime + " :\t\tRX: " + msg)

            else:
                print_to_terminal(tab, '\n' + "RX: " + msg)

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
            print_to_terminal(tab, msg)           
            log_msg += msg
            
    return True


'''
Function Description: Prints string to globally defined scroll terminal object
Auto scrolls to end of the box if user scrolls down. Else stays at same position.

Parameters: msg - string to print to terminal 

Return: void
'''
def print_to_terminal(tab : terminal_tab, msg):

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
Function Description: Closes come port, file pointer
to log file (If open) and program.
Ensures recieve_thread terminate gracefully

Parameters: void

Return: void
'''
def close_tab(tab : terminal_tab):

    # Check if the receive thread was started
    # If not, directly terminate program
    # else terminate the thread and then the program 
    if tab.receive_thread is None:
        pass

    else:
        # Set terminate flag for receive thread
        tab.terminate_event_flag.set()

        # Cancel any pending read
        sercomm.abort_serial_read(tab.settings.com_settings.serialport)

        # wait till receive thread is terminated
        tab.receive_thread.join()

    # Close the com port
    sercomm.close_serial_com(tab.settings.com_settings.serialport)

    # Close file pointer for logger
    tab.settings.logger.close_csv()

    return

def close_window():

    # Loop through all tabs and close each one
    for i in range(len(g_tab_list)):
        close_tab(g_tab_list[i])

    # Terminate window
    window.destroy()
    return

'''
Function Description: Clears scroll terminal screen

Parameters: void 

Return: void
'''
def clear_button_pressed(tab: terminal_tab):

    # Enable editing of text box
    tab.terminal_box.config(state="normal")
    # Delete all text in display
    tab.terminal_box.delete("1.0",END)
    # Disable editing of text box
    tab.terminal_box.config(state="disabled")
    return

'''
Menu Bar Functions
'''

def add_tab(notebook):

    # Return index number of current tab
    curr_index = len(g_tab_list)

    # Append index to name
    tab_name = "Tab" + str(curr_index)

    # Create new tab
    create_tab(notebook, tab_name)

    return

def create_tab(notebook, tab_name):

    # Create new instance of tab class
    new_tab = terminal_tab(notebook, tab_name)

    # Add to notebook
    notebook.add(new_tab.tab_frame, text=tab_name)

    # Add this tab to the global list tracking tabs
    g_tab_list.append(new_tab)

    return new_tab


def remove_tab(notebook):

    delete_tab(notebook, g_tab_list[terminal_notebook.index(terminal_notebook.select())])

    return


def delete_tab(notebook, tab: terminal_tab):
    
    # Remove from global list of tabs
    g_tab_list.remove(tab)

    # Remove to notebook
    notebook.forget(tab.tab_frame)

    return


def create_menubar(container):

    menu_bar = Menu(container)
    container.config(menu=menu_bar)

    tab_menu = Menu(menu_bar)
    theme_menu = Menu(menu_bar)
    
    menu_bar.add_cascade(label="Tab", menu=tab_menu)
    tab_menu.add_command(label="Add Tab", command=lambda: add_tab(terminal_notebook))
    tab_menu.add_command(label="Remove Tab", command=lambda: remove_tab(terminal_notebook))

    menu_bar.add_cascade(label="Theme", menu=theme_menu)
    theme_menu.add_command(label="Default", command=lambda: set_theme("superhero"))
    theme_menu.add_command(label="Dark", command=lambda: set_theme("darkly"))
    theme_menu.add_command(label="Light", command=lambda: set_theme("journal"))

    return menu_bar

'''
Theme Functions
'''
def save_theme(theme):

    # Check if the theme hidden folder exists
    if os.path.isdir(theme_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(theme_dir_path)

    # Write to file
    with open(theme_file_path, 'w') as json_file:
        json.dump({"theme":theme}, json_file)
    
    return

def load_theme():

    # Check if the theme hidden folder exists
    if os.path.isdir(theme_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(theme_dir_path)

    # Check if the theme json file exists
    if os.path.isfile(theme_file_path):
        # If yes, open and read it
        with open(theme_file_path, 'r') as f:
            data = json.load(f)
            saved_theme = data.get("theme")
    else:
        # If not, create one and set the default theme
        saved_theme = "superhero"
        save_theme(saved_theme)

    return saved_theme

def set_theme(term_theme = None):

    if term_theme == None:
        # Load theme from the saved file
        term_theme = load_theme()

    # Perform a theme change if required
    window.style.theme_use(term_theme)   

    # Save the latest set theme
    save_theme(term_theme)

    return

'''
Frame Definitions
'''
# Generate GUI window
window = ui_objects.define_window("superhero")
# Define window size
window.geometry('1150x700')
# Set title for window
window.title("Sheep-Term")
#Ensure display frame expands with window
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Create the notebook for the terminal frame
terminal_notebook = ui_objects.define_notebook(window)
terminal_notebook.grid(sticky=NSEW)

# Create a menu Bar
menu_bar = create_menubar(window)

# Create the default tab
create_tab(terminal_notebook, "Tab0")

# Set previously saved theme
set_theme()

# Bind Enter key to send button
#window.bind('<Enter>', send_button_pressed(g_tab_list[terminal_notebook.index(terminal_notebook.select())]))

# Change icon of the window
window.iconbitmap("ShaunTheSheep.ico")

'''
Main loop
'''
# Install window close routine
window.protocol("WM_DELETE_WINDOW",close_window)
window.mainloop()

