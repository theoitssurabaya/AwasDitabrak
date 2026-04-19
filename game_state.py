"""
Game state management and tracking.

This module provides the GameState class which encapsulates
all game data including player position, score, level, and collections.
"""

from typing import List
from particle import Particle
from powerup import PowerUpManager
from menu import Difficulty
from constants import INITIAL_BLOCK_SPEED, INITIAL_MAX_BLOCKS, LEVEL_UP_SCORE
from menu import DIFFICULTY_CONFIG


class GameState:
    """
    Complete game state container.

    Tracks player position, game objects (blocks, power-ups, particles),
    scoring, levels, and active power-ups. Provides methods for game state
    manipulation and resetting.
    """

    def __init__(self, difficulty: Difficulty):
        """
        Initialize game state with a specific difficulty level.

        Args:
            difficulty: Difficulty enum value (EASY, NORMAL, HARD)
        """
        self.difficulty = difficulty
        diff_config = DIFFICULTY_CONFIG[difficulty]

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

        # Game Collections
        self.blocks = []
        self.power_ups = []
        self.particles = []

        # Difficulty-adjusted Settings
        self.base_block_speed = INITIAL_BLOCK_SPEED
        self.block_speed = self.base_block_speed * diff_config.block_speed_multiplier
        self.max_blocks = INITIAL_MAX_BLOCKS + diff_config.max_blocks_offset
        self.level_speed_increase = diff_config.level_speed_increase

        # Power-up System
        self.power_up_manager = PowerUpManager()

        # Statistics
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def reset(self):
        """Reset game state for a new game while keeping difficulty."""
        self.score = 0
        self.level = 1
        self.blocks.clear()
        self.power_ups.clear()
        self.particles.clear()
        self.power_up_manager.deactivate_all()
        self.block_speed = self.base_block_speed * DIFFICULTY_CONFIG[self.difficulty].block_speed_multiplier
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def add_particle(self, x: float, y: float, vx: float, vy: float,
                    color: tuple, lifetime: int):
        """
        Create and add a particle effect to the game.

        Args:
            x: Starting x position
            y: Starting y position
            vx: Horizontal velocity
            vy: Vertical velocity
            color: RGB color tuple
            lifetime: Duration in frames
        """
        self.particles.append(Particle(x, y, vx, vy, color, lifetime))

    def update_particles(self):
        """Update all particles and remove dead ones."""
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def check_score_milestone(self) -> bool:
        """
        Check if score has reached a level-up threshold.

        Returns:
            True if a level-up has occurred, False otherwise
        """
        return self.score >= self.level * self.level_up_score

    def level_up(self):
        """Increase level and adjust difficulty."""
        self.level += 1
        self.block_speed += self.level_speed_increase
        self.max_blocks += 1
