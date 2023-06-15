'''Generic Modules'''
from tkinter import *      # Import tkinter modules used to generate GUI

import json     # Import json module
import os       # For directory manipulation

'''Custom Modules'''
import objects_ui           # custom library built to handle common UI objects
import tabs_ui              # custom library built to handle tabs

'''
Global Variables
'''
g_tab_list = []         # Stores all the tabs currently active
g_curr_tab_index = 0    # Stores current index of created tab names

settings_dir_path = ".settings"   # Saves the folder and file to store settings in
theme_file_path = settings_dir_path + "/theme.json" # Theme settings
config_file_path = settings_dir_path + "/config.json"   # Tab configuration settings

default_theme = "superhero" # Sets the default theme to startup with

'''
Functions for New / Edit tab window
'''

'''
Function Description: Called when user confirms new name of tab
in the tab name window by clicking confirm button

Parameters: tab_window - Container for confirm button
new_tab_name - Tab name written into text box

Return: None
'''
def confirm_tabname(tab_window, new_tab_name : str, event=None):

    global g_tab_name       # Tracks current tab name
    global g_add_tab_flag   # Tracks if new tab is to be added or not

    # Update global tab name
    g_tab_name = new_tab_name

    # Set confirm tab flag
    g_add_tab_flag = TRUE

    # Close the window
    tab_window.destroy()

    return

'''
Function Description: Creates a new window designed to
store a new tab name to either create a new tab or edit
a current tab

Parameters: default_tabname - Name to be written into textbox 
by default when the window is created

Return: New window
'''
def tabname_window(default_tabname : str):

    global g_tab_name       # Tracks current tab name
    global g_add_tab_flag   # Tracks if new tab is to be added or not
    
    # Update global tab name variable
    g_tab_name = default_tabname
    # Reset create new tab flag
    g_add_tab_flag = FALSE

    # Create new window over the main window
    tab_window = Toplevel()
    #tab_window.geometry("400x100")
    tab_window.resizable(width=False, height=False)
    tab_window.title("New Tab")

    # Disabled access to main terminal window
    tab_window.grab_set()
    # Change focus to new window
    tab_window.focus()
    # Install window close routine
    tab_window.protocol("WM_DELETE_WINDOW",tab_window.destroy)

    # Create new frames
    frame0 = objects_ui.define_frame(tab_window, 0, 0)
    frame0.grid(sticky=NW)
    frame1 = objects_ui.define_frame(tab_window, 0, 1)
    frame1.grid(sticky=NW)

    # Create a text box to add the name into. Automatically has default name
    tab_name_textbox = objects_ui.define_entry_textbox(frame0, 0, 0, 30)
    tab_name_textbox.grid(sticky=NSEW)
    tab_name_textbox.configure(font=('Times New Roman',11))
    tab_name_textbox.insert(0, g_tab_name)
    tab_name_textbox.focus()
    tab_name_textbox.selection_range(0, END)

    # Create buttons to confirm or cancel
    confirm_button = objects_ui.define_button(frame1, 0, 1, "Confirm",
                               lambda: confirm_tabname(tab_window, tab_name_textbox.get()), 'normal')
    confirm_button.grid(sticky=E)

    cancel_button = objects_ui.define_button(frame1, 1, 1, "Cancel",
                                tab_window.destroy, 'normal')
    cancel_button.grid(sticky=E)

    # Bind enter key to confirm button by default
    tab_window.bind("<Return>", lambda event = None: confirm_button.invoke())
    
    # Bind escape key to close window
    tab_window.bind("<Escape>", lambda event = None: cancel_button.invoke())

    return tab_window


'''
Menu Bar Functions
'''

'''
Function Description: Creates a new tab and appends it to notebook
and global tab array. Changes focus to new tab

Parameters: None

Return: None
'''
def create_tab():

    # Create new instance of tab class
    new_tab = tabs_ui.terminal_tab(window, terminal_notebook, g_tab_name)

    # Add to notebook
    terminal_notebook.add(new_tab.tab_frame, text=g_tab_name)

    # Add this tab to the global list tracking tabs
    g_tab_list.append(new_tab)

    # Change focus to new tab
    terminal_notebook.select((new_tab.tab_frame))

    return

'''
Function Description: Creates an instance of terminal_tab class
and adds it to the notebook

Parameters: None

Return: tab object
'''
def add_tab():

    global g_curr_tab_index     # Stores current index of created tab names

    # Increment index and append to name for new tab
    g_curr_tab_index += 1
    default_tab_name = "Tab" + str(g_curr_tab_index)

    # Create window to change tab name
    tab_window = tabname_window(default_tab_name)

    # Wait for the tab name window to close
    window.wait_window(tab_window)

    # Check if confirm button was pressed or if cancel was pressed
    if g_add_tab_flag == TRUE:
        create_tab()

    return


'''
Function Description:  Deletes the tab from the notebook

Parameters: None

Return: None
'''
def delete_tab():
    
    # Return current selected tab
    tab = g_tab_list[terminal_notebook.index(terminal_notebook.select())]

    # Close the tab
    tab.close_tab()

    # Remove from global list of tabs
    g_tab_list.remove(tab)

    # Remove from notebook
    terminal_notebook.forget(tab.tab_frame)

    return

'''
Function Description: Edit the current tab name

Parameters: None

Return: None
'''
def edit_tabname():

    # Get current tab index
    curr_tab_index = terminal_notebook.index("current")

    # Get current tab name
    curr_tabname = terminal_notebook.tab(terminal_notebook.select(), "text")

    # Create window to change tab name
    tab_window = tabname_window(curr_tabname)

    # Wait for the tab name window to close
    window.wait_window(tab_window)

    # Modify name of tab in notebook
    terminal_notebook.tab(curr_tab_index, text=g_tab_name)

    # Modify name in tab object
    g_tab_list[curr_tab_index].name = g_tab_name
    
    return

'''
Function Description: Create a custom menu bar with options

Parameters: None

Return: Instance of menubar
'''
def create_menubar():

    # Create a new menu bar
    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    # Create sub menus
    tab_menu = Menu(menu_bar)
    theme_menu = Menu(menu_bar)
    
    # Label sub menus and assign commands
    menu_bar.add_cascade(label="Tab", menu=tab_menu)
    tab_menu.add_command(label="Add Tab", command=lambda: add_tab())
    tab_menu.add_command(label="Edit Tab Name", command=lambda: edit_tabname())
    tab_menu.add_command(label="Remove Tab", command=lambda: delete_tab())
    tab_menu.add_command(label="Clear Settings", command=lambda: clear_settings())

    menu_bar.add_cascade(label="Theme", menu=theme_menu)
    theme_menu.add_command(label="Default", command=lambda: set_theme(default_theme))
    theme_menu.add_command(label="Dark", command=lambda: set_theme("darkly"))
    theme_menu.add_command(label="Light", command=lambda: set_theme("journal"))

    return menu_bar


'''
Function Description: Terminates window, saves configruations
and closes all tabs

Parameters: void

Return: void
'''
def close_window():

    # Save tab configuration
    save_tabs()

    # Loop through all tabs and close each one
    for i in range(len(g_tab_list)):
        g_tab_list[i].close_tab()

    # Terminate window
    window.destroy()
    return

'''
Tab configuration Functions
'''

'''
Function Description: Save the provided dictionary
to a json file. Create a new file if non existent

Parameters: data - Dictionary to save

Return: None
'''
def save_config(data):
    
    # Check if the settings hidden folder exists
    if os.path.isdir(settings_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(settings_dir_path)

    # Write to file
    with open(config_file_path, 'w') as json_file:
        json.dump(data, json_file)

    return

'''
Function Description: Load a dictionary of data
from a json file. Create a json file with
default data if non existent

Parameters: None

Return: data - dictionary data
'''
def load_config():

    # Check if the settings hidden folder exists
    if os.path.isdir(settings_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(settings_dir_path)

    # Check if the config json file exists
    if os.path.isfile(config_file_path):
        # If yes, open and read it into a dictionary
        with open(config_file_path, 'r') as f:
            data = json.load(f)
    
    else:
        # If not, create one and set the default tab configurations
        data = {
                "tab_index" : 0,
                "tab_names" : ["Tab0"]
                }
        # Save default dictionary to json file
        save_config(data)

    return data

'''
Function Description: Save current configuration of tabs

Parameters: None

Return: None
'''
def save_tabs():

    # Save a list of all active tab names
    tab_name = list()
    for i in range(len(g_tab_list)):
        tab_name.append(g_tab_list[i].name)

    # Create a dictionary with current tab index and names
    data = {
            "tab_index" : g_curr_tab_index,
            "tab_names"  : tab_name
    }

    # Save to json file
    save_config(data)

    return

'''
Function Description: Create tabs based on previous session
configuration data

Parameters: None

Return: None
'''
def setup_tabs():

    # Load tab index and names from json file
    data = load_config()

    # Set global tab index. Used to number future tabs
    global g_curr_tab_index
    g_curr_tab_index = data.get("tab_index")

    # Get list of tab names
    tab_names = list()
    tab_names = data.get("tab_names")

    global g_tab_name
    # For every tab name in list, create a new tab
    for i in range(len(tab_names)):
        g_tab_name = tab_names[i]
        create_tab()

    return

'''
Theme Functions
'''

'''
Function Description: Saves current theme to json file

Parameters: theme - string with theme name

Return: None
'''
def save_theme(theme: str):

    # Check if the settings hidden folder exists
    if os.path.isdir(settings_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(settings_dir_path)

    # Write to file
    with open(theme_file_path, 'w') as json_file:
        json.dump({"theme":theme}, json_file)
    
    return

'''
Function Description: Load theme from json file

Parameters: None

Return: None
'''
def load_theme():

    # Check if the theme hidden folder exists
    if os.path.isdir(settings_dir_path) == FALSE:
        # Create it if it doesnt exist
        os.mkdir(settings_dir_path)

    # Check if the theme json file exists
    if os.path.isfile(theme_file_path):
        # If yes, open and read it
        with open(theme_file_path, 'r') as f:
            data = json.load(f)
            saved_theme = data.get("theme")
    else:
        # If not, create one and set the default theme
        saved_theme = default_theme
        save_theme(saved_theme)

    return saved_theme

'''
Function Description: Sets the theme of curretn session
based on given parameter or theme json file

Parameters: term_theme - Theme name

Return: None
'''
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
Function Description: Clears the current theme 
to the default theme

Parameters: None

Return: None
'''
def clear_settings():

    global g_tab_name       # Tracks current tab name
    global g_curr_tab_index # Tracks index of created tabs
    
    # Delete all tabs
    for i in range(len(g_tab_list)):
        delete_tab()

    # Reset global tab index and tab name
    g_curr_tab_index = 0
    g_tab_name = "Tab0"

    # Create a new tab
    create_tab()

    # Set theme to default
    set_theme(default_theme)
    
    return

'''
Function Description: Changes enter key binding and focus to 
widgets in current tab

Parameters: None

Return: None
'''
def set_widget_focus():

    # Check that there is at least 1 active tab open
    if len(g_tab_list) == 0:
        return

    # terminal_notebook.select() returns handle of current tab frame
    # terminal_notebook.index() returns an index number of the handle
    # Index number corresponds to its position int he g_tab_list global array of tabs
    # Current tab
    curr_tab = g_tab_list[terminal_notebook.index(terminal_notebook.select())]

    # Binds the enter key to send button of the current tab
    window.bind("<Return>", lambda event=None: tabs_ui.terminal_tab.
                send_button_pressed(curr_tab))

    # Changes focus to the send message box of the current tab
    curr_tab.terminal_box.focus()

    return

'''
Frame Definitions
'''
# Generate GUI window
window = objects_ui.define_window(default_theme)
# Define window size
window.geometry('1470x600')
# Set title for window
window.title("Sheep-Term")
#Ensure display frame expands with window
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# Create the notebook for the terminal frame
terminal_notebook = objects_ui.define_notebook(window)
terminal_notebook.grid(sticky=NSEW)

# Create a menu Bar
menu_bar = create_menubar()

# Set previously saved theme
set_theme()

# Setup tab configuration
setup_tabs()

# Bind Enter key to send button of default tab
window.bind("<Return>", lambda event=None: tabs_ui.terminal_tab.send_button_pressed(g_tab_list[0]))

# Re-bind enter key to button of new tab in focus using a function called on tab change
terminal_notebook.bind("<<NotebookTabChanged>>", lambda event=None: set_widget_focus())

# Change icon of the window
window.iconbitmap("ShaunTheSheep.ico")

# Install window close routine
window.protocol("WM_DELETE_WINDOW",close_window)

'''
Main loop
'''
window.mainloop()

