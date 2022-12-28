import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
import serial.tools.list_ports as port_list # Import function to list serial ports.
from serial import SerialException  # Import pyserial exception handling

'''
Functions
'''

'''
Function Description: open com port to USBtoTTL converter
with default settings unless specified otherwise

Parameters: com_port - com port to open
baud - baud rate (default 9600)
bytes_size = size of each packet (default 8)
timeout - wait time for new packets during reception (default 2 sec)
stop_bits - number of stop bits (default one)
parity_bits - parity (default none)

return - 0 on success, -1 on failure
'''
def open_serial_com(com_port, baud = 9600, bytes_size = 8, time_out = 2, stop_bits = serial.STOPBITS_ONE, parity_bit = serial.PARITY_NONE):
    # Store user selected value
    #com_port_selected = com_ports_menu.get()
    # Extract com port value
    #com_port = com_port_selected[0:4]

    # Ensure a com port was selected
    if(com_port == ''):
        return -1

    global serial_port
    # Open selected com port with default parameters. Returned port handle is set as global variable
    try:
        #serial_port = serial.Serial(port=com_port, baudrate=9600,
        #                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE,
        #                            parity=serial.PARITY_NONE)
        serial_port = serial.Serial(port = com_port, baudrate = baud, bytesize = bytes_size, timeout = time_out, 
                                    stopbits = stop_bits, parity = parity_bit)
    # Check if COM port failed to open. Return failure value
    except SerialException:
        return -1

    # Check for incorrect input value
    except ValueError:
        return -1

    return 0


def close_serial_com():

    # Check if serial_port is defined
    try: serial_port
    except NameError: 
       return -1

    # Close serial port
    serial_port.close()

    return 0


def com_port_param_window():

    #Create new window

    #Generate frames and UI objects

    return 0


def set_com_port_param():


    return 0