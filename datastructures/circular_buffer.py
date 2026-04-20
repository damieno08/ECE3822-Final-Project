"""
circular_buffer.py - Circular Buffer base class
Author: Santiago Troya

Revision History:
    (ST) 04/19/2026 Create initial class
    (TL) 04/19/2026 Method implementations


"""

from datastructures.array import ArrayList


class CircularBuffer:

    
    def __init__(self, capacity):
        self._capacity = capacity
        self._buffer = ArrayList(capacity)
        self._head = 0
        self._tail = 0
        self._size = 0

    def write(self, item):
        """
        
        Add a new message to the circular buffer. If buffer is full, size == capacity, overwrite
        posiiton based off of modulo arithmetic, and update head and tail positions accordingly. 
        Return true for successful write.

        """
        # if buffer is full, update head to overwrite oldest message/head
        if(self.is_full()):
            self._head = (self._head + 1) % self._capacity
        else:
            self._size += 1

        # write item to buffer at tail position then update tail position and size
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity

        # return true for successful write
        return True

    def read(self):
        """
        Read most oldest message in the buffer, self._head. If empty, return None. 

        """
        # check if buffer is empty
        if(self.is_empty()):
            return None
        # otherwise, return message at head
        else:
            return self._buffer[self._head]

    def is_full(self):
        """
        
        Return true if buffer is full, size == capacity, false otherwise.

        """

        # check to see if size is equal to capacity, return true if equal
        if(self._size == self._capacity):
            return True
        
        # otherwise return false
        return False

    def is_empty(self):
        """
        
        Return true if buffer is empty, size == 0, false otherwise.
        
        """

        # check size of buffer, return true if size == 0
        if(self._size == 0):
            return True
        
        # otherwise return false
        return False

    def peek(self):
        """
        
        Peek the most recently written element in the buffer, tail.
        
        """

        # check if buffer is empty, if so, return None
        if(self.is_empty()):
            return None

        # otherwise, return tail
        else: 
            return self._buffer[self._tail - 1]       
        
    def __len__(self):
        """
        
        Return the current length, self._size, of the buffer.

        """
        # if buffer is empty, return 0
        if(self.is_empty()):   
            return 0
        # otherwise, return size of buffer
        else:
            return self._size
