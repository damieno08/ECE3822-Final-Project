import os
import sys

start_path = str(sys.path[0])

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

class Luaianid(Game):

    def __init__(self, user):
        super().__init__(user, "Luaianid")

    def start_game(self):
        start_string = "python3 /home/damien/ECE3822/projects/ECE3822-Final-Project/game_interaction/games/Luainid/code/game/main.py " + self.user
        print(start_string)
        os.system(start_string)


games = [Luaianid("Damien")]