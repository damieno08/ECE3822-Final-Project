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
        for _ in range(capacity):
            self._buffer.append(None)
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
        # (After each write, tail is is incremented to point to index right after most recently written message. Head and tail will point to same index at this point.)
        self._buffer.__setitem__(self._tail, item)
        self._tail = (self._tail + 1) % self._capacity

        # return true for successful write
        return True

    def read(self):
        """
        Read the latest message in the buffer, self._tail - 1. If buffer is empty, return None. 

        """
        # check if buffer is empty
        if(self.is_empty()):
            return None
        # otherwise, return message at index of tail with modular arithemtic.
        # T = (T - 1 + capacity) % capacity
        else:
            return self._buffer[(self._tail - 1 + self._capacity) % self._capacity]

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
        
        Peek the next most recently written element in the buffer, tail - 2. 
        Use module arithmetic, to move toward head from current tail.
        T = (T - 2 + capacity) % capacity. If buffer is empty, return None.
        
        """

        # check if buffer is empty or if only one element in buffer, if so, return None"
        if(self.is_empty() or self.__len__() == 1):
            return None

        # otherwise, return tail
        else:
            return self._buffer.__getitem__((self._tail - 2 + self._capacity) % self._capacity)
        
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
