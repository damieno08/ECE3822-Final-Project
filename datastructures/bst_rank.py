"""
bst_rank.py - Self-Balancing Binary Search Tree (AVL). With Rank included
Author: Paul Garrison
"""

class Node:
    def __init__(self, value):
        self.value = value      # score
        self.users = set()     # all users with this score
        self.left = None
        self.right = None
        self.height = 1
        self.size = 0          # total USERS, not nodes

class BST:
    def __init__(self):
        self._root = None

    def _get_height(self, node):
        # find height of current node
        return node.height if node else 0

    def _get_size(self, node):
        # find number of children of node
        return node.size if node else 0

    def _get_balance(self, node):
        # figure out if we need to rebalance
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _update(self, node):
        """
        Updates height and size after changes. 
        """
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.size = len(node.users) + self._get_size(node.left) + self._get_size(node.right)

    def _rotate_right(self, y):
        """
        Function will rebalance tree by shifting to the right
        """
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x):
        """
        Function will rebalance tree by shifting to the left
        """
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update(x)
        self._update(y)
        return y

    def insert(self, value):
        # return new root
        self._root = self._insert_recursive(self._root, value)

    def _insert_recursive(self, node, value):
        """
        Inserts (score, user) into AVL tree.
        Supports true ties by grouping users with same score.
        """
        
        score, user = value
        
        # if there is no root, make it root
        if not node:
            new_node = Node(score)
            new_node.users.add(user)  # store user in tie group
            self._update(new_node)
            return new_node

        
        # make left if less
        if score < node.value:
            node.left = self._insert_recursive(node.left, value)

        # make right if greater
        elif score > node.value:
            node.right = self._insert_recursive(node.right, value)
        
        # Tie case: same score goes into same node
        else:
            node.users.add(user)
            self._update(node)
            return node

        # change height counts and children count
        self._update(node)

        # figure out if tree needs to be rebalanced
        balance = self._get_balance(node)

        # if heavy left side, shift right
        if balance > 1 and score < node.left.value:
            return self._rotate_right(node)
        
        # if heavy right side, shift left
        if balance < -1 and score > node.right.value:
            return self._rotate_left(node)
            
        # left side heavy right
        if balance > 1 and score > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # right side heavy left
        if balance < -1 and score < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        # return new node location
        return node

    def search(self, key):
        # search through tree until we find the key
        curr = self._root

        # loop and break if we find it
        while curr:
            if key == curr.value: return curr.value
            curr = curr.left if key < curr.value else curr.right

        # return none if not found
        return None

    def delete(self, key):
        # return new root
        self._root = self._delete_recursive(self._root, key)

    def _delete_recursive(self, node, key):
        """
        Deletes (score, user) from AVL tree.
        Handles ties by removing user from node.users first.
        """
        # if not found, root stays the same
        if not node: return None
        score, user = key  # key = (score, user)
        # traverse tree until we find the node
        # Compare ONLY by score
        if score < node.value:
            node.left = self._delete_recursive(node.left, key)
        elif score > node.value:
            node.right = self._delete_recursive(node.right, key)
        else:
            """
            Found the node with matching score. remove the user from this node first.
            """
            # Remove user from tie group
            node.users.discard(user)

            # If other users still share this score, keep node
            if len(node.users) > 0:
                self._update(node)
                return node

            """
            No users remain → delete node normally
            """
            # find if we have one or no children
            if not node.left:
                return node.right

            if not node.right:
                return node.left
            
            # if two children, find the smallest node on the right to replace. replace with inorder successor
            temp = self._get_min_node(node.right)

            node.value = temp.value
            node.users = temp.users.copy()
            # Remove one user from successor node
            node.right = self._delete_recursive(
                node.right,
                (temp.value, next(iter(temp.users)))
            )

        # update height of tree
        self._update(node)

        # find if we're balanced
        balance = self._get_balance(node)
        
        # check if we are left heavy
        if balance > 1:
            if self._get_balance(node.left) >= 0:
                # rotate tree right
                return self._rotate_right(node)
            else:
                # shift left then right
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        # check if tree right heavy
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                # rotate tree left
                return self._rotate_left(node)
            else:
                # shift right then left
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        # return new root
        return node

    def find_min(self):
        # return the minimum node
        if not self._root: return None
        return self._get_min_node(self._root).value

    def _get_min_node(self, node):
        curr = node
        # loop to bottom left of tree
        while curr.left: curr = curr.left
        # return min
        return curr

    def find_max(self):
        # if tree empty return none
        if not self._root: return None
        curr = self._root
        # loop right side of tree
        while curr.right: curr = curr.right
        # return value at max
        return curr.value

    def inorder(self):
        res = []
        # walk through each node
        def _walk(node):
            if node:
                _walk(node.left)
                res.append(node.value)
                _walk(node.right)
        _walk(self._root)
        # return entire tree list
        return res

    def find_rank(self, key):
        """
        Returns number of users with strictly higher score.
        Best score is rank 0.
        """

        score, user = key

        def _rank(node):
            if not node:
                return 0
            
            # If current node score is LESS → all right side is higher
            if score < node.value:
                return (
                    self._get_size(node.right) +
                    len(node.users) +
                    _rank(node.left)
                )

            # If current node score is GREATER → go right only
            elif score > node.value:
                return _rank(node.right)

            # Found score node → everything in right subtree is higher
            else:
                return self._get_size(node.right)
            
        return _rank(self._root)   

    def kth_smallest(self, k):
        """
        Returns k-th smallest USER (by score order).
        Smallest score group starts at k = 1.
        """
        
        def _kth(node, k):
            if not node:
                return None
            
            # size of LEFT subtree (these are smaller scores)
            left_size = self._get_size(node.left)
            
            # Case 1: go left
            if k <= left_size:
                return _kth(node.left, k)
            
            # Case 2: current node (tie group)
            if k <= left_size + len(node.users):
                return (node.value, next(iter(node.users)))
            
            # Case 3: go right
            return _kth(node.right, k - left_size - len(node.users))
        
        return _kth(self._root, k)
    
    def kth_largest(self, k):
        """
        Returns the k-th largest USER (by score order).
        This is implemented using kth_smallest on reversed index,
        since the tree is ordered ascending by score.
        """

        # Total number of users in the entire tree
        total_users = len(self)

        # Convert kth largest → kth smallest index
        return self.kth_smallest(total_users - k + 1)

    def range_query(self, low, high):
        res = []
        def _range(node):
            if not node: return
            
            # if we can still go lower, go left
            if low < node.value: _range(node.left)
            
            # if value is in between, add to list
            if low <= node.value <= high: res.append(node.value)
            
            # if we can still go higher, go right
            if high > node.value: _range(node.right)
            
        _range(self._root)
        # return list of values found
        return res

    def __len__(self):
        # find the total count of the tree
        return self._get_size(self._root)
