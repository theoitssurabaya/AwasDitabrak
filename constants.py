"""
Game constants and configuration for AwasDitabrak.

This module contains all static configuration values including colors,
screen dimensions, FPS, asset paths, and game settings.
"""

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Frame Rate
FPS = 60

# Colors (RGB Tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# Asset Paths
PLAYER_CAR_IMAGE = "car.png"
ENEMY_CAR_IMAGE = "car2.png"
ROAD_IMAGE = "road.png"
HIGH_SCORE_FILE = "high_score.txt"

# Game Configuration
PLAYER_CAR_HEIGHT = 80
ENEMY_CAR_HEIGHT = 80
ROAD_LANES = [215, 340, 460, 585]
ROAD_TOP = -100

# Collision Detection
COLLISION_INSET = 10

# Initial Game Settings
INITIAL_BLOCK_SPEED = 5
INITIAL_MAX_BLOCKS = 3
LEVEL_UP_SCORE = 1000

# Block and Power-up Spawning
BLOCK_SPAWN_CHANCE = 3  # Percentage (1-100)
POWERUP_SPAWN_CHANCE = 250  # 1 in X chance per frame
