"""
hash_table.py - Hash Table implementationBBacks the DOK SparseMatrix. Uses separate chaining for collision resolution.
Each bucket is an ArrayList of (key, value) tuples. The hash function is a
custom polynomial rolling hash — Python's built-in hash() is never called.

Author: Santiago Troya
Date:   04/09/2026
Lab:    Lab 6 - Sparse World Map
"""

from game_interaction.games.game_santiago.code.game.datastructures.array import ArrayList


class HashTable:
    """
    Hash table with separate chaining and dynamic resizing.

    Keys are (row, col) integer tuples, but the implementation also handles
    plain ints and strings so the structure is general-purpose.

    Collision policy : chaining — each bucket slot holds an ArrayList of (key, value) pairs.
    Resize policy: when load factor (len / capacity) exceeds 0.7, capacity is doubled and all entries are rehashed.
    """

    def __init__(self, initial_capacity=64):
        """
        Initialize an empty hash table.

        Args:
            initial_capacity (int): Number of bucket slots to allocate.
                                    Should be a power of 2 for even distribution.
        """
        self.capacity = initial_capacity
        self._size = 0

        self._buckets = ArrayList(self.capacity)
        for _ in range(self.capacity):
            self._buckets.append(None)

    def _hash(self, key):
        """
        Compute a bucket index for key


        Args:
            key: A hashable key — (int, int) tuples are the primary use case.

        Returns:
            int: Bucket index in [0, capacity).

        Raises:
            TypeError: If key type is not supported.
        """
        if isinstance(key, tuple):
            # Polynomial hash: h = 17; for each element h = h*31 + element
            h = 17
            for item in key:
                if isinstance(item, int):
                    h = h * 31 + item
                else:
                    # Fallback: treat other element types as strings
                    for ch in str(item):
                        h = h * 31 + ord(ch)
            return abs(h) % self.capacity

        elif isinstance(key, int):
            # Knuth multiplicative hashing with a large prime
            return abs(key * 2_654_435_761) % self.capacity

        elif isinstance(key, str):
            # djb2 variant
            h = 5381
            for ch in key:
                h = (h * 33) ^ ord(ch)
            return abs(h) % self.capacity

        else:
            raise TypeError(f"HashTable: unsupported key type {type(key)}")

    def set(self, key, value):
        """
        Insert or update a key-value pair.

        Args:
            key:   Hashable key.
            value: Value to associate with the key.
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is None:
            # Create a new chain for this slot
            bucket = ArrayList()
            self._buckets[idx] = bucket

        # Search for an existing entry with the same key
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                # replace the tuple
                bucket[i] = (key, value)
                return

        # Append a new pair when key not present
        bucket.append((key, value))
        self._size += 1

        # Resize if load factor exceeds threshold
        if self._size / self.capacity > 0.7:
            self._resize()

    def get(self, key, default=None):
        """
        Return the value stored under key, or default if absent.

        Args:
            key:     Hashable key to look up.
            default: Value to return when the key is not found.

        Returns:
            The stored value, or default.
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is None:
            return default

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]

        return default

    def delete(self, key):
        """
        Remove the entry with the given key.

        Args:
            key: Key to remove.

        Raises:
            KeyError: If key is not present.
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is not None:
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    bucket.pop(i)
                    self._size -= 1
                    return

        raise KeyError(key)

    def __contains__(self, key):
        """
        Return True if key is stored in the table.

        """
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is None:
            return False

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return True

        return False

    def __len__(self):
        """Return the number of key-value pairs stored in the table."""
        return self._size

    def items(self):
        """
        Yield all (key, value) pairs stored in the table.

        """
        for i in range(self.capacity):
            bucket = self._buckets[i]
            if bucket is not None:
                for j in range(len(bucket)):
                    yield bucket[j]

    def _resize(self):
        """
        Double the bucket capacity and rehash all existing entries.

        """
        old_buckets = self._buckets
        old_capacity = self.capacity

        # Build a table at double capacity
        self.capacity *= 2
        self._buckets = ArrayList(self.capacity)
        for _ in range(self.capacity):
            self._buckets.append(None)
        self._size = 0  # set() will re-increment

        # Re-insert every existing entry into the new table
        for i in range(old_capacity):
            bucket = old_buckets[i]
            if bucket is not None:
                for j in range(len(bucket)):
                    k, v = bucket[j]
                    self.set(k, v)
