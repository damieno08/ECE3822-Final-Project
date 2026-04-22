"""
This program will define the history class for the arcade project of ECE3822

Revision History:
    (ALL) 04/10/2026 Create initial program
    (RL)  04/22/2026 Create some methods
"""

from datastructures.stack import Stack

class History:

    #initialize history class
    def __init__(self):

        # history is a Stack
        self._history = Stack()

    def get_history(self, idx = -1):
        """
        Return a history entry at a given index 
        If history is empty return None
        """
        if self._history.is_empty():
            return None
        return self._history.peek(idx)

    def set_history(self, session):
        """
        Add a new session to history
        """
        self._history.push(session)

    def size(self):
        """
        Return the number of items in the history
        """
        return self._history.size()
    
    def pop(self):
        """
        Remove and return the most recent history
        """
        return self._history.pop()

    def clear_history(self):
        """
        Remove all entries from history
        """
        self._history.clear()

