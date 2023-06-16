import serial  # Import pyserial library
from serial.serialutil import STOPBITS_ONE_POINT_FIVE       
from serial import SerialException  # Import pyserial exception handling

minimum_timeout = 0.01  # Is set when the user requests a timeout of 0s

'''
Functions
'''

'''
Function Description: open com port to USBtoTTL converter
with default settings unless specified otherwise

Parameters: com_port - com port name to open
            baud - baud rate (default 9600)
            bytes_size = size of each packet (default 8)
            timeout - wait time for new packets during reception (default 2 sec)
            stop_bits - number of stop bits (default one)
            parity_bits - parity (default none)

Return - serial port, else false
'''
def open_serial_com(com_port, baud = 9600, bytes_size = 8, time_out = 2, stop_bits = serial.STOPBITS_ONE, 
                    parity_bit = serial.PARITY_NONE):

    # Ensure a com port was selected
    if(com_port == ''):
        return False

    # Check timeout
    if(time_out == 0.0):
        time_out = minimum_timeout

    # Open selected com port with default parameters. Returned port handle is set as global variable
    try:
        serial_port = serial.Serial(port = com_port, baudrate = baud, bytesize = bytes_size, timeout = time_out, 
                                    stopbits = stop_bits, parity = parity_bit)
    # Check if COM port failed to open. Return failure value
    except SerialException:
        return False

    # Check for incorrect input value
    except ValueError:
        return False

    # Flush the port
    serial_port.flush()

    return serial_port

'''
Function Description: Writes to serial port

Parameters: void

Return: Number of bytes written to serial port/ False if serial port
        is not initialised
'''
def write_serial_com(serial_port, data):
    
    # Check that serial port is still valid
    if(False == check_serial_port_status(serial_port)):
        return False

    return serial_port.write(data.encode())

'''
Function Description: Returns data read from serial
port

Parameters: size - Number of bytes to read. Defaults to 1 byte

Return: Bytes read from serial port
'''
def read_serial_com(serial_port, size=1):

    # Check that serial port is still valid
    if(False == check_serial_port_status(serial_port)):
        return False

    return serial_port.read(size)

'''
Function Description: Closes serial port if
a it is open. 

Parameters: void

Return: False if serial port is not open / 
        True on successful closure
'''
def close_serial_com(serial_port):

    # Check that serial port is still valid
    if(False == check_serial_port_status(serial_port)):
        return False

    # Close serial port
    serial_port.close()

    return True

'''
Function Description: Aborts current serial read

Parameters: void

Return: void
'''
def abort_serial_read(serial_port):
    
    # Check that serial port is still valid
    if(False == check_serial_port_status(serial_port)):
        return False

    serial_port.cancel_read()
    return

'''
Function Description: Checks if serial port is open

Parameters: void

Return: True on success / False on Failure or invalid serial
        port identifier
'''
def check_serial_port_status(serial_port):

    # Check if serial_port is defined
    # Implying that open_serial_com was called
    if serial_port is None:
        return False
    
    # Variable is valid
    else:
        return serial_port.isOpen()
