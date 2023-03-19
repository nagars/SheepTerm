## Project Summary

This project involves the design of a Python script to create a GUI based serial port terminal on windows. Primary use case is for USB to TTL converters.

## Inspiration

I use serial terminals a lot, both in my job and my personal projects. I wanted to get a little exposure to Python so I decided to start this project while making my way through the Python [tutorial](https://docs.python.org/3/tutorial/). It's been a fun journey. If you're just stopping by or want to seriously try it out, any feedback is appreciated!

## Feature List

1. Shall open a GUI based terminal
2. Shall allow timestamping of incoming and outgoing messages
3. Shall allow the appending of CR and NL characters if required by the user
4. Shall list all available serial ports
5. Shall return success / failure messages when opening / configuring a port
6. Shall give the user the ability to configure default serial port parameters
7. Shall auto scroll messages in the terminal
8. Shall allow the user to select a .csv log file to log session data in
9. Shall allow the messages to be displayed as hex, binary, integers or strings
10. Shall allow a user to configure serial port paramaters during an active session

## Development Environment
1. Software Used:
      1. OS: Windows 11
      2. Python version: 3.10
      3. Null-modem emulator - [com0com](https://com0com.sourceforge.net/) version: 2.2.2.0-fre-signed
      4. VSCode version: 1.75
      5. VSCode Python Extension version: 2023.3.10531009
      6. pyserial version: 3.5
      7. tkinter version: 8.6

4. Hardware Hardware:
      1. USB to TTL Converter: CP2102

## Additional Notes:

### Testing with Virtual COM ports
My initial plan was to do a simple loopback with the CP2102 however, it very quickly became apparent that my module was defective. Thats what I get for going cheap on amazon :)
Being impatient as I am, I decided to look into virtual com ports on Windows. In walks com0com. With a few simple commands, one can link two virtual com ports. I opened one com port with my serial terminal and the other with Putty. Simple, straight forward and easy to configure. God bless the open source community.

Note: By default com0com installs 2 ports named CNCA0 and CNCB0. Remember to change their name to our familiar 'COM*' using the "change" command. Refer to the FAQ in the readme file linked below.

Note: I found that pyserial doesn't see this virtual com ports as available. However, hardcoding a virtual com port name into my script worked just fine.

### References
1. pyserial API               - [link](https://pythonhosted.org/pyserial/pyserial_api.html)
2. tkinter documentation      - [link](https://docs.python.org/3/library/tkinter.html)
3. tkinter's youtube channel  - [link](https://www.youtube.com/@TkinterPython)
3. com0com readme             - [link](https://com0com.sourceforge.net/com0com/ReadMe.txt)
