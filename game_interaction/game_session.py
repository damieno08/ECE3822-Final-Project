from datetime import datetime
import time

class GameSession:

    def __init__(self, user, game_name):
        self.score = 0
        self.created_time = datetime.now()
        self.end_time = None
        self.user = user
        self.game_name = game_name

    def end_session(self):
        self.end_time = datetime.now()
        return self.end_time

    def get_time_played(self):
        return self.end_time - self.created_time
    
    def is_active(self):
        return self.end_time == None


