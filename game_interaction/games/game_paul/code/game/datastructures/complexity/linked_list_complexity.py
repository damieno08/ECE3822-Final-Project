"""
linked_list_complexity.py - Analyze time complexity of Linked List operations

Measures actual performance of Linked List operations and compares to theoretical Big O.

Author: [Paul Garrison]
Date: [4/11/26]
Lab: Lab 5 - NPC Patrol Paths with Linked Lists
"""

import sys
sys.path.append('../..')
from datastructures.stack import Stack
from datastructures.array import ArrayList
from datastructures.patrol_path import PatrolPath
import time
import matplotlib.pyplot as plt

def measure_array_append(n):
    arr = ArrayList()
    start = time.time()

    for i in range(n):
        arr.append(i)

    return time.time() - start


def measure_linked_append(n):
    path = PatrolPath("one_way")
    start = time.time()

    for i in range(n):
        path.add_waypoint(i, i)

    return time.time() - start


def run_tests():
    sizes = [100, 500, 1000, 5000, 10000]

    array_times = []
    linked_times = []

    print("Running performance tests...\n")

    for size in sizes:
        array_time = measure_array_append(size)
        linked_time = measure_linked_append(size)

        array_times.append(array_time)
        linked_times.append(linked_time)

        print(f"Size {size}:")
        print(f"  ArrayList:   {array_time:.6f} sec")
        print(f"  Linked List: {linked_time:.6f} sec")
        print()

    return sizes, array_times, linked_times


def plot_results(sizes, array_times, linked_times):
    plt.plot(sizes, array_times, label="ArrayList Append")
    plt.plot(sizes, linked_times, label="Linked List Append")

    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.title("Linked List vs Array Append Complexity")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    sizes, array_times, linked_times = run_tests()
    plot_results(sizes, array_times, linked_times)


if __name__ == "__main__":
    main()
