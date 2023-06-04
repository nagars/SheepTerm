import csv      # Import csv file to write to .csv log file
from tkinter.filedialog import asksaveasfile # Import tkinter file save module


class csvlogger_class:
    def __init__(self) -> None:

        '''
        Public Objects
        '''
        self.file_obj = None    # Object is assigned a file pointer to the csv file
        
        '''
        Private Objects
        '''
        self.__writer_obj = None  # Object is assigned a csv writer object to csv file

    '''
    Public Functions
    '''    

    '''
    Function Description: Triggers the save file prompt to save a
    .csv file for logging. Opens a writer object to the file.

    Parameters: filename - name of file to save. Defaults to 'csvlog'
                delim - .csv delimiter. Defaults to ','
            
    Return: Writer object
    '''
    def create_csv(self, filename = 'csvlog', delim = ','):
        
        # Call save file dialog and return object to file
        self.file_obj =  asksaveasfile(initialfile = filename, mode='w+',
            defaultextension=".csv", filetypes=[(".csv", "*.csv")])

        # Check that a file was saved successfully
        if self.file_obj is None:
            return False

        # Return object to csv writer
        self.__writer_obj = csv.writer(self.file_obj, delimiter = delim)
    
        return self.file_obj

    '''
    Function Description: Writes list to current open writer object

    Parameters: print_list - list of elements to write to .csv

    Return: True on success / False on failure
    '''
    def write_row_csv(self, print_list):
        
        # Check if ___writer_obj is defined
        # Implying that create_csv was called successfully
        if self.__writer_obj is None:
            return False

        # Check that a file was saved successfully
        if self.file_obj is None:
            return False

        self.__writer_obj.writerow(print_list)
        return True


    '''
    Function Description: Closes the writer object

    Parameters: void

    Return: True on success / False on failure
    '''
    def close_csv(self):
        
        # Check if ___writer_obj is defined
        # Implying that create_csv was called
        if self.__writer_obj is None:
            return False
        
        # Check that a file was saved successfully
        if self.file_obj is None:
            return False
        
        self.file_obj.close()
        return True

