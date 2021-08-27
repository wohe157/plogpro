from __future__ import print_function

from abc        import ABCMeta, abstractmethod
from datetime   import datetime

from .settings  import LogType


class LogMessage:
    """Container class for log messages

    This class contains all the necessary information about a log message and is
    used to send this information from the base class ``Logger`` to an actual
    implementation of a logger. More specifically, when a user calls the
    ``log()`` method of a logger, a ``LogMessage`` will be created and passed on
    to the ``write_message()`` implementation.
    
    Arguments:
        msg (str)
            The message
        msg_type (LogType, optional)
            The message type that indicates its severity, this should be one
            of the options given by the enumeration ``LogType``
            (default: ``LogType.INFO``)

    Attributes:
        msg (str)
            The text message given to the ``log()`` function
        type (LogType)
            The type of the log message
        time (datetime)
            The time of the log message
        timestring (str)
            A formatted string with the date and time of the message
    """

    def __init__(self, msg, msg_type):
        if not isinstance(msg, str):
            raise ValueError("The given message is not a string.")
        if not isinstance(msg_type, LogType):
            raise ValueError("The message type is not an instance of the enum \"Type\".")
        
        self.msg = msg
        self.type = msg_type
        self.time = datetime.now()
        self.timestring = self.time.strftime("%d/%m/%Y %H:%M:%S")


class Logger(metaclass=ABCMeta):
    """Base class that provides an interface for different loggers

    To be able to log messages using a logger of your choice, e.g.
    ``TextLogger``, create an instance of that logger. You can then use the
    method ``log(msg, msg_type)`` to actually write a log message to a file.

    To implement a new logger, create a class that inherits from ``Logger`` and
    at least has a method ``write_message(self, msg)`` that accepts one
    argument: an instance of the ``LogMessage`` class.
    
    Warning:
        The ``log()`` method should **not** be overwritten.
    """

    def log(self, msg, msg_type=LogType.INFO):
        """Write a log message
        
        Arguments:
            msg (str)
                The message
            msg_type (LogType, optional)
                The message type that indicates its severity, this should be one
                of the options given by the enumeration ``LogType``
                (default: ``LogType.INFO``)
        """
        message = LogMessage(msg, msg_type)
        self.write_message(message)

    @abstractmethod
    def write_message(self, msg):
        raise NotImplementedError


class TextLogger(Logger):
    """A logger that writes messages to a text file
    
    The messages are written with the following syntax::

        [  <Type>  ] <Date> <Time> - <Message>

    Arguments:
        fname (str)
            The name of the output file
        overwrite (bool, optional)
            Whether to overwrite the contents of the output file if it
            already exists or to append the messages to the end of the file
            (default: `False`)
    
    Note:
        See ``Logger`` for more info on how to use the ``TextLogger``.
    """

    def __init__(self, fname, overwrite=False):
        super().__init__()
        self.fname = fname
        self.file = open(fname, 'w' if overwrite else 'a')
    
    def __del__(self):
        self.file.close()

    def write_message(self, msg):
        output_string  = "[" + msg.type.name.center(10) + "] "
        output_string += msg.timestring + " - " + msg.msg
        self.file.write(output_string + '\n')


class ConsoleLogger(Logger):
    """A logger that writes messages to the console
    
    The messages are written with the following syntax::

        [  <Type>  ] <Date> <Time> - <Message>

    Note:
        See ``Logger`` for more info on how to use the ``ConsoleLogger``.
    """
    
    def write_message(self, msg):
        output_string  = "[" + msg.type.name.center(10) + "] "
        output_string += msg.timestring + " - " + msg.msg
        print(output_string)
