"""
main.py - Complete game with character selection and networking

Integrated version combining lab-03 and project-01
"""

import pygame
import sys
import os
import argparse

from game_interaction.games.game_santiago.code.game.settings import *
from game_interaction.games.game_santiago.code.game.level import Level
from game_interaction.games.game_santiago.code.game.subcharacter import get_all_character_classes

_here = os.path.dirname(os.path.abspath(__file__))


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        try:
            self.font = pygame.font.Font(None, fontsize)
        except:
            self.font = pygame.font.SysFont('arial', fontsize)

        self.content = content
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.fg, self.bg = fg, bg

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class CharacterCard:
    """Visual card displaying a character option"""
    def __init__(self, x, y, character_class):
        self.character_class = character_class
        self.x, self.y = x, y
        self.width, self.height = 200, 280

        try:
            self.name_font = pygame.font.Font(None, 28)
            self.desc_font = pygame.font.Font(None, 18)
        except:
            self.name_font = pygame.font.SysFont('arial', 28)
            self.desc_font = pygame.font.SysFont('arial', 18)

        # Load character preview image relative to this file, not CWD
        try:
            _preview = os.path.normpath(os.path.join(_here, character_class.get_preview_image()))
            self.char_image = pygame.image.load(_preview).convert_alpha()
            self.char_image = pygame.transform.scale(self.char_image, (128, 128))
        except:
            self.char_image = pygame.Surface((128, 128))
            self.char_image.fill((200, 200, 200))

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.selected = False
        self.hovered = False

    def draw(self, surface):
        if self.selected:
            bg_color = (100, 200, 100)
        elif self.hovered:
            bg_color = (150, 150, 150)
        else:
            bg_color = (80, 80, 80)

        self.image.fill(bg_color)
        pygame.draw.rect(self.image, (255, 255, 255), [0, 0, self.width, self.height], 3)

        img_rect = self.char_image.get_rect(center=(self.width/2, 80))
        self.image.blit(self.char_image, img_rect)

        name_text = self.name_font.render(self.character_class.get_display_name(), True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.width/2, 160))
        self.image.blit(name_text, name_rect)

        desc = self.character_class.get_description()
        self.draw_wrapped_text(desc, self.desc_font, (255, 255, 255), 10, 190, self.width - 20)

        surface.blit(self.image, self.rect)

    def draw_wrapped_text(self, text, font, color, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if font.size(test_line)[0] > max_width:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.image.blit(text_surface, (x, y + i * 20))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos, pressed):
        if self.rect.collidepoint(pos) and pressed[0]:
            return True
        return False


class game_santi:
    def __init__(self, player_name, server_host='localhost', server_port=50076, serializer='text'):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))

        try:
            self.font = pygame.font.Font(None, 48)
            self.button_font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 20)
        except:
            self.font = pygame.font.SysFont('arial', 48)
            self.button_font = pygame.font.SysFont('arial', 32)
            self.small_font = pygame.font.SysFont('arial', 20)

        pygame.display.set_caption(GAME_NAME + f' - {player_name} ({serializer.upper()})')
        self.clock = pygame.time.Clock()

        self.player_name = player_name
        self.server_host = server_host
        self.server_port = server_port
        self.serializer  = serializer

        self.selected_character = None
        self.level   = None
        self.running = True

    def character_select(self):
        char_select = True

        title = self.font.render("Choose Your Character", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH/2, 50))

        network_info = self.small_font.render(
            f"Connecting as: {self.player_name} | Server: {self.server_host}:{self.server_port} | {self.serializer.upper()}",
            True, (200, 200, 200)
        )
        network_info_rect = network_info.get_rect(center=(WIDTH/2, 650))

        character_classes = get_all_character_classes()

        cards = []
        card_spacing = 220
        start_x = (WIDTH - (len(character_classes) * card_spacing - 20)) / 2

        for i, char_class in enumerate(character_classes):
            card = CharacterCard(start_x + i * card_spacing, 120, char_class)
            cards.append(card)

        button_width, button_height = 300, 50
        confirm_button_rect = pygame.Rect(WIDTH/2 - button_width/2, 480, button_width, button_height)
        return_button_rect  = pygame.Rect(WIDTH/2 - button_width/2, 550, button_width, button_height)

        selected_card      = None
        clicked_this_frame = False

        while char_select:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    char_select = False
                    self.running = False
                    pygame.quit()
                    if self.level and self.level.connected:
                        self.level.network.disconnect()
                        self.level.chat_client.disconnect()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        char_select = False
                        self.running = False
                        pygame.quit()
                        if self.level and self.level.connected:
                            self.level.network.disconnect()
                            self.level.chat_client.disconnect()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_this_frame = True

            mouse_pos     = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for card in cards:
                card.hovered = card.is_hovered(mouse_pos)
                if clicked_this_frame and card.is_hovered(mouse_pos):
                    for c in cards:
                        c.selected = False
                    card.selected = True
                    selected_card = card

            # Confirm — start game with selected character
            if clicked_this_frame and selected_card and confirm_button_rect.collidepoint(mouse_pos):
                self.selected_character = selected_card.character_class
                char_select = False

            # Return — go back to client
            if clicked_this_frame and return_button_rect.collidepoint(mouse_pos):
                self.running = False
                char_select = False
                pygame.quit()
                if self.level and self.level.connected:
                    self.level.chat_client.disconnect()
                    self.level.network.disconnect()
                return

            if not mouse_pressed[0]:
                clicked_this_frame = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(title, title_rect)

            for card in cards:
                card.draw(self.screen)

            # Confirm button
            if selected_card:
                button_color = (50, 150, 50) if confirm_button_rect.collidepoint(mouse_pos) else (30, 100, 30)
            else:
                button_color = (100, 100, 100)

            pygame.draw.rect(self.screen, button_color, confirm_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), confirm_button_rect, 2)
            confirm_text = self.button_font.render("Confirm", True, (255, 255, 255))
            confirm_rect = confirm_text.get_rect(center=confirm_button_rect.center)
            self.screen.blit(confirm_text, confirm_rect)

            # Return button
            button_color = (150, 30, 30) if return_button_rect.collidepoint(mouse_pos) else (100, 100, 100)
            pygame.draw.rect(self.screen, button_color, return_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), return_button_rect, 2)
            return_text = self.button_font.render("Return", True, (255, 255, 255))
            return_rect = return_text.get_rect(center=return_button_rect.center)
            self.screen.blit(return_text, return_rect)

            self.screen.blit(network_info, network_info_rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def run(self, is_multiplayer):
        pygame.mixer.init()
        _music = os.path.normpath(os.path.join(_here, '../../music/casino_sound_effect.mp3'))

        while True:
            # ---- Character selection ----
            self.running = True
            self.selected_character = None
            self.character_select()

            if not self.running or self.selected_character is None:
                return

            # ---- Tear down previous level if restarting ----
            if self.level and self.level.connected:
                self.level.network.disconnect()
                self.level.chat_client.disconnect()

            # ---- Create new level ----
            self.level = Level(
                self.player_name,
                self.selected_character,
                self.server_host,
                self.server_port,
                self.serializer,
                is_multiplayer
            )

            # ---- Start music ----
            try:
                pygame.mixer.music.load(_music)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"[Audio] Could not load music: {e}")

            go_to_select = False

            # ---- Inner game loop ----
            while self.running:

                # Handle death
                if not self.level.player.is_alive():
                    pygame.mixer.music.stop()

                    self.screen.fill((20, 0, 0))
                    try:
                        _death_img_path = os.path.normpath(os.path.join(_here, '../../graphics/death.png'))
                        death_image = pygame.image.load(_death_img_path).convert_alpha()
                        death_image = pygame.transform.scale(death_image, (WIDTH, HEIGHT))
                        self.screen.blit(death_image, (0, 0))
                    except Exception:
                        death_font = pygame.font.Font(None, 120)
                        death_text = death_font.render("YOU DIED", True, (200, 0, 0))
                        self.screen.blit(death_text, death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

                    death_start = pygame.time.get_ticks()
                    while pygame.time.get_ticks() - death_start < 5000:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                if self.level.connected:
                                    self.level.chat_client.disconnect()
                                    self.level.network.disconnect()
                                pygame.quit()
                                return
                        pygame.display.update()
                        self.clock.tick(FPS)

                    if self.level.connected:
                        self.level.chat_client.disconnect()
                        self.level.network.disconnect()
                    pygame.quit()
                    return

                events = []
                for event in pygame.event.get():
                    events.append(event)
                    if event.type == pygame.QUIT:
                        pygame.mixer.music.stop()
                        if self.level.connected:
                            self.level.network.disconnect()
                            self.level.chat_client.disconnect()
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mixer.music.stop()
                            self.running = False
                            if self.level.connected:
                                self.level.network.disconnect()
                                self.level.chat_client.disconnect()
                            go_to_select = True

                self.screen.fill('black')
                try:
                    self.level.run(events)
                except Exception:
                    import traceback
                    traceback.print_exc()
                    raise
                pygame.display.update()
                self.clock.tick(FPS)

            # Inner loop exited — go back to character select if Escape was pressed,
            # otherwise the Return button inside character_select already called pygame.quit()
            if not go_to_select:
                return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multiplayer Game Client with Character Selection')
    parser.add_argument('name', help='Your player name')
    parser.add_argument('--server', default='localhost',
                       help='Server hostname (default: localhost)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Server port (default: 8080)')
    parser.add_argument('--serializer', choices=['text', 'json', 'binary'],
                       default='text',
                       help='Serialization format: text (default), json, or binary')

    args = parser.parse_args()

    print("="*50)
    print(f"Starting game as '{args.name}'")
    print(f"Connecting to {args.server}:{args.port}")
    print(f"Using {args.serializer.upper()} serialization")
    print("="*50)
    print()

    game = game_santi(args.name, args.server, args.port, args.serializer)
    game.run()
