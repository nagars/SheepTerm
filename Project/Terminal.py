'''Generic Modules'''
from tkinter import *                # Import tkinter modules used to generate GUI

import json     # Import json module
import os       # For directory manipulation

'''Custom Modules'''
import objects_ui   # custom library built to handle common UI objects
import csvlogger as log    # custom library for logging data to .csv file
import tabs_ui      # custom library built to handle tabs

'''
Global Variables
'''
g_tab_list = []    # Store all the tabs currently active
g_curr_tab_index = 0

theme_dir_path = ".theme"   # Saves the folder and file to store theme settings in
theme_file_path = theme_dir_path + "/theme.json"


def confirm_tabname(tab_window, new_tab_name, event=None):

    # Update global tab name
    global g_tab_name
    g_tab_name = new_tab_name

    # Set confirm tab flag
    global g_add_tab_flag
    g_add_tab_flag = TRUE

    # Close the window
    tab_window.destroy()

    return

def create_tabname_window(default_tabname : str):

    global g_tab_name
    g_tab_name = default_tabname

    global g_add_tab_flag
    g_add_tab_flag = FALSE

    # Create new window over the main window
    tab_window = Toplevel()
    tab_window.geometry("400x100")
    tab_window.resizable(width=False, height=False)
    tab_window.title("New Tab")
    #window.eval(f'tk::PlaceWindow {str(tab_window)} center')

    # Disabled access to main terminal window
    tab_window.grab_set()
    tab_window.focus()
    # Install window close routine
    tab_window.protocol("WM_DELETE_WINDOW",tab_window.destroy)

    # Create new frames
    frame0 = objects_ui.define_frame(tab_window, 0, 0)
    frame0.grid(sticky=NW)
    frame1 = objects_ui.define_frame(tab_window, 0, 1)
    frame1.grid(sticky=NW)

    # Create a text box to add the name into. Autmatically has default name
    tab_name_textbox = objects_ui.define_entry_textbox(frame0, 0, 0, 47)
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
Function Description: Creates an instance of terminal_tab class
and adds it to the notebook

Parameters: notebook - Notebook to add tab too

Return: tab object
'''
def add_tab():

    # Return index number of current tab
    #curr_index = len(g_tab_list)

    # Append index to name
    global g_curr_tab_index
    g_curr_tab_index += 1
    default_tab_name = "Tab" + str(g_curr_tab_index)

    # Create window to change tab name
    tab_window = create_tabname_window(default_tab_name)

    # Wait for the tab name window to close
    window.wait_window(tab_window)

    # Check if confirm button was pressed or if cancel was pressed
    if g_add_tab_flag == TRUE:
    
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
Function Description:  Deletes the tab from the notebook

Parameters: notebook - Notebook to delete tab from
            tab - terminal_tab to remove 

Return: void
'''
def delete_tab():
    
    # Return current tab
    tab = g_tab_list[terminal_notebook.index(terminal_notebook.select())]

    # Close the tab
    tab.close_tab()

    # Remove from global list of tabs
    g_tab_list.remove(tab)

    # Remove to notebook
    terminal_notebook.forget(tab.tab_frame)

    return

def edit_tabname():

    # Get current tab handler
    curr_tab = terminal_notebook.index("current")

    # Get current tab name
    curr_tabname = terminal_notebook.tab(terminal_notebook.select(), "text")

    # Create window to change tab name
    tab_window = create_tabname_window(curr_tabname)

    # Wait for the tab name window to close
    window.wait_window(tab_window)

    # Modify name of tab
    terminal_notebook.tab(curr_tab, text= g_tab_name)

    return

'''
Function Description: Create a custom menu bar with options

Parameters: container - Window to generate menu for

Return: Instance of menubar
'''
def create_menubar():

    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    tab_menu = Menu(menu_bar)
    theme_menu = Menu(menu_bar)
    
    menu_bar.add_cascade(label="Tab", menu=tab_menu)
    tab_menu.add_command(label="Add Tab", command=lambda: add_tab())
    tab_menu.add_command(label="Edit Name", command=lambda: edit_tabname())
    tab_menu.add_command(label="Remove Tab", command=lambda: delete_tab())

    menu_bar.add_cascade(label="Theme", menu=theme_menu)
    theme_menu.add_command(label="Default", command=lambda: set_theme("superhero"))
    theme_menu.add_command(label="Dark", command=lambda: set_theme("darkly"))
    theme_menu.add_command(label="Light", command=lambda: set_theme("journal"))

    return menu_bar


'''
Function Description: Terminates window and all tabs

Parameters: void

Return: void
'''
def close_window():

    # Loop through all tabs and close each one
    for i in range(len(g_tab_list)):
        g_tab_list[i].close_tab()

    # Terminate window
    window.destroy()
    return


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
window = objects_ui.define_window("superhero")
# Define window size
window.geometry('1150x700')
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

# Create the default tab
g_tab_list.append(tabs_ui.terminal_tab(window, terminal_notebook, "Tab0"))
terminal_notebook.add(g_tab_list[0].tab_frame, text=g_tab_list[g_curr_tab_index].name)

# Bind Enter key to send button of default tab
window.bind("<Return>", lambda event=None: tabs_ui.terminal_tab.send_button_pressed(g_tab_list[0]))

# Re-bind enter key to send button of new tab in focus using a function called on tab change
# terminal_notebook.select() returns handle of current tab frame
# terminal_notebook.index() returns an index number of the handle
# Index number corresponds to its position int he g_tab_list global array of tabs
terminal_notebook.bind("<Return>", lambda event=None: tabs_ui.terminal_tab.send_button_pressed(
                        g_tab_list[terminal_notebook.index(terminal_notebook.select())]))

# Change icon of the window
window.iconbitmap("ShaunTheSheep.ico")

'''
Main loop
'''
# Install window close routine
window.protocol("WM_DELETE_WINDOW",close_window)
window.mainloop()

