## Project Summary

This project involves the design of a Python script to create a GUI based serial port terminal on windows. Primary use case is for USB to TTL converters.

## Inspiration

I use serial terminals a lot, both in my job and my personal projects. At the time I wanted to get a little exposure to Python so I decided to start this project while making my way through the Python [tutorial](https://docs.python.org/3/tutorial/).

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

## Development Environment
1. Software:
      1. OS: Windows 11
      2. Python version: 3.10
      3. Virtual COM: Electronic.us Virtual Serial Port Driver. Version: 10
      4. VSCode version: 1.75
      5. VSCode Python Extension version: 2023.3.10531009
      6. pyserial version: 3.5

4. Hardware:
      1. USB to TTL Converter: CP2102
