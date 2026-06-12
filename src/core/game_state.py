"""Game state management and tracking."""

import pygame
from src.entities.particle import Particle
from src.entities.powerup import PowerUpManager
from src.constants import INITIAL_BLOCK_SPEED, INITIAL_MAX_BLOCKS, LEVEL_UP_SCORE


class GameState:
    """Complete game state container."""

    def __init__(self, difficulty):
        self.difficulty = difficulty
        diff_config = difficulty.get_config()

        # Player State
        self.player = None

        # Game Mechanics
        self.score = 0.0
        self.level = 1
        self.level_up_score = LEVEL_UP_SCORE
        self.high_score = 0

        # Collections
        self.blocks = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.floating_texts = pygame.sprite.Group()
        
        # Effects
        self.shake_time = 0.0

        # Difficulty Settings
        self.base_block_speed = INITIAL_BLOCK_SPEED * 60.0
        self.block_speed = self.base_block_speed * diff_config["speed_multiplier"]
        self.max_blocks = INITIAL_MAX_BLOCKS + diff_config["max_blocks_offset"]
        self.level_speed_increase = diff_config["level_speed_increase"] * 60.0

        # Power-ups
        self.power_up_manager = PowerUpManager()

        # Statistics
        self.blocks_dodged = 0
        self.powerups_collected = 0
        self.coins_collected = 0

    def reset(self):
        """Reset game state for a new game."""
        self.score = 0.0
        self.level = 1
        self.blocks.empty()
        self.power_ups.empty()
        self.particles.empty()
        self.coins.empty()
        self.floating_texts.empty()
        self.power_up_manager.deactivate_all()
        self.shake_time = 0.0

        diff_config = self.difficulty.get_config()
        self.block_speed = self.base_block_speed * diff_config["speed_multiplier"]
        self.blocks_dodged = 0
        self.powerups_collected = 0
        self.coins_collected = 0

    def add_particle(self, x: float, y: float, vx: float, vy: float,
                    color: tuple, lifetime: int):
        self.particles.add(Particle(x, y, vx, vy, color, lifetime))

    def add_floating_text(self, x: float, y: float, text: str, color: tuple, font: pygame.font.Font):
        from src.entities.particle import FloatingText
        self.floating_texts.add(FloatingText(x, y, text, color, font))

    def update_particles(self, dt: float):
        self.particles.update(dt)
        self.floating_texts.update(dt)
        if self.shake_time > 0:
            self.shake_time -= dt

    def check_score_milestone(self) -> bool:
        return self.score >= self.level * self.level_up_score

    def level_up(self):
        self.level += 1
        self.block_speed += self.level_speed_increase
        self.max_blocks += 1
