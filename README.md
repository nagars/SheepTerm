## Project Summary

This project involves the design of a Python script to create a GUI based serial port terminal on windows. Primary use case is for USB to TTL converters.

## Inspiration

I use serial terminals a lot, both in my job and my personal projects. I wanted to get a little exposure to Python so I decided to start this project while making my way through the Python [tutorial](https://docs.python.org/3/tutorial/). It's been a fun journey. If you're just stopping by or want to seriously try it out, any feedback is appreciated!

## Current UI Layout (Dark Theme)

![Screenshot 2023-06-16 190746](https://github.com/nagars/SheepTerm/assets/25108047/7450d574-86ae-4e9f-ae3d-cb03accbfdb0)
![Screenshot 2023-06-16 210315](https://github.com/nagars/SheepTerm/assets/25108047/f3804a33-94a6-40c6-97d6-2eb5453efb07)

## Feature List

I have attempted to keep the features both comprehensive and still inline with the [KISS](https://www.interaction-design.org/literature/topics/keep-it-simple-stupid#:~:text=202%20shares-,What%20is%20Keep%20It%20Simple%2C%20Stupid%20(KISS)%3F,of%20user%20acceptance%20and%20interaction.) school of thought.

1. Shall open a GUI based terminal
2. Shall allow timestamping of incoming and outgoing messages
3. Shall allow the appending of CR and NL characters if required by the user
4. Shall list all available serial ports
5. Shall return success / failure messages when opening / configuring a port
6. Shall give the user the ability to configure default serial port parameters
7. Shall auto scroll messages in the terminal
8. Shall allow the user to select a .csv log file to log session data in
9. Shall allow the messages to be displayed as hex, binary, integers or strings
10. Shall allow the user to configure serial port parameters during an active session
11. Shall allow the user to open multiple unique serial ports through tabs
12. Shall allow the user to set the theme of appearence
13. Shall remember the theme and tab configuration from a previous session

## Project File Structure
**|-- Terminal.py**    : The main script file. Generates the UI and calls other modules <br />
**|** <br />
**|-- tabs_ui.py**     : Defines the class and associated functions for the tabs <br />
**|** <br />
**|-- settings_ui.py** : Defines the sercom settings class, window and associated functions <br />
**|** <br />
**|-- objects_ui.py**  : Defines various widgets like buttons, drop downs etc used across the project <br />
**|** <br />
**|-- csvlogger.py**   : Defines the csv log class and associated functions used for logging <br />
**|** <br />
**|-- sercomm.py**     : Defines various functions to interact with the pyserial api <br />
**|** <br />
**|-- ShaunTheSheep.ico** : Image to set as the icon of the terminal <br />

## Development Environment

1. Software Used:
      1. OS: Windows 11
      2. Python version: 3.10
      3. Null-modem emulator - [com0com](https://com0com.sourceforge.net/) version: 2.2.2.0-fre-signed
      4. VSCode version: 1.75
      5. VSCode Python Extension version: 2023.3.10531009
      6. pyserial version: 3.5
      7. tkinter version: 8.6

2. Hardware Hardware:
      1. Intel i5 x64 host computer    
      2. USB to TTL Converter: CP2102 with TX and RX shorted

## UI Breakdown

The UI can be broken down into 7 major components:
1. The Main Window
2. The Menu Bar
3. Notebook / Tabs
4. Frames  
5. Widgets
6. Auxiliary Windows
7. Logger

### The Main Window

The main window is generated using python's [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/) (An abstraction on the well known tkinter). Includes:
1. The menu bar with various options for themes, settings and tabs. 
2. The notebook which all the individual tabs are a part of. 

### The Menu Bar

The [menu bar](https://pythonspot.com/tk-menubar/) sits at the top of the notebook. It contains various options to change the appearence of tabs and the terminal in general.

![image](https://github.com/nagars/SheepTerm/assets/25108047/fda0938f-f411-4f38-b625-e0eaad9dc453)
![image](https://github.com/nagars/SheepTerm/assets/25108047/b9f7637b-e3a6-48c1-8516-53729c53ae90)

### The Notebook

A [notebook](https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/notebook.html) is a tkinter widget that supports tabs. There is one notebook in this terminal. It contains completely isolated unique tabs. Each tab can connect to a serial port and operate enitrely unaffected by the addition / removal of other tabs. Each tab maintains its own serial settings, csv log files and so on.

Each tab is further defined through frames. 

### Frames

[Frames](https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/frame.html) are tkinter widgets that allow one to split the window into unique sections that can be assigned unique formats, settings, widgets, positions etc.
This project contains 4 frames:

1. Com Frame
2. Config Frame
3. Display Frame
4. Display Button Frame

I chose this configuration based on ease of re-configuration of the terminals UI, space utilisation and widget justification and placement. Refer to previous project milestons section below.

![Untitled](https://github.com/nagars/SheepTerm/assets/25108047/2262626d-bc09-4324-a504-700167667412)

### Widgets

[Widgets](https://tkdocs.com/tutorial/widgets.html) are tkinter objects that form the basic UI. These include buttons, labels (Text), drop downs and so forth. I played around with a variety of widgets before settling on a mix of widgets that were both intuitive and had a good appearence (In my humble opinion). Find example screenshots and descriptions below:

1. **Com Label + Com Name Drop Down:** <br /><br />Names all available serial port. Device descriptions are appended to the names if available.

![image](https://github.com/nagars/SheepTerm/assets/25108047/d4f14265-0b73-43ca-a665-586a3df712d2)

2. **Display Type Drop Down + Config Check Button**: <br /><br /> Names all possible display formats. Checkbuttons enable / disable timestamps and echo of data being sent. Additional checkbutton append '\n' and '\r' to the message being sent.

![image](https://github.com/nagars/SheepTerm/assets/25108047/e47d7bb9-1487-4167-923c-42265e627ad0)

3. **Terminal Display Operation Examples:**

      1. Timestamps Disabled
![image](https://github.com/nagars/SheepTerm/assets/25108047/e739ddb3-c33a-4ccf-98a2-3aa6a4320f70)

      2. Timestamps Enabled
![image](https://github.com/nagars/SheepTerm/assets/25108047/87f32215-9ce6-4cdd-9d95-3cb0f313b3a8)

      3. Echo Enabled ( Transmitted Message is echoed back to terminal )
![image](https://github.com/nagars/SheepTerm/assets/25108047/38a42f80-a1bd-4acd-8b79-f529065d236c)

### Auxiliary Windows

Apart from the main window, there are 2 additional windows that can be generated:

1. **Tab name window** - This window is generated when the user attempts to add a new tab or edit the name of a current tab. It allows the user to enter the new name or simply accept a default name based on the number of previously opened tabs

![image](https://github.com/nagars/SheepTerm/assets/25108047/0bcd4c0e-2148-4dca-b5bc-e2f2d33a0e44)

2. **Serial settings window** - This window is generated when the user attempts to change the serial settings of a particular tab or to enable logging of data to a .csv file. 

![image](https://github.com/nagars/SheepTerm/assets/25108047/40e2ee95-faf7-4af0-a252-b6298b4bc8cb)

### Logger

Finally, the csv logger can be enabled through the serial settings window. An example of a .csv generated during a simple test is shown below. Note changing the display datatype in the terminal dynamically changes the format in which it is logged into the .csv file.

![image](https://github.com/nagars/SheepTerm/assets/25108047/5e67f3b7-6a10-4484-8795-e55e02f5d17b)

## References

1. pyserial API               - [link](https://pythonhosted.org/pyserial/pyserial_api.html)
2. tkinter documentation      - [link](https://docs.python.org/3/library/tkinter.html)
3. tkinter's youtube channel  - [link](https://www.youtube.com/@TkinterPython)
4. codemy.com's tkinter playlist - [link](https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV)
5. com0com readme             - [link](https://com0com.sourceforge.net/com0com/ReadMe.txt)
6. ttkbootstrap               - [link](https://ttkbootstrap.readthedocs.io/en/latest/)

## Additional Notes:

### Testing with Virtual COM ports

My initial plan was to do a simple loopback with the CP2102 however, it very quickly became apparent that my module was defective. Thats what I get for going cheap on amazon :)
Being impatient as I am, I decided to look into virtual com ports on Windows. In walks com0com. With a few simple commands, one can link two virtual com ports. In the beginning I opened one com port with my serial terminal and the other with Putty. Eventually once I added tabs, I connected one tab to each com port. Simple, straight forward and easy to configure. God bless the open source community.

Note: By default com0com installs 2 ports named CNCA0 and CNCB0. Remember to change their name to our familiar 'COM*' using the "change" command. Refer to the FAQ in the readme file linked below.

Note: I found that pyserial doesn't see this virtual com ports as available. However, hardcoding a virtual com port name into my script worked just fine.

## Previous Project Milestones :)

### First release iteration with tkinter

No tabs, no fancy UI, no ability to remember settings. Just a bare bones serial terminal. And terrible use of space.

![Screenshot 2023-03-22 140829](https://github.com/nagars/SheepTerm/assets/25108047/de0a9541-55ed-40ba-8a90-39a56f9619d0)
![Screenshot 2023-03-22 140947](https://github.com/nagars/SheepTerm/assets/25108047/b3f73d8e-8e83-4fee-b28f-fc652ac633a4)

### Look fancy theme!

Added ttkbootstrap and improved the appearence. Addition of an echo option to see what youre sending. Still terrible use of space.

![Screenshot 2023-03-26 222834](https://github.com/nagars/SheepTerm/assets/25108047/4a9c146e-7b94-4198-9a79-071016950646)

### Did somone mention tabs?

Added a notebook and tabs. No ability to change the number of tabs or remember tab names / configurations still. That use of space though :/

![Screenshot 2023-04-16 010110](https://github.com/nagars/SheepTerm/assets/25108047/6f4d3f7e-2dbd-49fb-bfeb-78ccbb5f8ec4)

