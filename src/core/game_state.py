"""Game state management and tracking."""

from src.entities.particle import Particle
from src.entities.powerup import PowerUpManager
from src.constants import INITIAL_BLOCK_SPEED, INITIAL_MAX_BLOCKS, LEVEL_UP_SCORE


class GameState:
    """Complete game state container."""

    def __init__(self, difficulty):
        self.difficulty = difficulty
        diff_config = difficulty.get_config()

        # Player State
        self.current_lane_index = 1
        self.player_x = 0
        self.player_y = 0
        self.target_x = 0

        # Game Mechanics
        self.score = 0
        self.level = 1
        self.level_up_score = LEVEL_UP_SCORE
        self.high_score = 0

        # Collections
        self.blocks = []
        self.power_ups = []
        self.particles = []

        # Difficulty Settings
        self.base_block_speed = INITIAL_BLOCK_SPEED
        self.block_speed = self.base_block_speed * diff_config["speed_multiplier"]
        self.max_blocks = INITIAL_MAX_BLOCKS + diff_config["max_blocks_offset"]
        self.level_speed_increase = diff_config["level_speed_increase"]

        # Power-ups
        self.power_up_manager = PowerUpManager()

        # Statistics
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def reset(self):
        """Reset game state for a new game."""
        self.score = 0
        self.level = 1
        self.blocks.clear()
        self.power_ups.clear()
        self.particles.clear()
        self.power_up_manager.deactivate_all()

        diff_config = self.difficulty.get_config()
        self.block_speed = self.base_block_speed * diff_config["speed_multiplier"]
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def add_particle(self, x: float, y: float, vx: float, vy: float,
                    color: tuple, lifetime: int):
        self.particles.append(Particle(x, y, vx, vy, color, lifetime))

    def update_particles(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def check_score_milestone(self) -> bool:
        return self.score >= self.level * self.level_up_score

    def level_up(self):
        self.level += 1
        self.block_speed += self.level_speed_increase
        self.max_blocks += 1
