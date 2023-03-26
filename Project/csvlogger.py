import csv      # Import csv file to write to .csv log file
from tkinter.filedialog import asksaveasfile # Import tkinter file save module

'''
Global Variables
'''
global g_file_obj       # Object is assigned a file pointer to the csv file
global g_writer_obj     # Object is assigned a csv writer object to csv file

'''
Function Description: Triggers the save file prompt to save a
.csv file for logging. Opens a writer object to the file.

Parameters: filename - name of file to save. Defaults to 'csvlog'
            delim - .csv delimiter. Defaults to ','
        
Return: Writer object
'''
def create_csv(filename = 'csvlog', delim = ','):

    # Call save file dialog and return object to file
    global g_file_obj
    g_file_obj =  asksaveasfile(initialfile = filename, mode='w+',
        defaultextension=".csv", filetypes=[(".csv", "*.csv")])

    # Check that a file was saved successfully
    try: g_file_obj
    except NameError: 
       return False

    # Return object to csv writer
    global g_writer_obj
    g_writer_obj = csv.writer(g_file_obj, delimiter = delim)
    
    return g_file_obj

'''
Function Description: Writes list to current open writer object

Parameters: print_list - list of elements to write to .csv

Return: True on success / False on failure
'''
def write_row_csv(print_list):
    
    # Check if g_writer_obj is defined
    # Implying that create_csv was called
    try: g_writer_obj
    except NameError: 
       return False

    g_writer_obj.writerow(print_list)
    return True

'''
Function Description: Closes the writer object

Parameters: void

Return: True on success / False on failure
'''
def close_csv():
    
    try: g_file_obj
    except NameError:
        return False
    
    g_file_obj.close()
    return True
