"""
hash_table.py - Hash Table implementation

Only required if you implement SparseMatrix using DOK (Option A).

Author:
Date:   
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent_dir)  # Add parent directory to path
sys.path.insert(0, parent_dir)

from datastructures.array import ArrayList

class HashTable:

    def __init__(self, initial_capacity=64):
        self.capacity = initial_capacity
        self.hash_table = ArrayList(self.capacity) # declare inital arraylist
        self.size = 0 # delcare size of 0 upon initialization

        # initialize array to None
        for e in range(self.hash_table.capacity):
            self.hash_table.append(None)
        # DONE

    def _hash(self, key):

        # key is a tuple(row, col)
        row, col = key

        # combine using a prime multiplier
        h = 17
        h = h * 31 + row
        h = h * 31 + col

        # use the golden ratio
        phi = 0x9e3779b9
        h ^= (h >> 16)
        h *= phi
        h ^= (h >> 13)
        h *= phi
        h ^= (h >> 16)

        return h % self.capacity
    
        # DONE: implement your own hash function — do not use Python's hash()

    def set(self, key, value, trigger_resize=True):
        idx = self._hash(key)
        # if bucket at index, idx, already has element, append value to bucket at idx
        if self.hash_table[idx] is None:
            self.hash_table[idx] = ArrayList()

        bucket = self.hash_table[idx]

        # check if key already exists to update it
        for i in range(bucket.__len__()):
            if bucket[i][0] == key:
                bucket[i][1] = value
                return
        # If key wasn't found, add new entry
        bucket.append([key, value])
        self.size += 1

        # check if need to resize
        if( trigger_resize and (self.size / self.capacity > 0.75)):
            self._resize()
        
        
        # if(self.hash_table[idx] is not None):
        #     bucket = self.hash_table[idx]
        #     # search for key in bucket and then append value
        #     for i in range(bucket.__len__()):
        #         if bucket[i][0] == key:
        #             bucket[i][1] = value
        #             return

        #     # append value if key wasn't found
        #     bucket.append([key ,value])
        #     self.size += 1

        # # if bucket doesn't exist, create new bucket and then append
        # if( self.hash_table[idx] is None):
        #     new_bucket = ArrayList()
        #     self.hash_table[idx] = new_bucket
        #     new_bucket.append([key, value])
        #     self.size += 1

            
        # DONE

    def get(self, key, default=None):
        # hash key to idx and assign bucket
        idx = self._hash(key)
        bucket = self.hash_table[idx]
        # if bucket is not empty
        # perform search on bucket for the target "key, value" pair
        if(bucket is not None):
            for value in range(bucket.__len__()):
                # assign bucket of "value" to target
                target = bucket[value]
                # check key of target vs key passed in, return value if true
                if(target[0] == key):
                    return target[1]

        # return default if not found
        return default
        # DONE

    def delete(self, key):
        # # hash key to idx and assign bucket
        # idx = self._hash(key)
        # bucket = self.hash_table[idx]
        # # find bucket with target key value
        # for i in range(bucket.__len__()):
        #     # if first entry of bucket[i] equals key, delete bucket[i]
        #     if(bucket[i][0] == key):
        #         bucket.remove(bucket[i])
        #         self.size -= 1
        #         return True

        # # return False if no key
        # return False

        idx = self._hash(key)
        bucket = self.hash_table[idx]

        if bucket is None:
            return False

        for i in range(bucket.__len__()):
            if bucket[i][0] == key:
                bucket.remove(bucket[i])
                self.size -= 1
                return True
            
        return False
        
        # DONE

    def __contains__(self, key):
        # hash key to idx and assign bucket
        idx = self._hash(key)
        bucket = self.hash_table[idx]

        # check if bucket is None
        if( bucket is None):
            return False
        
        # search bucket for key passed in
        for i in range(bucket.__len__()):
            # if first entry of bucket[i] equals key, return True
            if(bucket[i][0] == key):
                return True

        # otherwise return False
        return False
        # DONE

    def __len__(self):
        # return number of elements in array
        return self.size
        # DONE

    def items(self):
        # returns a list of items stored in hash table
        items_list = ArrayList()
        for a in range(self.hash_table.__len__()):
            bucket = self.hash_table[a]
            if(bucket is not None):
                for b in range(len(bucket)):
                    if(bucket[b] is not None):
                        items_list.append(bucket[b])

        # return list of items
        return items_list
        # DONE


    def _resize(self):
        # resize hash table by doubling size
        original_hash = self.hash_table
        original_size = original_hash.__len__()
        self.capacity = original_size * 2

        # declare new array and initialize bucket arrays, set size to 0
        self.hash_table = ArrayList(self.capacity)
        self.size = 0


        for i in range(self.capacity):
            self.hash_table.append(None)

        for idx in range(original_size):
            bucket = original_hash[idx]
            if bucket is not None:
                for i in range(bucket.__len__()):
                    data = bucket[i]
                    self.set(data[0], data[1], trigger_resize=False)
                
        # DONE
