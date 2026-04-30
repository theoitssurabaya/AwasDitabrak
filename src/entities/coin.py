import pygame
from src.constants import YELLOW

class Coin:
    """Collectible coin that grants bonus score."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = 15
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (200, 150, 0), (int(self.x), int(self.y)), self.radius, 2)
        # Draw a small $ symbol or inner circle
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), self.radius - 8)
