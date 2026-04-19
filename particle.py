"""
Particle effect system for visual feedback.

This module provides the Particle class for creating temporary
visual effects like sparks, bursts, and collision effects.
"""

import pygame


class Particle:
    """
    A visual particle that moves on screen with gravity and fades over time.

    Particles are used for visual feedback when collecting power-ups,
    colliding with obstacles, and leveling up.
    """

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: tuple, lifetime: int):
        """
        Initialize a particle.

        Args:
            x: Starting x position
            y: Starting y position
            vx: Horizontal velocity
            vy: Vertical velocity
            color: RGB color tuple
            lifetime: How many frames the particle lives
        """
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
        self.vy += 0.2  # Gravity effect

    def is_alive(self) -> bool:
        """Check if particle is still visible."""
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface):
        """
        Draw the particle on the screen.

        The particle fades out and shrinks as it ages.
        """
        # Calculate alpha fade based on remaining lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))

        # Size decreases as particle ages
        size = max(2, int(5 * (self.lifetime / self.max_lifetime)))

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
