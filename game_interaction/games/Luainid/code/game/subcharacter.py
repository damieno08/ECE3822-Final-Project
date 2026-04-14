"""
subcharacter.py - Character classes with inventory

Lab 4 Update: Characters now have inventories using ArrayList!
"""

import pygame
import sys
from character import Character
from item import Weapon

start_path = str(sys.path[0])

class Cleric(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)

        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/../../graphics/characters/Cleric.png').convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Sets all character stats
        #
        self.character_name = "Cleric"
        self.hp = 50
        self.max_hp = 50
        self.physical_attack = 0
        self.magical_attack = 2
        self.defense = 1
        self.speed = 8
        self.healing = 5
        Staff = Weapon("Staff", "The staff allows the user to cast grand magic. It is also the starting weapon of a Druid.", start_path + "/../../graphics/items/Staff.png", attack_bonus=2, value=40)
        self.equipped_weapon = Staff


        # Special undead bonus damage
        #
        self.undead_boost = 2

        self.import_player_assets(animate=True)

    
    # Protected as we don't want anyone to have infinite attack calls
    def _magical_damage(self, damage, enemyType="Not Undead"):
        """
        This function will determine how much damage a character should produce 
        from magical attacks taking into account the undead boost.
        
        Inputs:
            damage (int): The damage number of our weapon that determines hitpoints lost.
            enemyType(string): A string stating whether the enemy is undead

        Outputs:
            actual_damage(int): The damage points an enemy will actually take.
        """

        actual_damage = super()._magical_damage(damage)
        if enemyType == "Undead":
            actual_damage += self.undead_boost

        return actual_damage

    # Use massive aoe healing ability
    #
    def _special_ability(self):
        
        heal = self._heal(25)

        # Eventually add the ability to heal others
                       
        return heal
    
    @staticmethod
    def get_display_name():
       
        return "Cleric"
    
    @staticmethod
    def get_description():
        
        return "Clerics are warriors and healers who gain their strength from gods."

    
    @staticmethod
    def get_preview_image():
        
        return start_path + "/../../graphics/characters/Cleric.png"


class Paladin(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        
        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/../../graphics/characters/Paladin.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "Paladin"
        self.hp = 100
        self.max_hp = 100
        self.physical_attack = 3
        self.magical_attack = 1
        self.defense = 5
        self.speed = 10
        self.healing = -1
        self.shield = False
        self.import_player_assets(animate=True)
        GreatSword = Weapon("GreatSword", "A large two handed sword that serves as the starter weapon for Barbarians and Paladins", start_path+ "/../../graphics/item/GreatSword.png", attack_bonus=5, value=100)
        self.equipped_weapon = GreatSword

        
    def take_damage(self, amount):
        """Special damage calculation for Paladins as they have a shield spell"""

        # Check if Paladin shield is active before calculating damage
        #
        if self.shield:
            return 0
        amount -= self.defense
        self.hp -= amount

        # Make sure health is never negative
        if self.hp < 0:
            self.hp = 0

        return amount
    
    # Toggle the state of the shield and damage reduction
    def _special_ability(self):
        
        # Toggle shield
        self.shield = not self.shield
    

    
    @staticmethod
    def get_display_name():
       
        return "Paladin"
    
    @staticmethod
    def get_description():
        
        return "Paladins are warriors sworn to their oaths. They are incredibly loyal and protective of the party."
    
    
    @staticmethod
    def get_preview_image():
        
        return start_path + "/../../graphics/characters/Paladin.png"

class Barbarian(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        
        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/../../graphics/characters/Barbarian.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "Barbarian"
        self.hp = 85
        self.max_hp = 85
        self.physical_attack = 7
        self.magical_attack = -2
        self.defense = 3
        self.speed = 10
        self.healing = 0
        self.import_player_assets(animate=True)
        GreatSword = Weapon("GreatSword", "A large two handed sword that serves as the starter weapon for Barbarians and Paladins", start_path + "/../../graphics/item/GreatSword.png", attack_bonus=5, value=100)
        self.equipped_weapon = GreatSword

    
    # Drop our defense for better attack damage
    def _special_ability(self):
        self.physical_attack = 10
        self.defense = 0
        return
    
    @staticmethod
    def get_display_name():

        return "Barbarian"
    
    @staticmethod
    def get_description():

        return "Barbarians are the rough and tumble characters who only care about how hard their sword swings."
    
    
    @staticmethod
    def get_preview_image():
        
        return start_path + "/../../graphics/characters/Barbarian.png"

class Sorcerer(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True, test=False):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        
        # Checks if we are running in test mode, if we are then just make the image a surface.
        # if we aren't, use the real sprite
        #
        if test:
            self.image = pygame.Surface((64, 64))
        else:
            self.image = pygame.image.load(start_path + '/../../graphics/characters/Sorcerer.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set all stats
        self.character_name = "Sorcerer"
        self.hp = 40
        self.max_hp = 40
        self.physical_attack = -1
        self.magical_attack = 6
        self.defense = 3
        self.speed = 8
        self.healing = 0
        self.spell_charge = 0
        self.import_player_assets(animate=True)
        Dagger = Weapon("Dagger", "A small one handed blade that does not do much damage. It is the starter weapon for sorcerers.", "/../../graphics/item/Dagger.png", attack_bonus=2, value=30)
        self.equipped_weapon = Dagger

    
    # Produce a spell charge based on level
    def _special_ability(self):
        self.hp -= 5
        self.spell_charge = 1*self.level
        return 
    
    def expend_charge(self, charges):
        """
        This function will consume the spell charge of a sorcerer for bonus spell damage.
        It should also check that the player has charges to use.

        Inputs:
            charges(int): number of charges you wish to consume

        Outputs:
            self._magical_damage(damage): an integer returning how much magical damage was dealt.
        """

        # Check we have spell charges to use
        if charges > self.spell_charge:
            raise ValueError("Cannot expend more charges than we have")
        
        # Pick some random high number later for damage
        damage = self.level * 50 * charges

        self.spell_charge = 0
        return self._magical_damage(damage)
    
    @staticmethod
    def get_display_name():

        return "Sorcerer"
    
    @staticmethod
    def get_description():

        return "Those born with magic are sorcerers. They draw on the power of their lineage to cast spells."
    
    
    @staticmethod
    def get_preview_image():
        
        return start_path + "/../../graphics/characters/Sorcerer.png"
    
    @staticmethod
    def get_preview_image():
        
        return start_path + "/../../graphics/characters/Sorcerer.png"


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character':
            character_classes.append(cls)
    return character_classes