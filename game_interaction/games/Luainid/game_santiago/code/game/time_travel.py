"""
time_travel.py - Time travel system using stacks

Implements rewind/replay functionality for single-player mode.
Disabled when multiple players are connected.

Author: Santiago Troya
Date:   04/10/2026
Lab:    Lab 6 - Sparse World Map
"""

from datastructures.stack import Stack


class GameState:
    """
    Represents a snapshot of the game state at a single point in time.
    """

    def __init__(self, player_x, player_y, timestamp):
        """
        Create a game state snapshot.

        Args:
            player_x  (float): Player's x position.
            player_y  (float): Player's y position.
            timestamp (int):   Frame number when this state was recorded.
        """
        self.player_x = player_x
        self.player_y = player_y
        self.timestamp = timestamp

    def __repr__(self):
        """String representation for debugging."""
        return f"GameState(x={self.player_x:.1f}, y={self.player_y:.1f}, frame={self.timestamp})"


class TimeTravel:
    """
    Manages game state history for rewind/replay functionality.

    Uses two stacks:
    - history: Past states (what we have done).
    - future:  Future states (available after rewinding).

    Note: Only works in single-player mode.
    """

    def __init__(self, max_history=180, sample_rate=10):
        """
        Initialize the time travel system.

        Args:
            max_history (int): Maximum number of states to remember
                               (default: 180 states).
            sample_rate (int): Record every N frames (default: 10).
                               sample_rate=10 → 180 states ≈ 30 seconds at 60 FPS.
        """
        self.history = Stack()
        self.future = Stack()
        self.max_history = max_history
        self.sample_rate = sample_rate
        self.frame_counter = 0
        self.frames_counted_since_last_record = 0
        self.rewinding = False

    def record_state(self, player_x, player_y):
        """
        Record the current game state (sampled based on sample_rate).

        Called every frame but only stores a snapshot every sample_rate frames.
        Recording clears the future stack so that rewinding after new movement
        discards the stale forward history.

        Args:
            player_x (float): Current player x position.
            player_y (float): Current player y position.
        """
        self.frames_counted_since_last_record += 1

        if self.frames_counted_since_last_record >= self.sample_rate:
            state = GameState(player_x, player_y, self.frame_counter)
            self.history.push(state)

            # Trim oldest entry when history is full
            if self.history.size() > self.max_history:
                temp = Stack()
                while not self.history.is_empty():
                    temp.push(self.history.pop())
                temp.pop()  # discard the oldest (now on top)
                while not temp.is_empty():
                    self.history.push(temp.pop())

            self.future.clear()
            self.frames_counted_since_last_record = 0

        self.frame_counter += 1

    def can_rewind(self):
        """
        Check if rewinding is possible.

        Returns:
            bool: True if history has at least 2 states (need one to go back to).
        """
        return self.history.size() >= 2

    def can_replay(self):
        """
        Check if replaying forward is possible.

        Returns:
            bool: True if the future stack has states (we have rewound).
        """
        return not self.future.is_empty()

    def rewind(self):
        """
        Go back one step in time.

        Pops the current state from history onto the future stack, then
        returns the new top of history (the previous position).

        Returns:
            GameState | None: The state to restore to, or None if cannot rewind.
        """
        if not self.can_rewind():
            return None
        current = self.history.pop()
        self.future.push(current)
        return self.history.peek()

    def replay(self):
        """
        Go forward one step in time (after rewinding).

        Pops the next state from the future stack back onto history and
        returns it.

        Returns:
            GameState | None: The state to restore to, or None if cannot replay.
        """
        if not self.can_replay():
            return None
        next_state = self.future.pop()
        self.history.push(next_state)
        return next_state

    def get_history_size(self):
        """Return the number of states stored in history."""
        return self.history.size()

    def get_future_size(self):
        """Return the number of states available for replay."""
        return self.future.size()

    def clear(self):
        """
        Clear all history and future states.

        Call this when switching levels or starting a new game.
        """
        self.history.clear()
        self.future.clear()
