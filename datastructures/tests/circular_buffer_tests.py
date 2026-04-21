"""
circular_buffer_tests.py - Tests for CircularBuffer

Author: Tom Lipski
Date: 04/20/2026
Final Design Project

Revision History:
(TL) Create initial test program and individual tests

"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.circular_buffer import CircularBuffer

# CAPACITY OF BUFFER
CAPACITY = 5

def test_create_buffer():
    """
    Test creation of circular buffer as well as is_empty and is_full methods.
    """

    # create buffer
    test_buffer = CircularBuffer(CAPACITY)

    # assert buffer is empty
    assert test_buffer.is_empty()
    assert not test_buffer.is_full()
    assert test_buffer._size == 0

    # assert head, tail and capacity
    assert test_buffer._head == 0
    assert test_buffer._tail == 0
    assert test_buffer._capacity == CAPACITY

    # add an element
    test_buffer.write("Hello ECE3822")
    assert test_buffer._size == 1

    # read an element
    assert test_buffer.read() == "Hello ECE3822"

    # add a few more elements
    test_buffer.write("This is a circular buffer")
    test_buffer.write("This is for the final design project")

    assert test_buffer.read() == "This is for the final design project"
    assert test_buffer.peek() == "This is a circular buffer"


def test_write_read():
    """
    
    Test the write and read methods for the circular buffer where the size exceeds the
    capacity.
    
    """
    

    # create buffer
    test_buffer = CircularBuffer(CAPACITY)
    print(f"Self._tail is {test_buffer._tail}.")

    # write CAPACITY * 2 elements to the circular buffer and
    # assert head and tail pointers move accordingly via the
    # modulo arithmetic
    # for 0 < i < CAPACITY, head remains 0
    # once capacity reached, head is incremented and
    # tail will also point to head, primed to overwrite head on next write
    for i in range(CAPACITY*2 + 2):
        test_buffer.write(i)
        # assert head pointer is 0 if buffer not full
        if(i < CAPACITY):
            assert test_buffer._head == 0
        # otherwise assert that head and tail pointers point to same index
        else:
            assert test_buffer._head == test_buffer._tail
        
        # print(f"Value is {test_buffer.read()}.")
        # print(f"Self._head is {test_buffer._head}.")
        # print(f"Self._tail is {test_buffer._tail}.\n")

    # read most recent message
    print(f"Self._tail is {test_buffer._tail}.")
    print(test_buffer.read())
    print(f"Self._tail is {test_buffer._tail}.")
    print(test_buffer.peek())

    # try with strings
    test_buffer.write("This is the first string")
    test_buffer.write("This is the second string")
    print(f"The most recent is the string '{test_buffer.read()}'.")
    print(f"The next most recent is the string '{test_buffer.peek()}'.")
    


def run_all_test():

    test_create_buffer()
    test_write_read()

if __name__ == '__main__':
    run_all_test()

    print("\nALL TESTS PASSED")
