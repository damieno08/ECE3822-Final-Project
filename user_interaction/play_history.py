from user_interaction.history import History

class Play_history(History):
    def __init__(self, time):

        # Inheret the history class
        super().__init__()

        # Save time the message was sent
        self.time = time
        
        # add more data related to play history...