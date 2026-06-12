"""Particle effect system for visual feedback."""

import pygame
import random


class Particle(pygame.sprite.Sprite):
    """Visual particle with gravity and fade effect."""

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple, lifetime: int):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.shape = random.choice(["circle", "square"])
        
        # Convert frame lifetime to seconds (assuming originally 60 FPS)
        self.lifetime = lifetime / 60.0
        self.max_lifetime = self.lifetime
        
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self._update_image()

    def _update_image(self):
        self.image.fill((0, 0, 0, 0))
        ratio = max(0, self.lifetime / self.max_lifetime)
        alpha = int(255 * ratio)
        size = max(2, int(5 * ratio))
        if size > 0:
            color_with_alpha = (*self.color[:3], alpha)
            if self.shape == "circle":
                pygame.draw.circle(self.image, color_with_alpha, (5, 5), size)
            else:
                rect = pygame.Rect(5 - size, 5 - size, size * 2, size * 2)
                pygame.draw.rect(self.image, color_with_alpha, rect)

    def update(self, dt: float):
        """Update particle position and apply gravity."""
        # Scale velocities by 60 to maintain original visual speed per second
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.2 * dt * 60
        
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        else:
            self.rect.center = (int(self.x), int(self.y))
            self._update_image()


class FloatingText(pygame.sprite.Sprite):
    """Floating text pop-up for scores."""
    
    def __init__(self, x: float, y: float, text: str, color: tuple, font: pygame.font.Font, lifetime: float = 1.0):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        
        from src.ui.ui_renderer import UIRenderer
        self.base_image = UIRenderer.render_text_with_outline(self.font, self.text, self.color, outline_width=1, shadow_offset=2)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
    def update(self, dt: float, *args):
        self.y -= 50 * dt  # Float upwards
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.kill()
        else:
            alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
            self.image = self.base_image.copy()
            self.image.set_alpha(alpha)
            self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
