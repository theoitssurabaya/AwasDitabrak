"""Particle effect system for visual feedback."""

import pygame


class Particle:
    """Visual particle with gravity and fade effect."""

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple, lifetime: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        """Update particle position and apply gravity."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.2

    def is_alive(self) -> bool:
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface):
        """Render particle with fading and shrinking effect."""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = max(2, int(5 * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
