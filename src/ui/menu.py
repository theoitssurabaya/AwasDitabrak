"""Menu system, game modes, and difficulty configuration."""

import pygame
from enum import Enum
from dataclasses import dataclass
from src.ui.ui_renderer import UIRenderer


class GameMode(Enum):
    """Game state modes."""
    MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5
    HOW_TO_PLAY = 6


class Difficulty(Enum):
    """Difficulty levels."""
    EASY = 1
    NORMAL = 2
    HARD = 3

    def get_config(self):
        configs = {
            Difficulty.EASY: {
                "speed_multiplier": 0.8,
                "max_blocks_offset": -1,
                "level_speed_increase": 0.5,
                "description": "Slow and steady"
            },
            Difficulty.NORMAL: {
                "speed_multiplier": 1.0,
                "max_blocks_offset": 0,
                "level_speed_increase": 1.0,
                "description": "Balanced"
            },
            Difficulty.HARD: {
                "speed_multiplier": 1.3,
                "max_blocks_offset": 1,
                "level_speed_increase": 1.5,
                "description": "Fast and furious"
            },
        }
        return configs[self]


def create_fonts():
    """Create pygame font objects."""
    import os
    font_path = "assets/fonts/font.ttf"
    if os.path.exists(font_path):
        return {
            'large': pygame.font.Font(font_path, 64),
            'medium': pygame.font.Font(font_path, 42),
            'small': pygame.font.Font(font_path, 28),
            'tiny': pygame.font.Font(font_path, 20),
        }
    return {
        'large': pygame.font.SysFont("arial", 64, bold=True),
        'medium': pygame.font.SysFont("arial", 42),
        'small': pygame.font.SysFont("arial", 28),
        'tiny': pygame.font.SysFont("arial", 20),
    }


class MenuScreen:
    """Menu screen renderer and input handler."""

    def __init__(self, fonts: dict, screen_width: int, screen_height: int):
        self.fonts = fonts
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_items = ["START GAME", "HOW TO PLAY", "VIEW HIGH SCORE", "QUIT"]
        self.selected_index = 0
        self.difficulty_items = ["EASY", "NORMAL", "HARD"]
        self.selected_difficulty = 1

    def render_main_menu(self, screen: pygame.Surface, high_score: int):
        import math
        from src.constants import YELLOW, WHITE, GRAY, BLACK
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        time_ms = pygame.time.get_ticks()
        y_offset = math.sin(time_ms * 0.003) * 10

        title = UIRenderer.render_text_with_outline(self.fonts['large'], "AWAS DITABRAK", YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80 + y_offset))

        subtitle = UIRenderer.render_text_with_outline(self.fonts['medium'], "Watch Out for the Crash!", WHITE)
        screen.blit(subtitle, (self.screen_width // 2 - subtitle.get_width() // 2, 140 + y_offset))

        for i, item in enumerate(self.menu_items):
            if i == self.selected_index:
                pulse = (math.sin(time_ms * 0.008) + 1) / 2
                color = (int(YELLOW[0]), int(YELLOW[1]), int(YELLOW[2]*pulse))
                display_text = f">  {item}  <"
            else:
                color = WHITE
                display_text = item
                
            text = UIRenderer.render_text_with_outline(self.fonts['medium'], display_text, color)
            screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 240 + i * 50))

        controls = UIRenderer.render_text_with_outline(self.fonts['tiny'], "↑↓ Navigate  | ENTER Select", GRAY)
        screen.blit(controls, (self.screen_width // 2 - controls.get_width() // 2, self.screen_height - 40))

    def render_high_score(self, screen: pygame.Surface, high_score: int):
        from src.constants import YELLOW, WHITE, CYAN, BLACK
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = UIRenderer.render_text_with_outline(self.fonts['large'], "HIGH SCORE", YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))

        score_text = UIRenderer.render_text_with_outline(self.fonts['large'], str(high_score), CYAN)
        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 280))

        back = UIRenderer.render_text_with_outline(self.fonts['medium'], "Press SPACE to return", WHITE)
        screen.blit(back, (self.screen_width // 2 - back.get_width() // 2, self.screen_height - 60))

    def render_how_to_play(self, screen: pygame.Surface):
        from src.constants import YELLOW, WHITE, CYAN, BLUE, GREEN, RED
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title = UIRenderer.render_text_with_outline(self.fonts['large'], "HOW TO PLAY", YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))
        
        instructions = [
            ("OBJECTIVE", YELLOW),
            ("Avoid cars and survive as long as possible!", WHITE),
            ("Collect coins for +50 points.", WHITE),
            ("", WHITE),
            ("CONTROLS", YELLOW),
            ("A/D or Left/Right Arrows: Steer", WHITE),
            ("SPACE: Pause", WHITE),
            ("", WHITE),
            ("POWER-UPS", YELLOW),
            ("Shield (Blue): Absorbs one crash", BLUE),
            ("Speed Boost (Green): Game moves 1.5x faster", GREEN),
            ("Double Points (Yellow): 2x score multiplier", YELLOW),
            ("Invincible (Red): Immune to crashes", RED),
        ]
        
        y = 140
        for text, color in instructions:
            if text:
                line = UIRenderer.render_text_with_outline(self.fonts['small'], text, color, outline_width=1)
                screen.blit(line, (self.screen_width // 2 - line.get_width() // 2, y))
            y += 30

        back = UIRenderer.render_text_with_outline(self.fonts['medium'], "Press SPACE to return", WHITE)
        screen.blit(back, (self.screen_width // 2 - back.get_width() // 2, self.screen_height - 50))

    def render_difficulty_select(self, screen: pygame.Surface):
        import math
        from src.constants import YELLOW, WHITE, GRAY, BLACK
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        time_ms = pygame.time.get_ticks()
        y_offset = math.sin(time_ms * 0.003) * 10

        title = UIRenderer.render_text_with_outline(self.fonts['large'], "SELECT DIFFICULTY", YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80 + y_offset))

        for i, item in enumerate(self.difficulty_items):
            if i == self.selected_difficulty:
                pulse = (math.sin(time_ms * 0.008) + 1) / 2
                color = (int(YELLOW[0]), int(YELLOW[1]), int(YELLOW[2]*pulse))
                display_text = f">  {item}  <"
            else:
                color = WHITE
                display_text = item
                
            text = UIRenderer.render_text_with_outline(self.fonts['medium'], display_text, color)
            screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 240 + i * 60))

        descriptions = [
            "Slower blocks, easier gameplay",
            "Balanced difficulty",
            "Faster blocks, more challenging"
        ]
        desc = UIRenderer.render_text_with_outline(self.fonts['small'], descriptions[self.selected_difficulty], GRAY)
        screen.blit(desc, (self.screen_width // 2 - desc.get_width() // 2, 450))

        controls = UIRenderer.render_text_with_outline(self.fonts['tiny'], "↑↓ Navigate  | ENTER Select", GRAY)
        screen.blit(controls, (self.screen_width // 2 - controls.get_width() // 2, self.screen_height - 40))

    def render_pause_menu(self, screen: pygame.Surface):
        from src.constants import YELLOW, WHITE
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (50, 50, 50),
                        (self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200))

        title = UIRenderer.render_text_with_outline(self.fonts['large'], "PAUSED", YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 80))

        resume = UIRenderer.render_text_with_outline(self.fonts['medium'], "Press SPACE to Resume", WHITE)
        screen.blit(resume, (self.screen_width // 2 - resume.get_width() // 2, self.screen_height // 2))

        menu = UIRenderer.render_text_with_outline(self.fonts['medium'], "Press M for Menu", WHITE)
        screen.blit(menu, (self.screen_width // 2 - menu.get_width() // 2, self.screen_height // 2 + 50))

    def render_game_over(self, screen: pygame.Surface, game_state):
        import math
        from src.constants import RED, YELLOW, WHITE, CYAN, BLACK
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((150, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        time_ms = pygame.time.get_ticks()
        y_offset = math.sin(time_ms * 0.003) * 10

        game_over_text = UIRenderer.render_text_with_outline(self.fonts['large'], "GAME OVER", RED)
        screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 80 + y_offset))

        score_text = UIRenderer.render_text_with_outline(self.fonts['medium'], f"Final Score: {int(game_state.score)}", YELLOW)
        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 180))

        if game_state.score > game_state.high_score:
            new_high = UIRenderer.render_text_with_outline(self.fonts['medium'], "NEW HIGH SCORE!", CYAN)
            screen.blit(new_high, (self.screen_width // 2 - new_high.get_width() // 2, 230))
        else:
            high_score_text = UIRenderer.render_text_with_outline(self.fonts['small'], f"High Score: {game_state.high_score}", WHITE)
            screen.blit(high_score_text, (self.screen_width // 2 - high_score_text.get_width() // 2, 230))

        stats = UIRenderer.render_text_with_outline(self.fonts['small'], f"Level: {game_state.level} | Dodged: {game_state.blocks_dodged} | Coins: {game_state.coins_collected}", WHITE)
        screen.blit(stats, (self.screen_width // 2 - stats.get_width() // 2, 300))

        restart_text = UIRenderer.render_text_with_outline(self.fonts['medium'], "Press R to Restart or M for Menu", WHITE)
        screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height - 80))
