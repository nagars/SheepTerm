from tkinter import scrolledtext        # Import tkinter module for scroll text box
from tkinter import ttk
from tkinter import *                   # Import all tkinter modules

from ttkbootstrap.constants import *    # Import all ttkbootstrap modules
import ttkbootstrap as ttk_b            


'''Functions: Frame Definitions'''

'''
Function Description: Simple abstraction for creating a
tkinter GUI window. 

Parameters: theme - inbuilt theme to use. "darkly" by default.

Return: tkinter window object
'''
def define_window(theme="darkly"):
    return ttk_b.Window(themename=theme)

'''
Function Description: Define a frame for the UI objects

Parameters: container - Main window object
position_y - column index for frame position
position_x - row index for frame position
theme = colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/frame/

Return: frame object
'''
def define_frame(container, position_y, position_x, frame_sticky=None, theme='default'):

    frame = ttk_b.Frame(container, bootstyle=theme)
    frame.grid(column=position_y, row=position_x)
    frame.grid(sticky=frame_sticky)

    return frame

'''Functions: Widget Definitions'''
'''
Function Description: Define a drop down menu UI object

Parameters: container - Main window object
content_list - list of option in the drop down menu
position_y - columnm index for frame position
position_x - row index for frame position
default_state - default option selected by drop down menu
theme - colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/combobox/

Return: drop down object
'''
def define_drop_down(container, position_y, position_x, content_list, default_state = 'normal', theme = 'default'):

    menu = ttk_b.Combobox(container, value=content_list, state=default_state, bootstyle = theme)
    menu.grid(column=position_y, row=position_x, padx=1, pady=1)

    return menu


'''
Function Description: Define a button UI object that can be used to call a function
when selected

Parameters: container - Main window object
position_y - columnm index for frame position
position_x - row index for frame position
text - label for the button
default_state - active / inactive
function_call - callback function triggered when button is pressed
theme - colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/button/

Return: button object
'''
def define_button(container, position_y, position_x, text = '', function_call = None, default_state = 'normal', theme = 'default'):
    
    button = ttk_b.Button(container, text=text, command=function_call, state=default_state, bootstyle=theme)
    button.grid(column=position_y, row=position_x, padx=2, pady=2)

    return button


'''
Function Description: Define a label UI object

Parameters: container - Main window object
text - label text
position_y - columnm index for frame position
position_x - row index for frame position
theme - colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/label/

Return: button object
'''
def define_label(container, position_y, position_x, text = '', theme = 'normal'):

    label = ttk_b.Label(container, text=text, bootstyle=theme)
    label.grid(column=position_y, row=position_x, padx=2, pady=2)
    return label


'''
Function Description: Define a checkbox UI object

Parameters: container - Main window object
position_y - columnm index for frame position
position_x - row index for frame position
text - label text
status_variable - checked / unchecked
function_call - function to call on change of state
default_state - active / inactive
theme - colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/checkbutton/

Return: button object
'''
def define_checkbox(container, position_y, position_x, text = '', status_variable = None, function_call = None, 
                    default_state = 'normal', theme = 'default'):

    checkbox = ttk_b.Checkbutton(container, text=text, variable=status_variable, command=function_call, 
                                 state=default_state, bootstyle=theme)
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
def define_scroll_textbox(container, position_y, position_x, width = None, height = None):

    scrollbox = scrolledtext.ScrolledText(container, width=width, height=height, state="disabled")
    scrollbox.grid(column=position_y, row=position_x, padx=2, pady=2)
    scrollbox.configure(font=("Times New Roman", 10))

    return scrollbox


'''
Function Description: Define textbox to entry data into

Parameters: container - Main window object
width - width of the textbox
position_y - columnm index for frame position
position_x - row index for frame position
default_state - active / inactive
theme - colour scheme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/entry/

Return: entrybox object
'''
def define_entry_textbox(container, position_y, position_x, width, state = 'normal', theme = 'default'):
    entrybox = ttk_b.Entry(container, width=width, state=state, bootstyle=theme)
    entrybox.grid(column=position_y, row=position_x, padx=2, pady=2)
    entrybox.configure(font=("Times New Roman", 10))

    return entrybox


'''
Function Description: Define a radio button UI object

Parameters: container - Main window object
position_y - columnm index for frame position
position_x - row index for frame position
text - label text
status_variable - checked / unchecked
function_call - function to call when change of state occurs
default_state - active / inactive
theme - colour scheme to use

Note: Refer to https://ttkbootstrap.readthedocs.io/en/latest/styleguide/radiobutton/#radio-default

Return: button object
'''
def define_radiobutton(container, position_y, position_x, text = '', status_variable = None, function_call = None, 
                       default_state = 'normal', theme = 'default'):
    
    radiobutton = ttk_b.Radiobutton(container, text=text, variable=status_variable, command=function_call, 
                                    state=default_state, bootstyle=theme)
    radiobutton.grid(column=position_y, row=position_x, padx=2, pady=2)

    return radiobutton


'''
Function Description: Defines a UI notebook for tabs

Parameters: container - Main window object
padding - space around the notebook
theme - ttkbootstrap theme

Note: Refer to https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/notebook.html

Return: Instance of notebook
'''
def define_notebook(container, padding= 10, theme = 'dark'):
    notebook = ttk_b.Notebook(container, bootstyle = theme)
    notebook.grid(pady=padding, padx=padding)

    # Control + Tab selects the next tab
    # Shift + Tab selects the previous tab
    notebook.enable_traversal()

    return notebook