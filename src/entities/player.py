import pygame
from src.constants import ROAD_LANES, SCREEN_HEIGHT, COLLISION_INSET

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, start_lane_index: int):
        super().__init__()
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.current_lane_index = start_lane_index
        
        # Initial position
        self.x = float(ROAD_LANES[self.current_lane_index] - self.rect.width // 2)
        self.y = float(SCREEN_HEIGHT - self.rect.height - 20)
        self.rect.topleft = (int(self.x), int(self.y))
        
        self.target_x = self.x
        self.stun_timer = 0.0
        self.spin_angle = 0.0

    def update(self, dt: float, is_raining: bool = False):
        self.target_x = ROAD_LANES[self.current_lane_index] - self.base_image.get_width() // 2
        
        if self.stun_timer > 0:
            self.stun_timer -= dt
            self.spin_angle = (self.spin_angle + 720 * dt) % 360
            center = self.rect.center
            self.image = pygame.transform.rotate(self.base_image, self.spin_angle)
            self.rect = self.image.get_rect(center=center)
            # Drift slowly to target instead of snapping
            self.x += (self.target_x - self.x) * 2 * dt
            self.rect.centerx = int(self.x + self.base_image.get_width() // 2)
            self.rect.y = int(self.y)
            return
            
        self.spin_angle = 0.0
        
        vx = 0.0
        if abs(self.x - self.target_x) > 0.5:
            snap_velocity = 3.0 if is_raining else 12.0
            vx = (self.target_x - self.x) * snap_velocity
            self.x += vx * dt
        else:
            self.x = self.target_x
            
        # Rotate based on velocity
        # negative vx (moving left) -> positive angle (tilt left)
        # positive vx (moving right) -> negative angle (tilt right)
        angle = -vx * 0.015 # Tune this multiplier for more/less tilt
        
        if abs(angle) > 0.1:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.base_image, angle)
            self.rect = self.image.get_rect(center=center)
        else:
            self.image = self.base_image
            self.rect = self.image.get_rect(center=self.rect.center)
            
        self.rect.centerx = int(self.x + self.base_image.get_width() // 2)
        self.rect.y = int(self.y)

    def get_hitbox(self) -> pygame.Rect:
        return self.rect.inflate(-COLLISION_INSET * 2, -COLLISION_INSET * 2)
