"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Tom Lipski
Date: 02/16/2026
Lab: Lab 4 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        Constructor: Initialize an initial capacity of 10, intantiate
        number of items in list and instantiate empty list of size
        initial_capacity
        
        """
        # DONE: Initialize instance variables
        self.capacity = initial_capacity
        self.number_items = 0
        self.my_array = [None]*initial_capacity

    def get_capacity(self):
        """
        Return current capacity of arraylist at a given time. 
        """
        return self.capacity

    def get_size(self):
        """
        Return the number of elements currently in the array. 
        """

        return self.number_items
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Return the number of elements in the dynamic array list. 
        """
        # DONE: Return the size
        size = self.number_items
        return size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Return item at specified index passed into method.
        Raise IndexError if index out of bounds. 
        """
        # DONE: Return element at index)
        
        if((index < 0) or (index > self.number_items)):
            raise IndexError("Index out of bounds.")
        else:
            return self.my_array[index]
        #return self.my_array[index]
        
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        For an index and value passed in, set element at passed in index to passed in value
        """
        # DONE: Set element at index
        if((index < 0) or (index > self.number_items)):
            raise IndexError("Index out of bounds.")
        else:
            self.my_array[index] = value
    
    def append(self, value):
        """
        If number of items in arraylist is less than size of current
        arraylist, add to end of arraylist, arraylist[number_items] and
        then increment number_items by 1,
        else, multiply current capacity by 2 and then add value to
        arraylist index,number_items and then increment number_items by 1
        """
        if (self.number_items < self.capacity):
            self.my_array[self.number_items] = value
        else:
            # Calculte new capacity and create new array
            new_capacity = 2*self.capacity
            new_array = [None]*new_capacity

            # Copy over values from old array to new array
            for i in range(self.number_items):
                new_array[i] = self.my_array[i]

            # Copy over new array and size data
            self.my_array = new_array
            self.capacity = new_capacity

            # Append new item
            self.my_array[self.number_items] = value

        self.number_items += 1
    
    def insert(self, index, value):
        """
        For index and value passed in, if (number_items + 1) <= capacity,
        shift data to the right one space until index is available,
        then insert value at my_array[index]. Else, if
        (number_items + 1) > capacity, resize array, then shift and add
        value.
        """
        # If index is out of bounds, throw IndexError
        if((index < 0) or (index >= self.number_items)):
            return index
            raise IndexError("Index out of bounds.")
        # Else, proceed with insert
        else:
            if((self.number_items+1) < self.capacity):
                # Shift items above index to the right one space
                for j in range(self.number_items, index, -1):
                    self.my_array[j] = self.my_array[j-1]

                # Set my_array[index] = value
                self.my_array[index] = value

            else:
                # Double current capacity and create new array
                new_capacity = 2*self.capacity
                new_array = [None]*new_capacity

                # Copy over current array to new array
                for k in range(self.number_items):
                    new_array[k] = self.my_array[k]

                # Set original instance of array equal to new array
                # and set new capacity
                self.my_array = new_array
                self.capacity = new_capacity

                # Shift items and then insert
                for j in range(self.number_items, index, -1):
                    self.my_array[j] = self.my_array[j-1]
                    self.my_array[index] = value

            # increment number of items in array
            self.number_items += 1
            
           
    
    def remove(self, value):
        """
        For value passed in, search array and if it exists, remove.
        Otherwise do nothing. 
        """
        index_r = 0 # holder for index of found value
        item_found = False # Flag for if value is found

        # Loop through array and evaluate each element for equality
        # value passed in. If found, remove and shrink array and
        # number_items.
        for i in range(self.number_items):
            
            # check for equality
            # if found, get index and set flag to True then break
            if(self.my_array[i] == value):
                index_r = i
                item_found = True
                break


        # remove element from index_r, then shrink array and number_items
        if(item_found):

            # start at index_r, shift higher elements down one, writing
            # over index_r
            for i in range(index_r, self.number_items-1, 1):
                self.my_array[i] = self.my_array[i+1]

            # after shifting remaining elements down, erase
            # last remaining element at index (number_items - 1)
            self.my_array[self.number_items-1] = None

            # update number of items in list
            self.number_items -= 1
    
    def pop(self, index=-1):
        """
        Pop(remove) element of index passed in. If no index was passed in, pop last
        element. 
        """
        # if index to be popped is out of bounds, throw IndexError
        if((index < -1) or (index >= self.number_items)):
            raise IndexError("Index out of bounds.")
        # Otherwise, continue with pop
        else:
            # variable to store popped element
            value_pop = None
            # Pop item from passed index, if index >= 0
            if( index >=0):

                # get value at index
                value_pop = self.my_array[index]

                # write over index passed in by looping through array starting at index
                # up to the end of array, shrinking array by one
                for i in range(index, self.number_items-1, 1):
                    self.my_array[i] = self.my_array[i+1]

                # after shifting remaining elements down, erase
                # last remaining element at index (number_items - 1)
                self.my_array[self.number_items-1] = None

            # Else, pop last element of array
            else:
                # Set last element of the array to None
                self.my_array[self.number_items-1] = None
                value_pop = self.my_array[self.number_items-1]


            # Decrement number of itmes on list by one
            self.number_items -= 1

            # return popped value
            return value_pop

        
    
    def clear(self):
        """
        Clear all elements of the array by erasing their values. Loop
        through the array and set each element to None. 
        """
        # Set all elements of the array to None for clearing
        for i in range(self.capacity):
            self.my_array[i] = None

            # reassigne size of array to 
        self.number_items = 0
        
    
    def index(self, value):
        """
        Loop through the array to find the index of the value passed
        in. If not found 
        """
        
        index_r = -1 # index of found element, initialized to -1

        # loop through elements to check for value
        for i in range(self.number_items):

            # if found, capture index value
            if(self.my_array[i] == value):
               index_r = i

        # If item is in list, return index, else return None
        if( index_r >= 0):
            return index_r
        else:
            raise ValueError("Item not in array.")
            return None

    def count(self, value):
        """
        Return a count of the number of times value appears in the array. 
        """
        count = 0 # counter variable

        # loop through array to count the number of instances of "value"
        for i in range(self.number_items):
            if(self.my_array[i] == value):
                count +=1
        
        # Return count of value.
        return count

    def extend(self, iterable):
        """
        Appendds the elements of another list to the end of the current
        array. 
        """
        
        j = self.number_items # variable for incrementing parent array
        temp = self.number_items # variable for keeping track of elements added
        # Check current number_items vs capacity in terms of available
        # space for the array to be appended
        # If not enough space, resize array
        if((self.capacity - self.number_items) < len(iterable)):
            # Double current capacity and create new array
            new_capacity = 2*self.capacity
            new_array = [None] * new_capcity

            # Copy data from current array to new array
            for i in range(self.number_items):
                new_array[i] = self.my_array[i]

            # assign my_array to new_array
            self.my_array = new_array
            
            
        # loop through array to append, incrementing j to add each element
        for i in iterable:
            self.my_array[j] = i
            j += 1
            temp +=1


        # Update current number_items
        self.number_items = temp
        
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Check to see if value passed in is contained within the array.
        Return True if value is found, else return False. 
        """
        in_array = False # boolean for status of value in array, initialized to False

        # loop through array to check for the value passed in
        # if value is found, set in_array = True and then break
        for i in range(self.number_items):
            if(self.my_array[i] == value):
               in_array = True
               break

        return in_array
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Return a user-friendly string representation of the array by
        converting the elements of the list to strings and concatenating
        them all into one final string to return to the user, for easy
        readability. 
        """

        # instantiate container for readable user string, initialize
        # with "["
        user_string = "["
               
        # loop through array and convert each element to a string and
        # then concatenate to user_string.
        for i in range(self.number_items):
            temp = str(self.my_array[i])
            user_string += temp
            # add comma and space for all, i != (number_items - 1)
            if(i == (self.number_items-1)):
                user_string += "]"
            else:
                user_string += ", "

               
        return user_string
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Returns a developer-friendly string representation. This will
        the same code as the __str__method. 
        """

        # instantiate container for readable user string, initialize
        # with "["
        developer_string = "["
               
        # loop through array and convert each element to a string and
        # then concatenate to user_string.
        for i in range(self.number_items):
            temp = str(self.my_array[i])
            developer_string += temp
            # add comma and space for all, i != (number_items - 1)
            if(i == (self.number_items-1)):
                developer_string += "]"
            else:
                developer_string += ", "

               
        return developer_string
               
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Iterable method. Generator method for implementation.
        """
        i = 0
        end = self.number_items
        while i < end:
            yield self.my_array[i]
            i += 1
        pass
