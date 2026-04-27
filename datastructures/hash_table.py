"""
hash_table.py - Hash Table implementation

A custom HashTable implementation using Open Addressing with Quadratic Probing.
This is used as the backing storage for a SparseMatrix in a Dictionary of Keys 
(DOK) format.

Author: Damien Ortiz
Date:   04/10/2026
Lab:    Lab 6 - Sparse World Map
"""

from datastructures.array import ArrayList

class HashTable:
    """
    A hash table that maps unique keys to values.
    Uses Quadratic Probing to handle collisions and a Multiplicative Hash.
    """

    def __init__(self, initial_capacity=64):
        """
        Initializes the HashTable.

        Args:
            initial_capacity (int): The starting number of available bins.
        """
        self.capacity = initial_capacity
        self.number_elements = 0
        
        # Initialize the backing ArrayList with the starting capacity
        self.bins = ArrayList(self.capacity)
        
        # Fill the ArrayList with None to allocate addressable memory
        # This allows __getitem__ and __setitem__ to work on indices up to capacity
        for _ in range(self.capacity):
            self.bins.append(None)

    def _hash(self, key):
        """
        Calculates the index for a given key using the Multiplicative Method.
        Supports tuple keys (row, col) for sparse matrix indexing.

        Args:
            key: The key to hash (tuple or int).
        
        Returns:
            int: A valid index within the current capacity.
        """
        # If key is a coordinate tuple, combine into a single large integer
        if isinstance(key, tuple):
            # Shift row by 16 bits and XOR with column to create a unique key
            combined_key = (key[0] << 16) ^ key[1]
        elif isinstance(key, str):
            combined_key = hash(key)
        else:
            combined_key = key

        # Multiplicative hash formula: floor(capacity * (key * A mod 1))
        A = 0.6180339887  # Fractional part of the Golden Ratio
        fractional_part = (abs(combined_key) * A) % 1
        return int(self.capacity * fractional_part)

    def set(self, key, value):
        """
        Inserts or updates a key-value pair in the table.
        Triggers a resize if the load factor exceeds 0.7.

        Args:
            key: The key to store.
            value: The value associated with the key.
        """
        # Check load factor; if > 70% full, double the size
        if self.number_elements / self.capacity > 0.7:
            self._resize()

        start_hash = self._hash(key)
        
        # Search for an empty slot or the existing key using Quadratic Probing
        for i in range(self.capacity):
            index = (start_hash + i * i) % self.capacity
            entry = self.bins[index]

            # if slot is empty, insert new data
            if entry is None:
                self.bins[index] = (key, value)
                self.number_elements += 1
                return
            
            # if key matches, update the existing value
            if entry[0] == key:
                self.bins[index] = (key, value)
                return

    def get(self, key, default=None):
        """
        Retrieves the value associated with a key.

        Args:
            key: The key to look up.
            default: The value to return if the key is not found.

        Returns:
            The stored value or the provided default.
        """
        start_hash = self._hash(key)
        
        # Search using the same Quadratic Probing sequence as 'set'
        for i in range(self.capacity):
            index = (start_hash + i * i) % self.capacity
            entry = self.bins[index]
            
            # If we hit None, the key was never inserted
            if entry is None:
                return default
            
            # If keys match, we found our value
            if entry[0] == key:
                return entry[1]
                
        return default

    def delete(self, key):
        """
        Removes a key-value pair from the table.

        Args:
            key: The key to remove.
        """
        start_hash = self._hash(key)
        
        for i in range(self.capacity):
            index = (start_hash + i * i) % self.capacity
            entry = self.bins[index]
            
            if entry is None:
                return # Key not found, nothing to delete
            
            if entry[0] == key:
                # Clear the slot and update the element count
                self.bins[index] = None
                self.number_elements -= 1
                return

    def __contains__(self, key):
        """Enables the 'in' operator: if key in table."""
        return self.get(key) is not None

    def __len__(self):
        """Enables the len() function: returns number of stored elements."""
        return self.number_elements

    def items(self):
        """
        Returns an ArrayList of all stored (key, value) tuples.
        Used for iterating over the sparse matrix non-default entries.
        """
        item_list = ArrayList()
        for i in range(self.capacity):
            entry = self.bins[i]
            if entry is not None:
                item_list.append(entry)
        return item_list

    def _resize(self):
        """
        Doubles the capacity of the table and re-hashes all existing entries.
        Ensures collision chains are rebuilt for the new capacity.
        """
        old_bins = self.bins
        self.capacity *= 2
        self.number_elements = 0
        
        # Create a new, larger ArrayList
        self.bins = ArrayList(self.capacity)
        
        # Re-fill the new bins with None
        for _ in range(self.capacity):
            self.bins.append(None)

        # Iterate through old bins and re-insert items into the new bins
        # We must use 'set' so the items are hashed based on the NEW capacity
        for i in range(len(old_bins)):
            entry = old_bins[i]
            if entry is not None:
                self.set(entry[0], entry[1])