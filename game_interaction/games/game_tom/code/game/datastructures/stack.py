"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Author: Tom Lipski
Date: 2/19/2026
Lab: Lab 4 - Time Travel with Stacks
"""
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir) # Add parent directory to path
sys.path.insert(0, parent_dir)
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
        Since an arraylist forms the base of the stack, it will automatically
        initialize with 10 spaces
        """
        self.stack_base = ArrayList()
        
    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        self.stack_base.append(item)
        
    
    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item that was on top of the stack, or None if empty
        """

        # If stack is of size 0, return None
        if(self.stack_base.__len__() == 0):
            value = None
        # Else if stack size >0, continue with pop()
        else:
            value = self.stack_base.pop(-1)

        # return popped value
        return value
        
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the stack, or None if empty
        """
        return self.stack_base.__getitem__(-1)
        
    
    def is_empty(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack is empty, False otherwise
        """
        empty_value = False
        # if stack is empty set empty_value = true
        if(self.stack_base.__len__() == 0):
            empty_value = True

        # Return value of empty_value based on conditions
        return empty_value
        
    
    def size(self):
        """
        Get the number of items in the stack.
        
        Returns:
            int: The number of items currently in the stack
        """
        # Get number of items on stack
        stack_size = self.stack_base.__len__()
        # Return number of items on stack
        return stack_size
        
    
    def clear(self):
        """Remove all items from the stack."""
        self.stack_base.clear()
        
    
    def __str__(self):
        """String representation of the stack (for debugging)."""
        #Return string representation of stack.
        return self.stack_base.__str__()
