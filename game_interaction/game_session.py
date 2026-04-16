from datetime import datetime
import time

class GameSession:
    
    # intialize game sessions with start time, user, and game
    def __init__(self, user, game_name):
        self.score = 0
        self.start_time = datetime.now()
        self.end_time = None
        self.user = user
        self.game_name = game_name

    # record the time session ended
    def end_session(self):
        self.end_time = datetime.now()
        self.user.update_history("game", self)
        return self.end_time

    # calculate the time session was for
    def get_time_played(self):
        return self.end_time - self.start_time
    
    # check if game is active
    def is_active(self):
        return self.end_time == None


