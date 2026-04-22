"""
This program will define the play_history class for the arcade project of ECE3822

Revision History:
    (ALL) 04/10/2026 Create initial program
    (RL)  04/22/2026 Create some methods
"""

from game_interaction.game_session import GameSession
from user_interaction.history import History

class Play_history(History):
    def __init__(self, time):

        # Inheret the history class
        super().__init__()

        # Save time the message was sent
        self.time = time
        
        # add more data related to play history...

    def pop(self):
        """
        Gives the most recent session
        """
        return self._history.pop()
    
    def size(self):
        """
        Total number of games played
        """
        return self._history.size()

    def get_total_time(self):
        """
        Total playtime
        """
        total = 0
        sessions = self._history.get_array()

        for session in sessions:
            total += session.get_time_played().total_seconds()
        
        return total

    def get_history(self, idx=-1):
        """
        Get session by index
        """
        return self._history.peek(idx)
