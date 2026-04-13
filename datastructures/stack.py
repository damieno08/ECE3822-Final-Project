"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Author: Damien Ortiz
Date: 02/20/2026
Lab: Lab 4 - Time Travel with Stacks
"""
from datastructures.array import ArrayList

class Stack:
    """
    A LIFO (Last-In-First-Out) data structure.
    
    The last item added is the first item removed.
    Think of it like a stack of plates - you add to the top and remove from the top.
    """
    
    def __init__(self):
        """
        Initialize an empty stack.
        """
        
        # Create an empty list for the stack
        self.__array = ArrayList()

    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """

        # Just append to our array
        self.__array.append(item)
    
    def get_array(self):
        """
        Return the array stored within the stack
        """
        
        # Bring array from array class
        return self.__array.array

    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item that was on top of the stack, or None if empty
        """

        # Check if our array is empty
        if self.is_empty():

            # Return none if empty
            return None
        
        # Return bottom of stack
        return self.__array.pop()

    # updated peek to look at any chosen index
    def peek(self, index=-1):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the stack, or None if empty
        """

        # Check if stack is empty
        if self.is_empty():

            # Return none if it is
            return None
        
        if index == -1:
            # Return the last value on stack
            return self.__array[self.size()-1]
        
        # Return any value besides end
        else:
            data = self.get_array
            return data[index]
    
    def is_empty(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack is empty, False otherwise
        """

        # Check that our array has values
        return self.size() == 0
    
    def size(self):
        """
        Get the number of items in the stack.
        
        Returns:
            int: The number of items currently in the stack
        """

        # Find the number of values in the array
        return len(self.__array)
    
    def clear(self):
        """Remove all items from the stack."""

        # Call array class clear function to empty values
        self.__array.clear()
    
    def __str__(self):
        """String representation of the stack (for debugging)."""
        s = "Class: Stack ; Values: ["
        for i in range(len(self.__array)):
           s+= str(self.__array[i])
           if i < self.size()-1:
                s+=","
        s+="]"

        # Return a string containing the class and all stored values
        return s
