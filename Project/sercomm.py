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

Return - True on success, False on failure
'''
def open_serial_com(com_port, baud = 9600, bytes_size = 8, time_out = 2, stop_bits = serial.STOPBITS_ONE, 
                    parity_bit = serial.PARITY_NONE):

    # Ensure a com port was selected
    if(com_port == ''):
        return False

    global g_serial_port
    # Open selected com port with default parameters. Returned port handle is set as global variable
    try:
        g_serial_port = serial.Serial(port = com_port, baudrate = baud, bytesize = bytes_size, timeout = time_out, 
                                    stopbits = stop_bits, parity = parity_bit)
    # Check if COM port failed to open. Return failure value
    except SerialException:
        return False

    # Check for incorrect input value
    except ValueError:
        return False

    # Flush the port
    g_serial_port.flush()

    return True

'''
Function Description: Writes to serial port

Parameters: void

Return: Nummber of bytes written to serial port
'''
def write_serial_com(data):
    
    return g_serial_port.write(data.encode())

'''
Function Description: Returns data read from serial
port

Parameters: size - Number of bytes to read. Defaults to 1 byte

Return: Bytes read from serial port
'''
def read_serial_com(size=1):
    
    return g_serial_port.read(size)

'''
Function Description: Closes serial port if
a it is open. 

Parameters: void

Return: False if serial port is not open / 
        True on successful closure
'''
def close_serial_com():

    # Check if g_serial_port is defined
    # Implying that open_serial_com was called
    try: g_serial_port
    except NameError: 
       return False

    # Close serial port
    g_serial_port.close()

    return True

'''
Function Description: Aborts current serial read

Parameters: void

Return: void
'''
def abort_serial_read():
    
    # Check if g_serial_port is defined
    # Implying that open_serial_com was called
    try: g_serial_port
    except NameError: 
       return False
    
    g_serial_port.cancel_read()
    return

'''
Function Description: Checks if serial port is open

Parameters: void

Return: True on success / False on Failure or invalid serial
        port identifier
'''
def check_serial_port_status():

    # Check if g_serial_port is defined
    # Implying that open_serial_com was called
    try: g_serial_port
    except NameError: 
       return False
    
    return g_serial_port.isOpen()
