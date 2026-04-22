"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: [Paul Garrison]
Date: [2/12/26]
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        """
        # TODO: Initialize instance variables
        self._capacity = initial_capacity
        self._size = 0
        self._data = [None] * self._capacity
        pass
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        """
        # TODO: Return the size
        return self._size
        pass
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        """
        # TODO: Return element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        return self._data[index]
        pass
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        """
        # TODO: Set element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        self._data[index] = value
        pass
    
    def append(self, value):
        """
        """
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data

        self._data[self._size] = value
        self._size += 1
        pass
    
    def insert(self, index, value):
        """
        """
        if index < 0:
            index += self._size
        if index < 0:
            index = 0
        if index > self._size:
            index = self._size
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1
        pass
    
    
    def remove(self, value):
        """
        """
        for i in range(self._size):
            if self._data[i] == value:
                self.pop(i)
                return
        raise ValueError("Value not found")
        pass
    
    def pop(self, index=-1):
        """
        """
        if self._size == 0:
            raise IndexError("Pop from empty list")

        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        value = self._data[index]

        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

        return value
        pass

    def clear(self):
        """
        """
        self._data = [None] * self._capacity
        self._size = 0
        pass
    
    def index(self, value):
        """
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError("Value not found")
        pass

    def count(self, value):
        """
        """
        count = 0
        for i in range(self._size):
            if self._data[i] == value:
                count += 1
        return count
        pass

    def extend(self, iterable):
        """
        """
        for item in iterable:
            self.append(item)

        pass
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False
        pass
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        """
        return "[" + ", ".join(str(self._data[i]) for i in range(self._size)) + "]"
        pass 
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        """
        return self.__str__()
        pass
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        """
        for i in range(self._size):
            yield self._data[i]
        pass
