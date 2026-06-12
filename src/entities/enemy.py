import pygame
import random
from src.constants import ROAD_LANES, SCREEN_HEIGHT, COLLISION_INSET

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: float, y: float, lane: int, zig_zag: bool):
        super().__init__()
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.rect.topleft = (int(self.x), int(self.y))
        
        self.lane = lane
        self.target_lane = lane
        self.zig_zag = zig_zag

    def update(self, dt: float, block_speed: float):
        self.y += block_speed * dt
        vx = 0.0
        
        if self.zig_zag:
            if random.random() < 0.02 * (dt * 60) and 0 < self.y < SCREEN_HEIGHT - 200:
                current_idx = ROAD_LANES.index(self.target_lane) if self.target_lane in ROAD_LANES else 0
                possible_moves = []
                if current_idx > 0:
                    possible_moves.append(ROAD_LANES[current_idx - 1])
                if current_idx < len(ROAD_LANES) - 1:
                    possible_moves.append(ROAD_LANES[current_idx + 1])
                if possible_moves:
                    self.target_lane = random.choice(possible_moves)
            
            target_x = self.target_lane - self.base_image.get_width() // 2
            if abs(self.x - target_x) > 0.5:
                vx = (target_x - self.x) * 3
                self.x += vx * dt
            else:
                self.x = target_x

        angle = -vx * 0.02 # Tilt based on horizontal velocity
        
        if abs(angle) > 0.1:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.base_image, angle)
            self.rect = self.image.get_rect(center=center)
        else:
            self.image = self.base_image
            self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.centerx = int(self.x + self.base_image.get_width() // 2)
        self.rect.y = int(self.y)
        
        if self.y > SCREEN_HEIGHT:
            self.kill()

    def get_hitbox(self) -> pygame.Rect:
        return self.rect.inflate(-COLLISION_INSET * 2, -COLLISION_INSET * 2)
