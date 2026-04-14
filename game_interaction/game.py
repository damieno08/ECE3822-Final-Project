
class Game:
    
    # basic initialization for making name of game and user
    def __init__(self,user, name):
        self.name = name
        self.user = user

    # empty start_game function to be overwritten by subclass
    def start_game(self):
        pass


    # empty end_game function to be overwritten by subclass
    def end_game(self):
        pass