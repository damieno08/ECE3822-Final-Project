"""
This program will define the playhistory class for the arcade project of ECE3822

Revision History:
    (RL) 04/13/2026 Create initial program

"""

from user_interaction.history import History

class Play_history(History):
    def __init__(self, time):

        # Inheret the history class
        super().__init__()

        # Save time the message was sent
        self.time = time
        
        # add more data related to play history...