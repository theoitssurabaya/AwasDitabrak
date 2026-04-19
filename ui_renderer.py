"""
UI rendering system for heads-up display and visual effects.

This module provides the UIRenderer class for rendering game HUD,
particle effects, and shield glow.
"""

import pygame
from typing import List
from constants import SCREEN_WIDTH, WHITE, YELLOW, BLUE, GREEN, RED, CYAN, GRAY
from particle import Particle


class UIRenderer:
    """
    Static methods for rendering UI elements and visual effects.

    Handles drawing the heads-up display (HUD), particles, and effects.
    """

    @staticmethod
    def render_hud(screen: pygame.Surface, game_state, fonts: dict):
        """
        Render the main game heads-up display.

        Displays score, high score, level, difficulty, and active power-ups.

        Args:
            screen: Pygame surface to draw on
            game_state: Current GameState object
            fonts: Dictionary of pygame Font objects
        """
        # Score
        score_text = fonts['small'].render(f"Score: {game_state.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # High Score
        high_score_text = fonts['small'].render(f"High Score: {game_state.high_score}", True, YELLOW)
        screen.blit(high_score_text, (10, 35))

        # Level
        level_text = fonts['small'].render(f"Level: {game_state.level}", True, CYAN)
        screen.blit(level_text, (10, 60))

        # Active power-ups indicator
        power_y = 10
        if game_state.power_up_manager.is_active("shield"):
            remaining = game_state.power_up_manager.get_remaining_time("shield")
            shield_text = fonts['tiny'].render(f"Shield: {remaining // 60 + 1}s", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("speed"):
            remaining = game_state.power_up_manager.get_remaining_time("speed")
            speed_text = fonts['tiny'].render(f"Speed Boost: {remaining // 60 + 1}s", True, GREEN)
            screen.blit(speed_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("double"):
            remaining = game_state.power_up_manager.get_remaining_time("double")
            double_text = fonts['tiny'].render(f"2x Points: {remaining // 60 + 1}s", True, YELLOW)
            screen.blit(double_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("invincible"):
            remaining = game_state.power_up_manager.get_remaining_time("invincible")
            invincible_text = fonts['tiny'].render(f"Invincible: {remaining // 60 + 1}s", True, RED)
            screen.blit(invincible_text, (SCREEN_WIDTH - 150, power_y))

        # Difficulty indicator
        diff_name = game_state.difficulty.name
        diff_text = fonts['tiny'].render(f"Difficulty: {diff_name}", True, GRAY)
        screen.blit(diff_text, (SCREEN_WIDTH // 2 - 60, 10))

    @staticmethod
    def render_particles(screen: pygame.Surface, particles: List[Particle]):
        """
        Render all active particles.

        Args:
            screen: Pygame surface to draw on
            particles: List of Particle objects
        """
        for particle in particles:
            particle.draw(screen)

    @staticmethod
    def render_shield_glow(screen: pygame.Surface, player_x: float, player_y: float,
                          player_width: int, player_height: int):
        """
        Render a glowing shield effect around the player.

        Args:
            screen: Pygame surface to draw on
            player_x: Player's x position
            player_y: Player's y position
            player_width: Player sprite width
            player_height: Player sprite height
        """
        pygame.draw.circle(
            screen,
            (100, 150, 255),
            (int(player_x + player_width // 2), int(player_y + player_height // 2)),
            int(player_width // 2 + 15),
            2
        )
