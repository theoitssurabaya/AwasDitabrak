"""UI rendering system for heads-up display and visual effects."""

import pygame
from typing import List


class UIRenderer:
    """Renders HUD, particles, and visual effects."""

    @staticmethod
    def render_hud(screen: pygame.Surface, game_state, fonts: dict, screen_width: int):
        from src.constants import WHITE, YELLOW, CYAN, BLUE, GREEN, RED, GRAY

        score_text = fonts['small'].render(f"Score: {game_state.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = fonts['small'].render(f"High Score: {game_state.high_score}", True, YELLOW)
        screen.blit(high_score_text, (10, 35))

        level_text = fonts['small'].render(f"Level: {game_state.level}", True, CYAN)
        screen.blit(level_text, (10, 60))

        power_y = 10
        if game_state.power_up_manager.is_active("shield"):
            remaining = game_state.power_up_manager.get_remaining_time("shield")
            shield_text = fonts['tiny'].render(f"Shield: {remaining // 60 + 1}s", True, BLUE)
            screen.blit(shield_text, (screen_width - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("speed"):
            remaining = game_state.power_up_manager.get_remaining_time("speed")
            speed_text = fonts['tiny'].render(f"Speed Boost: {remaining // 60 + 1}s", True, GREEN)
            screen.blit(speed_text, (screen_width - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("double"):
            remaining = game_state.power_up_manager.get_remaining_time("double")
            double_text = fonts['tiny'].render(f"2x Points: {remaining // 60 + 1}s", True, YELLOW)
            screen.blit(double_text, (screen_width - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("invincible"):
            remaining = game_state.power_up_manager.get_remaining_time("invincible")
            invincible_text = fonts['tiny'].render(f"Invincible: {remaining // 60 + 1}s", True, RED)
            screen.blit(invincible_text, (screen_width - 150, power_y))

        diff_name = game_state.difficulty.name
        diff_text = fonts['tiny'].render(f"Difficulty: {diff_name}", True, GRAY)
        screen.blit(diff_text, (screen_width // 2 - 60, 10))

    @staticmethod
    def render_particles(screen: pygame.Surface, particles: List):
        for particle in particles:
            particle.draw(screen)

    @staticmethod
    def render_shield_glow(screen: pygame.Surface, player_x: float, player_y: float,
                          player_width: int, player_height: int):
        pygame.draw.circle(
            screen,
            (100, 150, 255),
            (int(player_x + player_width // 2), int(player_y + player_height // 2)),
            int(player_width // 2 + 15),
            2
        )
