"""
patrol_path.py - Linked list implementation for NPC patrol paths

Implements different types of linked lists for NPC movement:
- Singly linked list (one-way patrol)
- Circular linked list (looping patrol)
- Doubly linked list (back-and-forth patrol)

Author: Damien Ortiz
Date: 04/02/2026
Lab: Lab 5 - NPC Patrol Paths with Linked Lists
"""

from game_interaction.games.game_damien.code.game.datastructures.waypoint import Waypoint


class PatrolPath:
    """
    A linked list of waypoints that defines how an NPC moves.

    Supports three patrol types:
    - "one_way": Walk through waypoints once, then stop
    - "circular": Loop through waypoints infinitely
    - "back_and_forth": Walk forward to end, then reverse back to start
    """

    def __init__(self, patrol_type="circular"):
        """
        Initialize an empty patrol path.

        Args:
            patrol_type (str): Type of patrol - "one_way", "circular", or "back_and_forth"
        """
        
        # Create linked list with no nodes yet
        self.head = None
        self.tail = None
        self.current = None
        self.patrol_type = patrol_type
        self.size = 0
        self.direction = 1  # 1 = forward, -1 = backward

    def add_waypoint(self, x, y, wait_time=0):
        """
        Add a waypoint to the end of the patrol path.
        """

        # Create node to add to list
        new_node = Waypoint(x, y, wait_time)

        # Check if the list is empty then add node
        if self.is_empty():
            # First node initialization
            self.head = self.tail = self.current = new_node
            # Self-reference for circular with only 1 node
            if self.patrol_type == "circular":
                new_node.next_pointer = new_node
                new_node.prev_pointer = new_node
        else:
            # Link existing tail to new node
            self.tail.next_pointer = new_node
            
            # Set back pointer for types that require it
            if self.patrol_type != "one_way":
                new_node.prev_pointer = self.tail
            
            # Move tail forward
            self.tail = new_node

            # Finalize based on type
            if self.patrol_type == "circular":
                # Close the loop
                self.tail.next_pointer = self.head
                self.head.prev_pointer = self.tail
            else:
                # Ensure non-circular paths end at None
                self.tail.next_pointer = None

        # Increase our size after adding a new waypoint
        self.size += 1

    def get_next_waypoint(self):
        """
        Get the next waypoint in the patrol sequence and update the current position.

        Returns:
            Waypoint: The waypoint to move toward, or None if patrol is complete.
        """

        # Check that our list is not empty or there is no next pointer
        if self.is_empty() or self.current is None:
            return None

        # Store current to return it
        result = self.current

        # Advance the 'current' pointer for the NEXT call
        if self.patrol_type == "one_way":
            self.current = self.current.next_pointer

        elif self.patrol_type == "circular":
            self.current = self.current.next_pointer

        elif self.patrol_type == "back_and_forth":
            if self.direction == 1:
                # Moving forward
                if self.current == self.tail:
                    self.direction = -1
                    self.current = self.current.prev_pointer
                else:
                    self.current = self.current.next_pointer
            else:
                # Moving backward
                if self.current == self.head:
                    self.direction = 1
                    self.current = self.current.next_pointer
                else:
                    self.current = self.current.prev_pointer

        # Return where we went next
        return result

    def reset(self):
        """Reset patrol to the beginning."""

        # Return to start and make head current node
        self.current = self.head
        self.direction = 1

    def __len__(self):
        """Return the number of waypoints."""
        return self.size

    def __iter__(self):
        """Standard linked list iterator."""
        self._iter_current = self.head
        return self

    def __next__(self):
        """Returns the next node in the sequence (head to tail)."""
        if self._iter_current is None:
            raise StopIteration
            
        result = self._iter_current
        
        # Stop iteration after tail to avoid infinite circular loops in 'for' loops
        if self._iter_current == self.tail:
            self._iter_current = None
        else:
            self._iter_current = self._iter_current.next_pointer
            
        return result

    def is_empty(self):
        """Check if path has any waypoints."""
        return self.head is None

    def get_path_info(self):
        """Return a summary of the path state."""
        return {
            "type": self.patrol_type,
            "length": len(self),
            "current": str(self.current) if self.current else "None",
            "direction": self.direction if self.patrol_type == "back_and_forth" else "N/A"
        }
