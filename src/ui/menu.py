"""Menu system, game modes, and difficulty configuration."""

import pygame
from enum import Enum
from dataclasses import dataclass


class GameMode(Enum):
    """Game state modes."""
    MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5


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
    return {
        'large': pygame.font.SysFont("arial", 48, bold=True),
        'medium': pygame.font.SysFont("arial", 36),
        'small': pygame.font.SysFont("arial", 24),
        'tiny': pygame.font.SysFont("arial", 18),
    }


class MenuScreen:
    """Menu screen renderer and input handler."""

    def __init__(self, fonts: dict, screen_width: int, screen_height: int):
        self.fonts = fonts
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.menu_items = ["START GAME", "VIEW HIGH SCORE", "QUIT"]
        self.selected_index = 0
        self.difficulty_items = ["EASY", "NORMAL", "HARD"]
        self.selected_difficulty = 1

    def render_main_menu(self, screen: pygame.Surface, high_score: int):
        from src.constants import YELLOW, WHITE, GRAY, BLACK
        screen.fill(BLACK)

        title = self.fonts['large'].render("AWAS DITABRAK", True, YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80))

        subtitle = self.fonts['medium'].render("Watch Out for the Crash!", True, WHITE)
        screen.blit(subtitle, (self.screen_width // 2 - subtitle.get_width() // 2, 140))

        for i, item in enumerate(self.menu_items):
            color = YELLOW if i == self.selected_index else WHITE
            text = self.fonts['medium'].render(item, True, color)
            screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 240 + i * 50))

        controls = self.fonts['tiny'].render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (self.screen_width // 2 - controls.get_width() // 2, self.screen_height - 40))

    def render_high_score(self, screen: pygame.Surface, high_score: int):
        from src.constants import YELLOW, WHITE, CYAN, BLACK
        screen.fill(BLACK)

        title = self.fonts['large'].render("HIGH SCORE", True, YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))

        score_text = self.fonts['large'].render(str(high_score), True, CYAN)
        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 280))

        back = self.fonts['medium'].render("Press SPACE to return", True, WHITE)
        screen.blit(back, (self.screen_width // 2 - back.get_width() // 2, self.screen_height - 60))

    def render_difficulty_select(self, screen: pygame.Surface):
        from src.constants import YELLOW, WHITE, GRAY, BLACK
        screen.fill(BLACK)

        title = self.fonts['large'].render("SELECT DIFFICULTY", True, YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80))

        for i, item in enumerate(self.difficulty_items):
            color = YELLOW if i == self.selected_difficulty else WHITE
            text = self.fonts['medium'].render(item, True, color)
            screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 240 + i * 60))

        descriptions = [
            "Slower blocks, easier gameplay",
            "Balanced difficulty",
            "Faster blocks, more challenging"
        ]
        desc = self.fonts['small'].render(descriptions[self.selected_difficulty], True, GRAY)
        screen.blit(desc, (self.screen_width // 2 - desc.get_width() // 2, 450))

        controls = self.fonts['tiny'].render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (self.screen_width // 2 - controls.get_width() // 2, self.screen_height - 40))

    def render_pause_menu(self, screen: pygame.Surface):
        from src.constants import YELLOW, WHITE
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (50, 50, 50),
                        (self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200))

        title = self.fonts['large'].render("PAUSED", True, YELLOW)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 80))

        resume = self.fonts['medium'].render("Press SPACE to Resume", True, WHITE)
        screen.blit(resume, (self.screen_width // 2 - resume.get_width() // 2, self.screen_height // 2))

        menu = self.fonts['medium'].render("Press M for Menu", True, WHITE)
        screen.blit(menu, (self.screen_width // 2 - menu.get_width() // 2, self.screen_height // 2 + 50))

    def render_game_over(self, screen: pygame.Surface, game_state):
        from src.constants import RED, YELLOW, WHITE, CYAN, BLACK
        screen.fill(BLACK)

        game_over_text = self.fonts['large'].render("GAME OVER", True, RED)
        screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 80))

        score_text = self.fonts['medium'].render(f"Final Score: {game_state.score}", True, YELLOW)
        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 180))

        if game_state.score > game_state.high_score:
            new_high = self.fonts['medium'].render("NEW HIGH SCORE!", True, CYAN)
            screen.blit(new_high, (self.screen_width // 2 - new_high.get_width() // 2, 230))
        else:
            high_score_text = self.fonts['small'].render(f"High Score: {game_state.high_score}", True, WHITE)
            screen.blit(high_score_text, (self.screen_width // 2 - high_score_text.get_width() // 2, 230))

        stats = self.fonts['small'].render(
            f"Level Reached: {game_state.level} | Blocks Dodged: {game_state.blocks_dodged}",
            True, WHITE
        )
        screen.blit(stats, (self.screen_width // 2 - stats.get_width() // 2, 300))

        restart_text = self.fonts['medium'].render("Press R to Restart or M for Menu", True, WHITE)
        screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height - 80))
