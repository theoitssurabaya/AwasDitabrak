import pygame
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class AtmosphereManager:
    def __init__(self):
        self.rain_particles = []
        self.darkness_alpha = 0.0
        self.target_alpha = 0.0
        
        self.is_raining = False
        self.is_night = False
        
    def reset(self):
        self.rain_particles.clear()
        self.darkness_alpha = 0.0
        self.target_alpha = 0.0
        self.is_raining = False
        self.is_night = False

    def set_level(self, level: int):
        cycle = (level - 1) % 4
        if cycle == 0:
            self.is_raining = False
            self.is_night = False
            self.target_alpha = 0.0
        elif cycle == 1:
            self.is_raining = True
            self.is_night = False
            self.target_alpha = 50.0 
        elif cycle == 2:
            self.is_raining = False
            self.is_night = True
            self.target_alpha = 230.0
        elif cycle == 3:
            self.is_raining = True
            self.is_night = True
            self.target_alpha = 245.0

    def update(self, dt: float):
        if self.darkness_alpha < self.target_alpha:
            self.darkness_alpha = min(self.target_alpha, self.darkness_alpha + 30 * dt)
        elif self.darkness_alpha > self.target_alpha:
            self.darkness_alpha = max(self.target_alpha, self.darkness_alpha - 30 * dt)
            
        if self.is_raining:
            # Spawn rain
            spawn_rate = int(2500 * dt) + 2
            for _ in range(spawn_rate):
                if random.random() < 0.7:
                    self.rain_particles.append({
                        "x": random.randint(-100, SCREEN_WIDTH + 400),
                        "y": -50,
                        "vx": random.uniform(-600.0, -400.0),
                        "vy": random.uniform(1000.0, 1500.0),
                        "length": random.randint(40, 80)
                    })
                    
        for p in self.rain_particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            
        self.rain_particles = [p for p in self.rain_particles if p["y"] < SCREEN_HEIGHT + 100]

    def draw_rain(self, screen: pygame.Surface, shake_x: int, shake_y: int):
        if not self.rain_particles: return
        for p in self.rain_particles:
            end_x = p["x"] - p["length"] * 0.5
            end_y = p["y"] + p["length"]
            # Draw line with thickness
            pygame.draw.line(screen, (180, 220, 255), (p["x"] + shake_x, p["y"] + shake_y), (end_x + shake_x, end_y + shake_y), 3)
            
    def _generate_headlight(self, up: bool) -> pygame.Surface:
        surf = pygame.Surface((300, 500))
        surf.fill((0, 0, 0))
        if up:
            pygame.draw.polygon(surf, (180, 180, 80), [(150, 500), (50, 0), (250, 0)])
        else:
            pygame.draw.polygon(surf, (180, 180, 80), [(150, 0), (50, 500), (250, 500)])
        return surf

    def draw_lighting(self, screen: pygame.Surface, player, blocks, shake_x: int, shake_y: int):
        if self.darkness_alpha <= 0:
            return
            
        light_map = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        ambient = max(10, 255 - int(self.darkness_alpha))
        light_map.fill((ambient, ambient, min(255, ambient + 20)))
        
        if self.is_night:
            if not hasattr(self, 'headlight_up'):
                self.headlight_up = self._generate_headlight(True)
                self.headlight_down = self._generate_headlight(False)
                
            hx = player.rect.centerx - 150 + shake_x
            hy = player.rect.top - 500 + shake_y
            light_map.blit(self.headlight_up, (hx, hy), special_flags=pygame.BLEND_RGBA_ADD)
            
            for block in blocks:
                if -100 < block.rect.bottom < SCREEN_HEIGHT + 200:
                    ex = block.rect.centerx - 150 + shake_x
                    ey = block.rect.bottom + shake_y - 20
                    light_map.blit(self.headlight_down, (ex, ey), special_flags=pygame.BLEND_RGBA_ADD)
                    
        screen.blit(light_map, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
