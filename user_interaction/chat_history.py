from user_interaction.history import History

class Chat_history(History):
    def __init__(self, time):

        # Inheret the history class
        super().__init__()

        self.time  = time
        