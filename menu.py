"""
Menu system, game modes, and difficulty configuration.

This module provides the menu screens, game mode states,
difficulty settings, and difficulty configuration.
"""

import pygame
from enum import Enum
from dataclasses import dataclass
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW, BLUE, RED,
    CYAN, GRAY
)


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


@dataclass
class DifficultySettings:
    """Configuration for a difficulty level."""
    block_speed_multiplier: float
    max_blocks_offset: int
    level_speed_increase: float
    description: str


# Difficulty configuration
DIFFICULTY_CONFIG = {
    Difficulty.EASY: DifficultySettings(
        block_speed_multiplier=0.8,
        max_blocks_offset=-1,
        level_speed_increase=0.5,
        description="Slow and steady"
    ),
    Difficulty.NORMAL: DifficultySettings(
        block_speed_multiplier=1.0,
        max_blocks_offset=0,
        level_speed_increase=1.0,
        description="Balanced"
    ),
    Difficulty.HARD: DifficultySettings(
        block_speed_multiplier=1.3,
        max_blocks_offset=1,
        level_speed_increase=1.5,
        description="Fast and furious"
    ),
}


# Font setup (create after pygame.init())
def create_fonts():
    """Create font objects for rendering."""
    return {
        'large': pygame.font.SysFont("arial", 48, bold=True),
        'medium': pygame.font.SysFont("arial", 36),
        'small': pygame.font.SysFont("arial", 24),
        'tiny': pygame.font.SysFont("arial", 18),
    }


class MenuScreen:
    """
    Menu screen renderer and input handler.

    Handles rendering of main menu, difficulty select, pause menu,
    and game over screen. Also manages menu navigation state.
    """

    def __init__(self, fonts: dict):
        """
        Initialize the menu screen.

        Args:
            fonts: Dictionary of pygame Font objects from create_fonts()
        """
        self.fonts = fonts
        self.menu_items = ["START GAME", "VIEW HIGH SCORE", "QUIT"]
        self.selected_index = 0
        self.difficulty_items = ["EASY", "NORMAL", "HARD"]
        self.selected_difficulty = 1

    def render_main_menu(self, screen: pygame.Surface, high_score: int):
        """Render the main menu screen."""
        screen.fill(BLACK)

        # Title
        title = self.fonts['large'].render("AWAS DITABRAK", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Subtitle
        subtitle = self.fonts['medium'].render("Watch Out for the Crash!", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))

        # Menu items
        for i, item in enumerate(self.menu_items):
            color = YELLOW if i == self.selected_index else WHITE
            text = self.fonts['medium'].render(item, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240 + i * 50))

        # Controls hint
        controls = self.fonts['tiny'].render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 40))

    def render_high_score(self, screen: pygame.Surface, high_score: int):
        """Render the high score view."""
        screen.fill(BLACK)

        title = self.fonts['large'].render("HIGH SCORE", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        score_text = self.fonts['large'].render(str(high_score), True, CYAN)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))

        back = self.fonts['medium'].render("Press SPACE to return", True, WHITE)
        screen.blit(back, (SCREEN_WIDTH // 2 - back.get_width() // 2, SCREEN_HEIGHT - 60))

    def render_difficulty_select(self, screen: pygame.Surface):
        """Render the difficulty selection screen."""
        screen.fill(BLACK)

        title = self.fonts['large'].render("SELECT DIFFICULTY", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Difficulty options
        for i, item in enumerate(self.difficulty_items):
            color = YELLOW if i == self.selected_difficulty else WHITE
            text = self.fonts['medium'].render(item, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240 + i * 60))

        # Description
        descriptions = [
            "Slower blocks, easier gameplay",
            "Balanced difficulty",
            "Faster blocks, more challenging"
        ]
        desc = self.fonts['small'].render(descriptions[self.selected_difficulty], True, GRAY)
        screen.blit(desc, (SCREEN_WIDTH // 2 - desc.get_width() // 2, 450))

        # Controls hint
        controls = self.fonts['tiny'].render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 40))

    def render_pause_menu(self, screen: pygame.Surface):
        """Render the pause menu overlay."""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Pause menu box
        pygame.draw.rect(screen, (50, 50, 50),
                        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 200))

        title = self.fonts['large'].render("PAUSED", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        resume = self.fonts['medium'].render("Press SPACE to Resume", True, WHITE)
        screen.blit(resume, (SCREEN_WIDTH // 2 - resume.get_width() // 2, SCREEN_HEIGHT // 2))

        menu = self.fonts['medium'].render("Press M for Menu", True, WHITE)
        screen.blit(menu, (SCREEN_WIDTH // 2 - menu.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def render_game_over(self, screen: pygame.Surface, game_state):
        """Render the game over screen with stats."""
        screen.fill(BLACK)

        # Game Over title
        game_over_text = self.fonts['large'].render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 80))

        # Final score
        score_text = self.fonts['medium'].render(f"Final Score: {game_state.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 180))

        # High score indicator
        if game_state.score > game_state.high_score:
            new_high = self.fonts['medium'].render("NEW HIGH SCORE!", True, CYAN)
            screen.blit(new_high, (SCREEN_WIDTH // 2 - new_high.get_width() // 2, 230))
        else:
            high_score_text = self.fonts['small'].render(f"High Score: {game_state.high_score}", True, WHITE)
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 230))

        # Statistics
        stats = self.fonts['small'].render(
            f"Level Reached: {game_state.level} | Blocks Dodged: {game_state.blocks_dodged}",
            True, WHITE
        )
        screen.blit(stats, (SCREEN_WIDTH // 2 - stats.get_width() // 2, 300))

        # Instructions
        restart_text = self.fonts['medium'].render("Press R to Restart or M for Menu", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 80))
