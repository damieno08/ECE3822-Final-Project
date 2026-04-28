# Graph Complexity Analysis

**Author:** Santiago Troya
**Date:** 04/27/2026
**Lab:** Lab 7 - NPC Dialog with Graphs

---

## 1. Implementation Overview

The Graph uses two HashTable instances as the backing store: `_adj` maps each node ID to a Python list of `(neighbor_id, weight, edge_data)` tuples, and `_data` maps each node ID to its payload dict. The graph supports both directed and undirected modes; in undirected mode `add_edge` inserts entries in both adjacency lists. The HashTable itself uses separate chaining with an ArrayList per bucket and doubles capacity when load factor exceeds 0.7.

---

## 2. Time Complexity Table

| Method            | Your Big-O    | Justification                                                                 |
|-------------------|---------------|-------------------------------------------------------------------------------|
| `add_node`        | O(1) avg      | Single HashTable.set call; O(1) average with a good hash and low load factor. |
| `add_edge`        | O(1) avg      | Two has_node checks plus one list.append per direction; all O(1) average.     |
| `remove_node`     | O(V + E)      | Must iterate all V nodes and scan their adjacency lists to remove touching edges. |
| `remove_edge`     | O(degree)     | Scans the adjacency list of from_id (length = out-degree) to find and remove the edge. |
| `has_node`        | O(1) avg      | HashTable.__contains__ hashes the key and scans one bucket; O(1) average.    |
| `has_edge`        | O(degree)     | Calls get_neighbors then scans the returned list linearly.                    |
| `get_neighbors`   | O(1) avg      | Returns the stored list directly after a single HashTable.get lookup.         |
| `bfs`             | O(V + E)      | Each node is enqueued once and each edge is examined once.                    |
| `dfs`             | O(V + E)      | Same visit-once property as BFS; iterative with an explicit stack.            |
| `shortest_path`   | O(V + E)      | BFS-based; stops early when the target is found but worst case visits all nodes and edges. |

---

## 3. Benchmark Results

```
============================================================================
Graph Performance Benchmark  (best of 3 runs)
Edge factor: 3x  |  has_node queries: 500  |  shortest_path pairs: 20
============================================================================
 Nodes |          Build |       has_node |            BFS |            DFS |   ShortestPath
-------------------------------------------------------------------------------------------
   100 |          1.077 |          0.131 |          0.321 |          0.359 |          0.285
   500 |          6.277 |          0.133 |          1.634 |          1.805 |          0.263
  1000 |         13.956 |          0.137 |          3.335 |          3.678 |          0.257
============================================================================
```

---

## 4. Space Complexity

The graph uses O(V + E) memory. V is the number of nodes, each contributes one entry in _adj and one in _data. E is the number of directed edges, each contributes one tuple in the adjacency list of its source node. The HashTable buckets hold at most O(V) entries in _adj and O(V) in _data, while the adjacency lists collectively hold O(E) tuples, giving O(V + E) total.

---

## 5. Reflection Questions

**Q1.** BFS and DFS both visit every reachable node exactly once.
Why might BFS be preferred for `shortest_path` even though both are O(V + E)?

BFS explores nodes level by level, so the first time it reaches the destination it's guaranteed to have taken the minimum number of edges. DFS may reach the destination via a long detour first, requiring backtracking or a full traversal before the true shortest path can be identified. For unweighted graphs, BFS finds the shortest path without any additional tracking.

---

**Q2.** Your adjacency list uses O(V + E) space. An adjacency *matrix* uses O(V^2).
For the NPC dialog trees in this lab (small, sparse graphs), which representation is
more appropriate? Would your answer change for a 10,000-node social network graph?

For the dialog trees in this lab, the adjacency list is more appropriate. Each NPC graph has only 5-6 nodes and little edges, so V^2 would add to a lot of overhead. For a 10,000-node social network where each user connects to dozens of others, the adjacency list is still more appropriate because social networks are sparse (E << V^2); an adjacency matrix would waste 10^8 cells to store a fraction of that many edges.

---

**Q3.** Compare your `bfs` timing to networkx's (if you ran the comparison).
What accounts for the difference? Is networkx faster or slower, and why?

The comparison against networkx was not run for this lab. Networkx would be faster at large scales. This implementation uses a custom HashTable backed by an ArrayList, which adds overhead from Python-level looping, ArrayList bounds checks, and hash computation for every operation.

---

## 6. Conclusions

The implementation shows linear growth in BFS/DFS time as graph size increases, which is consistent with the expected O(V + E) complexity. The has_node time stays nearly constant across sizes, confirming O(1) average performance for the HashTable lookup.

---

## 7. References

- Course lecture slides on graph algorithms and adjacency list representations.
- AI tool usage logged in `ai_conversations.md`.
