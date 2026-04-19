"""
circular_buffer.py - Circular Buffer base class
Author: Santiago Troya
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
        pass

    def read(self):
        pass

    def is_full(self):
        pass

    def is_empty(self):
        pass

    def peek(self):
        pass

    def __len__(self):
        pass
