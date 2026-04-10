"""
linked_list_tests.py - Test suite for Linked List implementation

Tests all Linked List methods with edge cases.

Author: [Your Name]
Date: [Date]
Lab: Lab 6 Enemy Patrol Paths
"""

import sys
sys.path.append('../..')

from datastructures.linked_list import linked_list,node

def test_traverse():
    L = linked_list()
    N1 = node()
    N2 = node()
    L.add_node(N1)
    L.add_node(N2)

    ender = True
    count = 0

    while ender != False:
        ender = L.move()
        count +=1
        if count > 2:
            raise IndexError("Loop failed; continued to move past end pointer")
            break
    print("Travelersal Passed")

def test_add_non_node():
    L = linked_list()
    N1 = 12

    assert L.add(N1) == False
    print("Adding non-node test complete")

def run_all_tests():
    """Run all linked list tests"""
    print("=" * 50)
    print("Running Linked List Tests")
    print("=" * 50)
    print()
    test_traverse()
    print()
    print("=" * 50)
    print("✓ ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
