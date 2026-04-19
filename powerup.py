"""
Power-up system for special abilities and bonuses.

This module provides the PowerUp class for collectible bonuses
and PowerUpManager for tracking active effects.
"""

import pygame
from constants import BLUE, GREEN, YELLOW, RED


class PowerUp:
    """
    A collectible power-up that grants temporary bonuses.

    Supported power-up types:
    - shield: Absorbs one collision
    - speed: Increases block speed
    - double: Doubles points earned
    - invincible: Immunity from collisions
    """

    # Power-up type metadata
    POWER_UP_TYPES = {
        "shield": {"color": BLUE, "duration": 300, "icon": "🛡"},
        "speed": {"color": GREEN, "duration": 240, "icon": "⚡"},
        "double": {"color": YELLOW, "duration": 360, "icon": "2x"},
        "invincible": {"color": RED, "duration": 180, "icon": "★"},
    }

    def __init__(self, x: float, y: float, power_type: str):
        """
        Initialize a power-up.

        Args:
            x: X position on screen
            y: Y position on screen
            power_type: Type of power-up (see POWER_UP_TYPES keys)
        """
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 20

    def draw(self, screen: pygame.Surface):
        """Draw the power-up as a colored circle."""
        color = self.POWER_UP_TYPES[self.type]["color"]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)


class PowerUpManager:
    """
    Manages all active power-ups and their effects.

    Tracks which power-ups are active, their remaining duration,
    and provides methods to activate/deactivate them.
    """

    def __init__(self):
        """Initialize the power-up manager with empty active effects."""
        self.active = {
            "shield": [],
            "speed": [],
            "double": [],
            "invincible": []
        }

    def apply_powerup(self, power_type: str):
        """
        Activate a power-up effect.

        Args:
            power_type: Type of power-up to activate
        """
        duration = PowerUp.POWER_UP_TYPES[power_type]["duration"]
        self.active[power_type].append(duration)

    def update(self):
        """
        Update all active power-ups, decreasing remaining duration.

        Call this once per game frame.
        """
        for power_type in self.active:
            self.active[power_type] = [d - 1 for d in self.active[power_type] if d > 0]

    def is_active(self, power_type: str) -> bool:
        """Check if a power-up type is currently active."""
        return len(self.active[power_type]) > 0

    def get_remaining_time(self, power_type: str) -> int:
        """
        Get remaining duration of a power-up (in frames).

        Args:
            power_type: Type of power-up to check

        Returns:
            Remaining frames, or 0 if not active
        """
        if self.active[power_type]:
            return self.active[power_type][0]
        return 0

    def deactivate_all(self):
        """Remove all active power-ups immediately."""
        for power_type in self.active:
            self.active[power_type] = []

    def get_active_powerups(self) -> list:
        """
        Get list of currently active power-up types.

        Returns:
            List of power-up type strings that are currently active
        """
        return [pt for pt in self.active if self.is_active(pt)]
