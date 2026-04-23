
"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

import pygame
from game_interaction.games.game_richard.code.game.character import Character

class SpiritSwordCultivator(Character):
    """SpiritSwordCultivator"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Cleric"
        self.hp, self.max_hp = 120, 120
        self.attack, self.defense = 25, 15
        self.speed = 20
        
        # Load image for remote players or as fallback
        try:
            self.image = pygame.image.load('../../graphics/characters/SpiritSwordCultivator.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        # Load animations for local player
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        # TODO
        return "Spirit Sword Cultivator"
    
    @staticmethod
    def get_description():
        # TODO
        return "Melee warrior, master of sword techniques, focusing on speed and precision."

    @staticmethod
    def get_preview_image():
        # TODO
        return '../../graphics/characters/SpiritSwordCultivator.png'


class BodyCultivator(Character):
    """BodyCultivator"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Hobbit"
        self.hp, self.max_hp = 200, 200
        self.attack, self.defense = 15, 30
        self.speed = 10  # Faster than others
        
        try:
            self.image = pygame.image.load('../../graphics/characters/BodyCultivator.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        # TODO
        return "Body Cultivator"

    @staticmethod
    def get_description():
        # TODO
        return "Frontline cultivator who strengthens the physical body to absorb damage and protect allies."

    @staticmethod
    def get_preview_image():
        # TODO
        return '../../graphics/characters/BodyCultivator.png'


class SpellCultivator(Character):
    """SpellCultivator"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Thief"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 20, 10
        self.speed = 18
        
        try:
            self.image = pygame.image.load('../../graphics/characters/SpellCultivator.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        # TODO
        return "Spell Cultivator"

    @staticmethod
    def get_description():
        # TODO
        return "Ranged cultivator who controls elemental and spiritual energy to attack enemies."

    @staticmethod
    def get_preview_image():
        # TODO
        return '../../graphics/characters/SpellCultivator.png'


class Alchemist(Character):
    """Alchemist"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Wizard"
        self.hp, self.max_hp = 80, 80
        self.attack, self.defense = 10, 10
        self.speed = 15
        
        try:
            self.image = pygame.image.load('../../graphics/characters/Alchemist.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        # TODO
        return "Alchemist"

    @staticmethod
    def get_description():
        # TODO
        return "Specialized in refining pills to cultivate, heal allies, or enhance combat."

    @staticmethod
    def get_preview_image():
        # TODO
        return '../../graphics/characters/Alchemist.png'


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character':
            character_classes.append(cls)
    return character_classes