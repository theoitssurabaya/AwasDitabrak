"""Power-up system for special abilities and bonuses."""

import pygame
import math
from src.constants import BLUE, GREEN, YELLOW, RED


class PowerUp(pygame.sprite.Sprite):
    """Collectible power-up that grants temporary bonuses."""

    POWER_UP_TYPES = {
        "shield": {"color": BLUE, "duration": 5.0, "icon": "🛡"},
        "speed": {"color": GREEN, "duration": 4.0, "icon": "⚡"},
        "double": {"color": YELLOW, "duration": 6.0, "icon": "2x"},
        "invincible": {"color": RED, "duration": 3.0, "icon": "★"},
    }

    def __init__(self, x: float, y: float, power_type: str):
        super().__init__()
        self.type = power_type
        self.radius = 20
        self.time = 0.0
        
        size = self.radius * 2
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = self.POWER_UP_TYPES[self.type]["color"]
        pygame.draw.circle(self.base_image, color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.base_image, (255, 255, 255), (self.radius, self.radius), self.radius, 2)
        
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (int(self.x), int(self.y))

    def update(self, dt: float, block_speed: float):
        self.y += (block_speed / 2.0) * dt
        self.time += dt
        
        scale = 1.0 + 0.1 * math.sin(self.time * 6.0)
        new_size = int(self.radius * 2 * scale)
        if new_size > 0:
            self.image = pygame.transform.smoothscale(self.base_image, (new_size, new_size))
            self.rect = self.image.get_rect()
            
        self.rect.center = (int(self.x), int(self.y))


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

    def update(self, dt: float):
        """Decrease duration of all active power-ups."""
        for power_type in self.active:
            self.active[power_type] = [d - dt for d in self.active[power_type] if d - dt > 0]

    def is_active(self, power_type: str) -> bool:
        return len(self.active[power_type]) > 0

    def get_remaining_time(self, power_type: str) -> float:
        """Returns remaining seconds or 0.0 if not active."""
        return self.active[power_type][0] if self.active[power_type] else 0.0

    def deactivate_all(self):
        for power_type in self.active:
            self.active[power_type] = []

    def get_active_powerups(self) -> list:
        return [pt for pt in self.active if self.is_active(pt)]
