from enum import Enum
from datetime import datetime


class Type(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    def __init__(self, fname: str, verbose: bool = False, overwrite: bool = False):
        """Create a logger that writes log messages to a file
        
        Arguments:
            fname (str)
                The name of the output file
            verbose (bool, optional)
                Output will also be written to the console if verbose is `True`
                (default: `False`)
            overwrite (bool, optional)
                Whether to overwrite the contents of the output file if it
                already exists or to append the messages to the end of the file
                (default: `False`)
        """
        self.fname = fname
        self.verbose = verbose
        self.file = open(fname, 'w' if overwrite else 'a')
    
    def __del__(self):
        self.file.close()

    def log(self, msg: str, msg_type: Type = Type.INFO):
        """Write a log message
        
        Arguments:
            msg (str)
                The message
            msg_type (Type, optional)
                The message type that indicates its severity, this should be one
                of the options given by the enum `Type` (default: `Type.INFO`)
        """
        if not isinstance(msg, str):
            raise ValueError("The given message is not a string.")
        if not isinstance(msg_type, Type):
            raise ValueError("The message type is not an instance of the enum \"Type\".")
        
        output_string  = "[" + msg_type.name.center(10) + "] "
        output_string += datetime.now().strftime("%d/%m/%Y %H:%M:%S - ")
        output_string += msg

        self.file.write(output_string + '\n')
        if self.verbose:
            print(output_string)
