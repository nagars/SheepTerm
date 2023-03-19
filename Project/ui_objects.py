import tkinter                       # Import tkinter library used to generate GUI
from tkinter import *                # Import tkinter modules used to generate GUI
from tkinter import scrolledtext     # Import tkinter module for scroll text box
from tkinter import ttk

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
    label.grid(column=position_y, row=position_x, padx=2, pady=2)

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
def define_checkbox(container, text, default_state, status_variable, function_call, position_y, position_x):

    checkbox = Checkbutton(container, text=text, variable=status_variable, command=function_call, state=default_state)
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
