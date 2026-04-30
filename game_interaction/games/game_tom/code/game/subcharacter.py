"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

import pygame
import sys
from game_interaction.games.game_tom.code.game.character import Character
from game_interaction.games.game_tom.code.game.item import Weapon
from datetime import datetime

start_path = str(sys.path[0])


class Character1(Character):
    """Class Name: Fire Class"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)

        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/game_interaction/games/game_tom/graphics/characters/Salamus.png').convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
            
        self.character_name = "Salamus"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 10, 10
        self.speed = 6
        
        # # Load image for remote players or as fallback
        # try:
        #     self.image = pygame.image.load('/game_interaction/games/game_tom/graphics/characters/Salamus.png').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        #     self.hitbox = self.rect.inflate(0, -26)
        # except:
        #     pass
            
        # # Load animations for local player
        # if is_local:
        #     self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Salamus"
    
    @staticmethod
    def get_description():
        return "A salamnder, member of the fire class. Quick to react and be agitated."
    
    @staticmethod
    def get_preview_image():
        return start_path + "/game_interaction/games/game_tom/graphics/characters/Salamus.png"


class Water(Character):
    """Class Name: Water Class"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)

        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/game_interaction/games/game_tom/graphics/characters/Olive.png').convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        
        self.character_name = "Olivius"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 10, 10
        self.speed = 4  # Faster than others
        
        # try:
        #     self.image = pygame.image.load('../../graphics/characters/Olive.png').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        #     self.hitbox = self.rect.inflate(0, -26)
        # except:
        #     pass
            
        # if is_local:
        #     self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Olivius"
    
    @staticmethod
    def get_description():
        return "An otter, a member of the water class. "
    
    @staticmethod
    def get_preview_image():
        return start_path + "/game_interaction/games/game_tom/graphics/characters/Olive.png"


class Earth(Character):
    """Class Name: Earth Class"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)

        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/game_interaction/games/game_tom/graphics/characters/Wendl.png').convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)        
        
        self.character_name = "Wendius"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 5, 5
        
        # try:
        #     self.image = pygame.image.load('../../graphics/characters/Wendl.png').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        #     self.hitbox = self.rect.inflate(0, -26)
        # except:
        #     pass
            
        # if is_local:
        #     self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Wendius"
    
    @staticmethod
    def get_description():
        return "A wolf, a member of the Earth Class."
    
    @staticmethod
    def get_preview_image():
        return start_path + "/game_interaction/games/game_tom/graphics/characters/Wendl.png"


class Air(Character):
    """Class Name: Air"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)

                # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/game_interaction/games/game_tom/graphics/characters/Ernesto.png').convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        self.character_name = "Erneus"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 4, 6
        self.speed = 30
        
        # try:
        #     self.image = pygame.image.load('../../graphics/characters/Ernesto.PNG').convert_alpha()
        #     self.rect = self.image.get_rect(topleft=pos)
        #     self.hitbox = self.rect.inflate(0, -26)
        # except:
        #     pass
            
        # if is_local:
        #     self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Erneus"
    
    @staticmethod
    def get_description():
        return "A Hawk, swift and agile, good as a scout."
    
    @staticmethod
    def get_preview_image():
        return start_path + "/game_interaction/games/game_tom/graphics/characters/Ernesto.png"

def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character' or cls.__name__.startswith('Character'):
            character_classes.append(cls)
    return character_classes

