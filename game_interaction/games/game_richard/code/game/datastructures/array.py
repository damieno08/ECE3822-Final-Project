"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Richard Lin
Date: 2/9/2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        Initialize a new ArrayList with a fixed initial capacity
        """
        # TODO: Initialize instance variables
        self._capacity = initial_capacity
        self._size = 0
        self._data = [None]*self._capacity
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Return the number of elements currently in the list.
        """
        # TODO: Return the size
        return self._size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Return the element at a given index.
        IndexError: If index is out of bounds
        """
        # TODO: Return element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index out of bound")
        return self._data[index]
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        Replace the element at a given index.
        IndexError: If index is out of bounds.
        """
        # TODO: Set element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index out of bound")
        self._data[index] = value
    
    def append(self, value):
        """
        Add an element to the end of the list.
        Automatically resizes if capacity is reached.
        """
        if self._size >= self._capacity:
            new_capacity = self._capacity*2
            new_data = [None]*new_capacity

            for i in range(self._size):
                new_data[i] = self._data[i]
        
            self._data = new_data
            self._capacity = new_capacity

        self._data[self._size] = value
        self._size +=1
        
    
    def insert(self, index, value):
        """
        Insert an element at a given index.
        All Elements from index are shifted one position to the right.
        If the array is full, resizes first.
        """
        if index < 0:
            index += self._size
        if index < 0:
            index = 0
        if index > self._size:
            index = self._size
        
        if self._size >= self._capacity:
            new_capacity = self._capacity*2
            new_data = [None]*new_capacity

            for i in range(self._size):
                new_data[i] = self._data[i]

            for i in range(index, self._size):
                new_data[i+1] = self._data[i]
            self._data = new_data
            self._capacity = new_capacity
        else:
            for i in range(self._size, index, -1):
                self._data[i] = self._data[i-1]

        self._data[index] = value
        self._size +=1
    
    def remove(self, value):
        """
        Remove the first occurrence of a value from the list.
        ValueError: If value is not found
        """
        for i in range(self._size):
            if(self._data[i] == value):
                for j in range(i, self._size - 1):
                    self._data[j] = self._data[j+1]

                self._data[self._size - 1] = None        
                self._size -= 1
                return

        raise ValueError(f"{value} not found in ArrayList")
    
    def pop(self, index=-1):
        """
        Remove and return the element at the given index. 
        If no index is specified remove and return the last item.
        IndexError: list is empty or the index is out of bound.
        """
        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise IndexError("pop Index out of bound")
        
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None

        self._size -= 1
        return value
    
    def clear(self):
        """
        Remove all items from the list
        """

        for i in range(self._size):
            self._data[i] = None    
        self._size = 0
    
    def index(self, value):
        """
        Return zero-based index of the list of the first occurrence of value in the list.
        ValueError: if there is no such item
        """
        for i in range (self._size):
            if (self._data[i] == value):
                return i
        raise ValueError("value not in ArrayList")

    def count(self, value):
        """
        Return the number of times a value appear in the list.
        """
        count = 0
        for i in range (self._size):
            if(self._data[i] == value):
                count+=1
        return count

    def extend(self, iterable):
        """
        Extend the list by appending all the items from the iterable
        """
        for item in iterable:
            self.append(item)
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Makes the "in" operator work: if 5 in my_array:
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False
        
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Returns a user-friendly string representation when you call str(my_array) or print(my_array)
        """
        elements = []
        for i in range(self._size):
            elements.append(str(self._data[i]))
        return "[" + ",".join(elements) + "]"
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Returns a developer-friendly string representation (often the same as __str__ for simple classes), used in the interactive shell
        """
        return f"{self.__class__.__name__}({str(self)})"
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Makes the list iterable so you can use it in for loops: for item in my_array:
        """
        for i in range(self._size):
            yield self._data[i]
