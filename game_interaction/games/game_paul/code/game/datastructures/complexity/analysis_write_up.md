# Linked List Complexity Analysis Write-Up

**Author:** [Paul Garrison]
**Date:** [4/11/26]
**Lab:** Lab 5 - NPC Patrol Paths with Linked Lists

---

## Overview

This analysis tested the performance of linked list waypoint insertion using `add_waypoint()` and compared it against `ArrayList` append performance. The goal was to compare measured runtime with theoretical Big O complexity.

---

## Time Complexity Analysis

### Operation Tested: `add_waypoint()`

**Theoretical Complexity:** O(1) per insertion, O(n) for n insertions

**Results:**

| n (waypoints) | Time (seconds) |
|--------------|----------------|
| 100          | 0.000277       |
| 1,000        | 0.001740       |
| 10,000       | 0.014817       |
| 100,000      | N/A            |

**Theory vs. Practice:**  
The measured runtime increased approximately linearly as `n` increased, which matches the expected **O(n)** total runtime for performing `n` constant-time insertions.

**Discrepancies:**  
Times are not perfectly proportional because of Python interpreter overhead, object creation costs, and small timing fluctuations.

---

### Operation Tested: `get_next_waypoint()`

**Theoretical Complexity:** O(1)

**Results:**

| n (waypoints) | Time (seconds) |
|--------------|----------------|
| 100          | Constant        |
| 1,000        | Constant        |
| 10,000       | Constant        |
| 100,000      | Constant        |

**Theory vs. Practice:**  
This operation is constant time because it only moves a pointer to the next node.

**Discrepancies:**  
Minor differences may occur due to system timing precision.

---

## Space Complexity Analysis

**Theoretical Complexity:** O(n)

**Results:**

| n (waypoints) | Memory (bytes) |
|--------------|----------------|
| 100          | O(100)         |
| 500          | O(500)         |
| 1,000        | O(1000)        |
| 5,000        | O(5000)        |

**Theory vs. Practice:**  
Memory usage grows linearly because each waypoint requires one node object and pointer references.

---

## Linked Lists vs. Arrays

The `ArrayList` was faster for all tested sizes.

For example:

- 10,000 array inserts: **0.005056 sec**
- 10,000 linked list inserts: **0.014817 sec**

Arrays are better for fast indexing and lower overhead.

Linked lists are better for NPC patrol paths because moving to the next waypoint, looping routes, and backtracking are naturally efficient.

---

## Conclusions

The results confirmed theoretical complexity expectations.

Adding 10,000 waypoints took **0.014817 seconds**, showing linear growth consistent with **O(n)** total scaling.

This makes linked lists practical for NPC patrol systems because traversal and directional movement remain efficient while supporting circular and doubly linked paths.