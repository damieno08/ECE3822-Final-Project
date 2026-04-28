"""
This program will define the play_history class for the arcade project of ECE3822

Revision History:
    (ALL) 04/10/2026 Create initial program
    (RL)  04/22/2026 Create some methods
"""

from game_interaction.game_session import GameSession
from user_interaction.history import History

class Play_history(History):
    def __init__(self):

        # Inheret the history class
        super().__init__()

    def get_total_time(self):
        """
        Total playtime
        """
        total = 0
        sessions = self._history.get_array()

        for session in sessions:
            if session is not None:
                total += session.get_time_played().total_seconds()
        
        return total
