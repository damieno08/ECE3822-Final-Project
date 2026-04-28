"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Santiago Troya
Date: 02/11/2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here:
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """

    def __init__(self, initial_capacity=10):
        """
        Initializes an array with initial_capacity (in this case 10)
        empty elements. Using private attributes, to prevent external mods.
        """

        self._data = [None] * initial_capacity
        self._size = 0
        self._capacity = initial_capacity

    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Returns the number of elements in ArrayList
        """

        return self._size

    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Access to the item in the given index.

        Raises IndexError if the index is outside of the range
        """

        # check if index is inside of the range of the array
        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index is outside of range")

        return self._data[index]

    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        Sets the value provided in setitem to the corresponding index
        """
        # check if index is inside of the range of the array
        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index is outside of range")

        self._data[index] = value


    def append(self, value):
        """
        Allocates more memory to the array if needed,
        if no more memory is needed, then it copies to the last
        index being followed with size and then adds one to size so
        that it keeps being moved.

        """

        # if the data has reached the maximum capacity, then allocate
        # double the memory and copy the data from the previous data
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity

            # copy data
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data

        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """
        Checks if the index is inside of the range,
        allocates more memory if needed,
        copies data from back to front leaving a space in the index
        inserts value in the index position
        """
        # check if index is inside of the range of the array
        if index < 0 or index > self._size:
            raise IndexError("ArrayList index is outside of range")


        # resizing if max capacity is achieved
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity

            # copy data
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data

        # defining starting and ending positions for inserting
        initial_pos = self._size
        final_pos = index

        # loop backwards copying data
        # such that it doesn't get overwritten
        for i in range(initial_pos, final_pos, -1):
            self._data[i] = self._data[i - 1]

        # insert new value in the space left
        self._data[index] = value

        # increase the size since an element was added
        self._size += 1

    def remove(self, value):
        """
        Removes the first occurence of the specified value

        Exits once the first value was encountered and outputs
        an error if there is no such value
        """

        # find the value to remove with a O(n) algorithm since
        # this is an inventory game implementation
        for i in range(self._size):
            if self._data[i] == value:
                # shift items to the left from the
                # position of the object removed
                for j in range(i,self._size -1):
                    self._data[j] = self._data[j + 1]

                # set the last item to None since items were shifted
                # and the last is going to be repeated
                self._data[self._size - 1] = None

                # decreases the size since an item was removed
                self._size -= 1

                # exit such that it doesnt remove more of the same items
                return

        # if there isn't a value, then raise a value error
        raise ValueError(f"ArrayList.remove({value}) was not able to find {value}")

    def pop(self, index=-1):
        """
        Checks if the index requested is inside of the range

        if there is no items raises error

        copies the values to the left and returns the value at the given index
        """

        # check if there are items to be popped
        if self._size == 0:
            raise IndexError("There are no items in the array")

        # handle the default case
        if index == -1:
            index = self._size - 1

        # check if index is inside of the range of the array
        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index is outside of range")

        # save the value to be returned
        value_pop = self._data[index]

        # copy data and shift it to the left
        for i in range(index, self._size-1):
            self._data[i] = self._data[i+1]

        # set the last value to None
        self._data[self._size - 1] = None

        # reduce the size since there is a removed item
        self._size -= 1


        return value_pop

    def clear(self):
        """
        Clears the complete array
        """
        self._data = [None] * self._capacity
        self._size = 0


    def index(self, value):
        """
        finds the item in the value and provides an index for it
        """

        # use O(n) search for the value since it is going to be
        # implemented as an inventory
        for i in range(self._size):
            if self._data[i] == value:

                # return the index where the value was found
                return i

        raise ValueError(f"ArrayList.index({value}) the {value} was not found")

    def count(self, value):
        """
        Counts and returns the ammount of times the value is found in the array
        """

        counter = 0

        for i in range(self._size):
            if self._data[i] == value:
                counter += 1
        return counter


    def extend(self, iterable):
        """
        Extends the list by appending all elements from
        the iterable.
        """
        for item in iterable:
            self.append(item)

    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Returns true if the item is on the list, false if not
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False

    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        returns a string representation of ArrayList
        """
        # create an empty list wihout the extra None elements
        elements = []

        # copy information such that there is no extra None items
        for i in range(self._size):
            elements.append(str(self._data[i]))

        # formated return which returns a string
        return '[' + ', '.join(elements) + ']'

    # Returns a developer-friendly string representation (often the same as __str__ for simple classes),
    # used in the interactive shell
    def __repr__(self):
        """
        returns arraylist as a string
        """
        return f"ArrayList({self.__str__()})"

    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Returns an iterator over the class elements
        """
        for i in range(self._size):
            yield self._data[i]
