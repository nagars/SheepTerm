import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

'''
Functions
'''
"""
def print_to_terminal(terminal_box,msg):
    terminal_box.insert(END, msg)
    terminal_box.insert(END, '\n')

    # Reset position index to have messages scroll down
    terminal_box.yview = END
    return
"""

def open_serial_com(com_port):
    # Store user selected value
    #com_port_selected = com_ports_menu.get()
    # Extract com port value
    #com_port = com_port_selected[0:4]

    # Ensure a com port was selected
    if(com_port == ''):
        return

    global serial_port
    # Open selected com port with default parameters. Returned port handle is set as global variable
    try:
        serial_port = serial.Serial(port=com_port, baudrate=9600,
                                    bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE,
                                    parity=serial.PARITY_NONE)
    # Check if COM port failed to open. Return failure value
    except SerialException:
        return -1

    return 0


def close_serial_com(com_port):

    return 0


def com_port_param_window():

    #Create new window

    #Generate frames and UI objects

    return 0


def set_com_port_param():


    return 0