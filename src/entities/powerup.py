"""Power-up system for special abilities and bonuses."""

import pygame
from src.constants import BLUE, GREEN, YELLOW, RED


class PowerUp:
    """Collectible power-up that grants temporary bonuses."""

    POWER_UP_TYPES = {
        "shield": {"color": BLUE, "duration": 300, "icon": "🛡"},
        "speed": {"color": GREEN, "duration": 240, "icon": "⚡"},
        "double": {"color": YELLOW, "duration": 360, "icon": "2x"},
        "invincible": {"color": RED, "duration": 180, "icon": "★"},
    }

    def __init__(self, x: float, y: float, power_type: str):
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 20

    def draw(self, screen: pygame.Surface):
        color = self.POWER_UP_TYPES[self.type]["color"]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)


class PowerUpManager:
    """Manages active power-ups and their durations."""

    def __init__(self):
        self.active = {
            "shield": [],
            "speed": [],
            "double": [],
            "invincible": []
        }

    def apply_powerup(self, power_type: str):
        duration = PowerUp.POWER_UP_TYPES[power_type]["duration"]
        self.active[power_type].append(duration)

    def update(self):
        """Decrease duration of all active power-ups."""
        for power_type in self.active:
            self.active[power_type] = [d - 1 for d in self.active[power_type] if d > 0]

    def is_active(self, power_type: str) -> bool:
        return len(self.active[power_type]) > 0

    def get_remaining_time(self, power_type: str) -> int:
        """Returns remaining frames or 0 if not active."""
        return self.active[power_type][0] if self.active[power_type] else 0

    def deactivate_all(self):
        for power_type in self.active:
            self.active[power_type] = []

    def get_active_powerups(self) -> list:
        return [pt for pt in self.active if self.is_active(pt)]
