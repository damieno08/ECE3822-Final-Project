"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Damien Ortiz
Date: 02/11/2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self,initial_capacity: int = 10):
        """
        Function will create an instance of the ArrayList class

        Inputs:
            intial_capacity (int): initialize length of our array

        Values:
            array: array storing data
            ____max_length: current maximum length of our array
            end: next write index and current size 
        """
        # TODO: Initialize instance variables

        # Give initial_capacity blank values
        self.array = [None] * initial_capacity

        # Keep track of size
        self.__max_length = initial_capacity

        # Keep track of end of array and number of elements
        self.__end = 0
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Function will return the current size of our array

        """
        # Return size
        return self.__end
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index: int):
        """
        Function returns the value at an index if the index is valid

        Inputs:
            index (int): The index we would like to look for our value at

        Outputs: 
            self.array[index]: The value stored at the index we searched
        """
        # Check that index is valid and return value
        if index < self.__end and index >= 0:
            return self.array[index]
        
        # Tell user they input an invalid index
        raise IndexError("Error: Cannot index value in unallocated memory")
        
    # Returns the current maximum size of the array
    def get_capacity(self):
        """
        Function will return the maximum length of the array
        
        Output:
            self.__max_length (int): maximum length allowed for array until resizing
        """

        return self.__max_length
    
    # Resize the array whenever we need more space
    def __resize(self):
        """
        Function will create a new array with more space, copy values into the new array,
        delete the old array, and then set our object array to this new larger array
        
        """

        # Create blank array twice the size of old array
        array = [None] * self.__max_length * 2

        # Copy old values
        array[0:self.__end] = self.array

        # Set object array to the new array
        self.array = array

        # Update size of array
        self.__max_length*=2

    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index: int, value):
        """
        Function sets the value at an index to the desired value if the index is valid

        Inputs:
            index (int): The index we would like to change the value of
            value: The value we would like to place into the index; Can be of any type
        """

        # Check that index is valid
        if index < self.__end and index >=0:
            self.array[index] = value
            return
        
        # Tell user if index is invalid
        raise IndexError("Error: Cannot place value in unallocated memory")
    
    # Add value to array
    def append(self, value):
        """
        Function will add the value to the end of the list

        Input: 
            value: The value we would like to add to the array
        """

        # Check if we have free space
        if self.__end == self.__max_length:

            # If we don't, reallocate memory and copy values to larger array
            self.__resize()
            
        # Add value to the end of array
        self.array[self.__end] = value

        # Move end of array index
        self.__end+=1
            
    # Insert a value at some index
    def insert(self, index: int, value):
        """
        Function will place a value at a desired index so long as the index is valid

        Inputs:
            index (int): The index we want to write to
            value: The value we want to write into the desired index
        """

        # Tell user if they indexed outside of array
        if index > self.__end or index < 0:
            raise IndexError("Error: Index must be within current array")

        # Check for enough space to do insertion
        if self.__end == self.__max_length:

            # If we don't, reallocate memory and copy values to larger array
            self.__resize()

        # Move all values foward
        for i in range(self.__end-1, index-1, -1):
            self.array[i+1] = self.array[i]
        
        # Insert value at the index
        self.array[index] = value

        # Move end index
        self.__end+=1

    
    def remove(self, value):
        """
        Function will remove a given value within the array

        Input:
            value: The value we would like to remove from our list
        """

        # Start at 0 and assume value is not in list
        index = 0
        found = False

        # Run through each value in list
        for i in range(self.__end):

            # Check if any index has the value we want to remove
            if self.array[i] == value:

                # Store the index we need to remove the value from
                index = i

                # Store boolean saying the value is within the array
                found = True

                # Exit loop once we have found a match
                break
        
        # Tell user the value isn't inside the array if we don't find it
        if not found:
            raise ValueError("Error: value not inside of array")
        
        # Move all values one space
        for i in range(index, self.__end-1):
            self.array[i]=self.array[i+1]

        # Remove end of list and move end index
        self.array[self.__end-1] = None
        self.__end-=1

    
    # Remove and return a value
    def pop(self, index: int = -1):
        """
        Function will take an index, check if it is valid, 
        then remove the value at the index and return it.

        Input:
            index (int): The index we would like to remove and return the value 

        Output:
            val: The value returned at the index we are searching for
        """

        # Check that index is valid and alert user if not
        if index >= self.__end or self.__end == 0:
            raise IndexError("Error: Index must be within range of current array")
        
        # Default case to return and remove end of list
        if index == -1:
            val = self.array[self.__end-1]
            self.array[self.__end-1] = None

            # Move end index
            self.__end-=1

        else:

            # Store the value we want to remove
            val = self.array[index]

            # Move all values to overwrite the index we would like to remove
            for i in range(index, self.__end-1):
                self.array[i]=self.array[i+1]

            # Move end index
            self.__end-=1

        # Return value we removed
        return val

    
    def clear(self):
        """
        Function will delete all values but keep allocated space for array
        """

        # Go to each index and delete the value
        for index in range(self.__end):
            self.array[index] = None

        # Move end index to start of array
        self.__end = 0
    
    def index(self, value):
        """
        Find the first index where a value occurs if the value is within the array

        Input:
            value: The value we search for inside the array

        Output:
            i (int): The index where the value was found

        """

        # Search for each index and retun if the value was found
        for i in range(self.__end):
            if self.array[i] == value:
                return i
            
        # Return an error if the value is not within the list
        raise ValueError("Value is not in ArrayList")


    def count(self, value):
        """
        Function will count the number of occurences of a desired value

        Input:
            value: Value we would like to count occurences for

        Output:
            counter (int): The number of times the desired value occurs
        """

        # Initialize counter to 0
        counter = 0

        # Loop through each element incrementing counter by 1 if value is found
        for i in range(self.__end):
            if self.array[i] == value: counter+=1
        
        # Return the occurences of the value
        return counter


    def extend(self, iterable):
        """
        Function will take an iterable object and append each of its elements
        to the end of the ArrayList

        Input:
            iterable: Any iterable object (list, tuple, string, etc.) 
                      whose elements will be added to the ArrayList
        """
        
        # Loop through iterable and append each item
        for item in iterable:
            self.append(item)

    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Function takes a value and will tell the user whether that value is wtihin our array
        """

        # Loop through each element and check if value is inside the array
        for i in range(self.__end):

            # If we find the value inside the array return true
            if self.array[i] == value:
                return True
            
        # Return false if the value was not found
        return False
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Function will allow the array to print in a human readable fashion
        """
        # Show class name and starting bracket
        s = "Class: ArrayList ; Values: ["

        # Append each element to the string followed by a comma
        for i in range(self.__end):
            s+= str(self.array[i])
            if i < self.__end-1:
                s+="," 
        
        # Add closing bracket
        s+="]"

        # Return the string representation of the array
        return s
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Function will allow the array to print in a human readable fashion

        """

        # Show class name and starting bracket
        s = "Class: ArrayList ; Values: ["

        # Append each element to the string followed by a comma
        for i in range(self.__end):
            s+= str(self.array[i])
            if i < self.__end-1:
                s+="," 
        
        # Add closing bracket
        s+="]"

        # Return the string representation of the array
        return s
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Function will allow the ArrayList to be iterable

        Output:
            Each element in the ArrayList one at a time,
            enabling use in for-loops and other iterable contexts
        """

        # Yield each element currently stored in the array
        for i in range(self.__end):
            yield self.array[i]
