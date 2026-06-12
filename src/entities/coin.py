import pygame
import math
from src.constants import YELLOW

class Coin(pygame.sprite.Sprite):
    """Collectible coin that grants bonus score."""
    
    def __init__(self, x: float, y: float):
        super().__init__()
        self.radius = 15
        self.time = 0.0
        
        size = self.radius * 2
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.base_image, YELLOW, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.base_image, (200, 150, 0), (self.radius, self.radius), self.radius, 2)
        # Draw a small inner circle
        pygame.draw.circle(self.base_image, (255, 255, 200), (self.radius, self.radius), self.radius - 8)
        
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (int(self.x), int(self.y))
        
    def update(self, dt: float, block_speed: float):
        self.y += (block_speed / 2.0) * dt
        self.time += dt
        
        # Pulse animation
        scale = 1.0 + 0.15 * math.sin(self.time * 8.0)
        new_size = int(self.radius * 2 * scale)
        if new_size > 0:
            self.image = pygame.transform.smoothscale(self.base_image, (new_size, new_size))
            self.rect = self.image.get_rect()
            
        self.rect.center = (int(self.x), int(self.y))
