from history import History

class Chat_history(History):
    def __init__(self, time, message):

        # Inheret the history class
        super().__init__(self)

        # Save time the message was sent
        self.time = time
        
        # Save message sent
        self.message = message