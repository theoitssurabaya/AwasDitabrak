"""UI rendering system for heads-up display and visual effects."""

import pygame
from typing import List


class UIRenderer:
    """Renders HUD, particles, and visual effects."""

    @staticmethod
    def render_text_with_outline(font: pygame.font.Font, text: str, color: tuple, outline_color=(0, 0, 0), outline_width=2, shadow_offset=3) -> pygame.Surface:
        text_surface = font.render(text, True, color)
        if outline_width == 0 and shadow_offset == 0:
            return text_surface
            
        outline_surface = font.render(text, True, outline_color)
        w = text_surface.get_width() + (2 * outline_width) + shadow_offset
        h = text_surface.get_height() + (2 * outline_width) + shadow_offset
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        
        if shadow_offset > 0:
            shadow_surface = font.render(text, True, (0, 0, 0))
            shadow_surface.set_alpha(150)
            surface.blit(shadow_surface, (outline_width + shadow_offset, outline_width + shadow_offset))
            
        if outline_width > 0:
            for dx in [-outline_width, 0, outline_width]:
                for dy in [-outline_width, 0, outline_width]:
                    if dx == 0 and dy == 0:
                        continue
                    surface.blit(outline_surface, (dx + outline_width, dy + outline_width))
                    
        surface.blit(text_surface, (outline_width, outline_width))
        return surface

    @staticmethod
    def render_hud(screen: pygame.Surface, game_state, fonts: dict, screen_width: int):
        from src.constants import WHITE, YELLOW, CYAN, BLUE, GREEN, RED, GRAY

        score_text = UIRenderer.render_text_with_outline(fonts['small'], f"Score: {int(game_state.score)}", WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = UIRenderer.render_text_with_outline(fonts['small'], f"High Score: {game_state.high_score}", YELLOW)
        screen.blit(high_score_text, (10, 50))

        level_text = UIRenderer.render_text_with_outline(fonts['small'], f"Level: {game_state.level}", CYAN)
        screen.blit(level_text, (10, 90))

        power_y = 10
        if game_state.power_up_manager.is_active("shield"):
            remaining = game_state.power_up_manager.get_remaining_time("shield")
            shield_text = UIRenderer.render_text_with_outline(fonts['tiny'], f"Shield: {remaining // 60 + 1}s", BLUE)
            screen.blit(shield_text, (screen_width - shield_text.get_width() - 10, power_y))
            power_y += 30

        if game_state.power_up_manager.is_active("speed"):
            remaining = game_state.power_up_manager.get_remaining_time("speed")
            speed_text = UIRenderer.render_text_with_outline(fonts['tiny'], f"Speed Boost: {remaining // 60 + 1}s", GREEN)
            screen.blit(speed_text, (screen_width - speed_text.get_width() - 10, power_y))
            power_y += 30

        if game_state.power_up_manager.is_active("double"):
            remaining = game_state.power_up_manager.get_remaining_time("double")
            double_text = UIRenderer.render_text_with_outline(fonts['tiny'], f"2x Points: {remaining // 60 + 1}s", YELLOW)
            screen.blit(double_text, (screen_width - double_text.get_width() - 10, power_y))
            power_y += 30

        if game_state.power_up_manager.is_active("invincible"):
            remaining = game_state.power_up_manager.get_remaining_time("invincible")
            invincible_text = UIRenderer.render_text_with_outline(fonts['tiny'], f"Invincible: {remaining // 60 + 1}s", RED)
            screen.blit(invincible_text, (screen_width - invincible_text.get_width() - 10, power_y))

        diff_name = game_state.difficulty.name
        diff_text = UIRenderer.render_text_with_outline(fonts['tiny'], f"Difficulty: {diff_name}", GRAY)
        screen.blit(diff_text, (screen_width // 2 - diff_text.get_width() // 2, 10))

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
