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
CAPACITY = 20

def test_create_buffer():
    """
    Test creation of circular buffer as well as is_empty and is_full methods.
    """

    print("Testing of the creation of the circular buffer works...")
    
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

    print("✓ Testing of the creation of the circular buffer works!")


def test_write_read():
    """
    
    Test the write and read methods for the circular buffer where the size exceeds the
    capacity.
    
    """

    print("Testing of the creation of circular buffer and write and read methods...")
    

    # create buffer
    test_buffer = CircularBuffer(CAPACITY)
    #print(f"Self._tail is {test_buffer._tail}.")

    # write CAPACITY * 2 elements to the circular buffer and
    # assert head and tail pointers move accordingly via the
    # modulo arithmetic
    # for 0 < i < CAPACITY, head remains 0
    # once capacity reached, head is incremented and
    # tail will also point to head, primed to overwrite head on next write
    for i in range(CAPACITY+2):
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
    # print(f"The most recent is the string '{test_buffer.read()}'.")
    # print(f"The next most recent is the string '{test_buffer.peek()}'.")

    print("✓ Testing of the creation of circular buffer and write and read methods works!")

def test_edge_cases():
    """

    Test some of the edge cases associated with the circular buffer class.
    
    """

    print("Testing of some edge cases for the circular buffer...")
    
    # create buffer
    test_buffer = CircularBuffer(CAPACITY)

    # assert read returns None
    assert test_buffer.is_empty()
    assert test_buffer.read() == None

    # add one element and assert None when peeking
    test_buffer.write("First write.")
    assert test_buffer.__len__() == 1
    assert test_buffer.peek() == None

    for i in range(test_buffer._capacity*2):
        test_buffer.write(f"'{i}'th entry")

    # after # of writes > than capacity, assert that length is equal to capacity
    assert test_buffer.__len__() == test_buffer._capacity

    print("✓ Testing of some edge cases for the circular buffer works!")

def test_is_full():
    """
    Test that is_full() returns False while filling and True exactly at capacity,
    and that writing one more item (overflow) leaves is_full() still True
    and does not increase size beyond capacity.
    """
 
    print("Testing is_full method...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    # buffer should not be full before capacity is reached
    for i in range(CAPACITY - 1):
        test_buffer.write(i)
        assert not test_buffer.is_full(), f"Expected not full at size {i+1}"
 
    # writing the final item should make it exactly full
    test_buffer.write(CAPACITY - 1)
    assert test_buffer.is_full()
    assert test_buffer._size == CAPACITY
 
    # writing one more item should overwrite the oldest — size stays at capacity
    test_buffer.write(999)
    assert test_buffer.is_full()
    assert test_buffer._size == CAPACITY
 
    print("✓ Testing is_full behavior works!")
 
 
def test_overflow_data_integrity():
    """
    After overflowing the buffer, verify that read() returns the most recently
    written value and peek() returns the second most recently written value.
    This confirms data is correctly stored and not corrupted on overflow.
    """
 
    print("Testing data integrity after overflow...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    # fill past capacity: write 0, 1, 2, ... CAPACITY+4
    for i in range(CAPACITY + 5):
        test_buffer.write(i)
 
    # most recently written value is CAPACITY + 4
    assert test_buffer.read() == CAPACITY + 4, (
        f"Expected {CAPACITY + 4}, got {test_buffer.read()}"
    )
 
    # second most recently written value is CAPACITY + 3
    assert test_buffer.peek() == CAPACITY + 3, (
        f"Expected {CAPACITY + 3}, got {test_buffer.peek()}"
    )
 
    print("✓ Testing data integrity after overflow works!")
 
 
def test_write_returns_true():
    """
    Verify that write() returns True on every call — both before and after
    the buffer reaches capacity (overflow case).
    """
 
    print("Testing write() return value...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    # write returns True when buffer is not full
    for i in range(CAPACITY):
        result = test_buffer.write(i)
        assert result == True, f"Expected True on write {i}, got {result}"
 
    # write returns True when buffer is full (overflow path)
    for i in range(5):
        result = test_buffer.write(i)
        assert result == True, f"Expected True on overflow write {i}, got {result}"
 
    print("✓ Testing write() return value works!")
 
 
def test_capacity_one():
    """
    Test a buffer with capacity 1 — a degenerate but valid edge case.
    Every new write should overwrite the single slot.
    """
 
    print("Testing capacity-1 buffer...")
 
    test_buffer = CircularBuffer(1)
 
    assert test_buffer.is_empty()
    assert not test_buffer.is_full()
 
    # write one item — buffer should now be full
    test_buffer.write("first")
    assert test_buffer.is_full()
    assert test_buffer._size == 1
    assert test_buffer.read() == "first"
 
    # overwrite with a second item — most recent should update
    test_buffer.write("second")
    assert test_buffer.is_full()
    assert test_buffer._size == 1
    assert test_buffer.read() == "second"
 
    # peek on a single-element buffer should return None
    assert test_buffer.peek() == None
 
    print("✓ Testing capacity-1 buffer works!")
 
 
def test_mixed_types():
    """
    Verify the buffer correctly stores and returns different Python types —
    integers, strings, floats, None, lists, and dicts.
    """
 
    print("Testing mixed-type writes...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    items = [42, "hello", 3.14, None, [1, 2, 3], {"key": "value"}]
 
    for item in items:
        test_buffer.write(item)
 
    # most recently written item is the dict
    assert test_buffer.read() == {"key": "value"}
    # second most recently written is the list
    assert test_buffer.peek() == [1, 2, 3]
 
    print("✓ Testing mixed-type writes works!")
 
 
def test_pointer_wraparound():
    """
    Verify that _tail wraps back to 0 after reaching the end of the underlying
    array, and that _head follows correctly during overflow.
    """
 
    print("Testing pointer wraparound...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    # fill exactly to capacity: tail should now be back at 0 (wrapped)
    for i in range(CAPACITY):
        test_buffer.write(i)
 
    assert test_buffer._tail == 0, (
        f"Expected tail to wrap to 0 after {CAPACITY} writes, got {test_buffer._tail}"
    )
    assert test_buffer._head == 0
 
    # one more write causes overflow: head and tail both advance to 1
    test_buffer.write(999)
    assert test_buffer._tail == 1
    assert test_buffer._head == 1
 
    # write CAPACITY - 1 more items to wrap tail all the way around again
    for i in range(CAPACITY - 1):
        test_buffer.write(i)
 
    assert test_buffer._tail == 0, (
        f"Expected tail to wrap to 0 again, got {test_buffer._tail}"
    )
 
    print("✓ Testing pointer wraparound works!")
 
 
def test_peek_after_overflow():
    """
    Write exactly capacity + 1 items and verify that after overflow:
      - read()  returns the last written item
      - peek()  returns the second-to-last written item
      - size remains at capacity
    """
 
    print("Testing peek() after overflow...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    for i in range(CAPACITY + 1):
        test_buffer.write(i)
 
    # most recent is CAPACITY (the overflow item)
    assert test_buffer.read() == CAPACITY
    # second most recent is CAPACITY - 1
    assert test_buffer.peek() == CAPACITY - 1
    # size should still be capped at CAPACITY
    assert test_buffer.__len__() == CAPACITY
 
    print("✓ Testing peek() after overflow works!")
 
 
def test_len_during_fill():
    """
    Verify __len__() increments by 1 on each write until capacity is reached,
    then stays constant at capacity during overflow writes.
    """
 
    print("Testing __len__() during fill and overflow...")
 
    test_buffer = CircularBuffer(CAPACITY)
 
    # size should increment with each write up to capacity
    for i in range(CAPACITY):
        test_buffer.write(i)
        assert test_buffer.__len__() == i + 1, (
            f"Expected length {i+1}, got {test_buffer.__len__()}"
        )
 
    # additional writes should not increase size past capacity
    for i in range(10):
        test_buffer.write(i)
        assert test_buffer.__len__() == CAPACITY, (
            f"Expected length {CAPACITY} after overflow write {i}, got {test_buffer.__len__()}"
        )
 
    print("✓ Testing __len__() during fill and overflow works!")


def run_all_test():

    test_create_buffer()
    test_write_read()
    test_edge_cases()
    test_is_full()
    test_overflow_data_integrity()
    test_write_returns_true()
    test_capacity_one()
    test_mixed_types()
    test_pointer_wraparound()
    test_peek_after_overflow()
    test_len_during_fill()
    

if __name__ == '__main__':
    run_all_test()

    print("\nALL TESTS PASSED")
