from __future__ import print_function

from abc  import ABCMeta, abstractmethod
from time import time


class ProgressBar(metaclass=ABCMeta):
    """Base class that provides an interface for progress bars
    
    To implement a new progress bar, create a class that derives from
    `ProgressBar` and implement the method `draw()`. This method should draw the
    progress bar based on the accessible member variables.

    Usage:
        To create a progress bar, create an instance of one of its
        implementations. The progressbar can then be updated by calling the
        method `update()`.
    """

    def __init__(self, nsteps: int):
        """Create an instance of `ProgressBar`
        
        Arguments:
            nsteps (int)
                The number of steps that the progressbar will go through
        """
        self.nsteps = nsteps
        self.step = 0
        self.start_time = time()
        self.current_time = time()
    
    def update(self, step: int = None) -> None:
        """Update the progressbar

        Arguments:
            step (int, optional)
                The current step of the operation, the progress will be
                increased with one step if not provided
                (default: `None`)
        """
        self.current_time = time()
        if step is None:
            self.step += 1
        else:
            self.step = step
        self.draw()

    def progress(self) -> float:
        """Get the progress as a number between 0 and 1

        Returns:
            (float) The progress
        """
        return self.step / self.nsteps
    
    @abstractmethod
    def draw(self) -> None:
        pass
