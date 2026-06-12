import pygame
from src.constants import SCREEN_HEIGHT, COLLISION_INSET

class OilSlick(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        # Create a procedural oil slick (black translucent ellipse)
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (20, 20, 20, 180), [0, 0, 70, 50])
        # Add a subtle highlight to make it look wet
        pygame.draw.ellipse(self.image, (80, 80, 80, 100), [10, 10, 20, 10])
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (int(self.x), int(self.y))

    def update(self, dt: float, block_speed: float):
        self.y += block_speed * dt
        self.rect.y = int(self.y)
        
        if self.y > SCREEN_HEIGHT:
            self.kill()

    def get_hitbox(self) -> pygame.Rect:
        return self.rect.inflate(-COLLISION_INSET, -COLLISION_INSET)
