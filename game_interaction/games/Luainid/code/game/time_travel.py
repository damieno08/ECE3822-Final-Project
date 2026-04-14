"""
time_travel.py - Time travel system using stacks

Implements rewind/replay functionality for single-player mode.
Disabled when multiple players are connected.

Author: Damien Ortiz
Date: 02/20/2026
Lab: Lab 4 - Time Travel with Stacks
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
            player_x (float): Player's x position
            player_y (float): Player's y position
            timestamp (int): Frame number when this state was recorded
        """

        # Set all player values 
        self.player_x = player_x
        self.player_y = player_y
        self.timestamp = timestamp
    
    def __repr__(self):
        """String representation for debugging"""
        return f"GameState(x={self.player_x:.1f}, y={self.player_y:.1f}, frame={self.timestamp})"


class TimeTravel:
    """
    Manages game state history for rewind/replay functionality.
    
    Uses two stacks:
    - history: Past states (what we've done)
    - future: Future states (available after rewinding)
    
    Note: Only works in single-player mode!
    """
    
    def __init__(self, max_history=180, sample_rate=10):
        """
        Initialize the time travel system.
        
        Args:
            max_history (int): Maximum number of states to remember 
                              (default: 180 states)
            sample_rate (int): Record every N frames (default: 10)
                              sample_rate=5 means 180 states = 15 seconds at 60 FPS
                              sample_rate=10 means 180 states = 30 seconds at 60 FPS
        """
        # Create a stack for the past and future
        self.history = Stack()
        self.future = Stack()

        # Store a maximum number of frames we can store
        self.max_history = max_history

        # Store our unchangable sample rate
        self.__sample_rate = sample_rate

        # Create counters for frames
        self.__frame_counter = 0
        self.__frames_since_last_record = 0

        # Make rewinding false on start
        self._rewinding = False
    
    def record_state(self, player_x, player_y):
        """
        Record the current game state (sampled based on sample_rate).
        
        This should be called every frame, but only records every N frames
        based on sample_rate.
        
        Args:
            player_x (float): Current player x position
            player_y (float): Current player y position
        """
        # TODO: Increment frames_since_last_record
        # TODO: Check if frames_since_last_record >= sample_rate
        # TODO: If yes:
        #   - Create a GameState with the current position and frame counter
        #   - Push the new state onto the history stack
        #   - If history stack size exceeds max_history, remove the oldest state
        #     Hint: You'll need to remove from the BOTTOM of the stack
        #     This is tricky with a stack! Consider using a temporary stack
        #   - Clear the future stack (new actions invalidate redo)
        #   - Reset frames_since_last_record to 0
        # TODO: Always increment the frame counter

        # Increment frames from recording
        self.__frames_since_last_record+=1

        # Check if we have enough frames for a sample
        if self.__frames_since_last_record >= self.__sample_rate:

            # If we do, push the gamestate to the stack
            self.history.push(GameState(player_x, player_y, self.__frame_counter))

            # If our history is full do the following
            if self.history.size() > self.max_history:

                # Create a temporary stack, pop all values to it, pop the last value, then 
                # repush all values to original stack
                temp_stack = Stack()
                while self.history.size() > 1:
                    temp_stack.push(self.history.pop())
                self.history.pop()
                while not temp_stack.is_empty():
                    self.history.push(temp_stack.pop())

            # Clear our future stack
            self.future.clear()

            # Fix frame counts
            self.__frames_since_last_record = 0
        self.__frame_counter+=1
    
    def can_rewind(self):
        """
        Check if rewinding is possible.
        
        Returns:
            bool: True if we can rewind (history has at least 2 states)
            
        Note: We need at least 2 states because we need to keep the current state
              and go back to the previous one.
        """

        # Check that we have at least 2 states to swap between
        return self.history.size() >= 2
    
    def can_replay(self):
        """
        Check if replaying forward is possible.
        
        Returns:
            bool: True if future stack has states (we've rewound and can go forward)
        """

        # If the future is not empty tell use we can replay
        return not self.future.is_empty()
    
    def rewind(self):
        """
        Go back one frame in time.
        
        Returns:
            GameState or None: The previous state to restore to, or None if can't rewind
            
        Algorithm:
            1. Check if we can rewind (need at least 2 states in history)
            2. Pop the current state from history
            3. Push that state onto the future stack (so we can replay later)
            4. Peek at the new top of history (this is where we rewind to)
            5. Return that state
        """

        # Check that we have values in history stack
        if not self.can_rewind():
            # If not, return none
            return None
        
        # If we do, pop a gamestate from history and push it to future
        self.future.push(self.history.pop())

        # Return the latest history gamestate
        return self.history.peek()

    def replay(self):
        """
        Go forward one frame in time (after rewinding).
        
        Returns:
            GameState or None: The next state to restore to, or None if can't replay
            
        Algorithm:
            1. Check if we can replay (future stack must not be empty)
            2. Pop the next state from the future stack
            3. Push it back onto the history stack
            4. Return that state
        """

        # Make sure replaying is allowed
        if not self.can_replay():

            # Return None if not
            return None
        
        # Pop the future state and push it to the history stack
        state = self.future.pop()
        self.history.push(state)

        # Return the state we just pushed
        return state
        
    
    def get_history_size(self):
        """Get number of states in history"""

        # Return the size of the history stack
        return self.history.size()
    
    def get_future_size(self):
        """Get number of states in future (available for replay)"""

        # Return the size of future stack
        return self.future.size()
    
    def clear(self):
        """
        Clear all history and future states.
        Call this when switching levels or starting a new game.
        """

        # Clear all values in both stack
        self.history.clear()
        self.future.clear()