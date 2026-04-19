"""Game constants and configuration."""

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
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
PLAYER_CAR_IMAGE = "assets/images/car.png"
ENEMY_CAR_IMAGE = "assets/images/car2.png"
ROAD_IMAGE = "assets/images/road.png"
HIGH_SCORE_FILE = "high_score.txt"

# Game Configuration
PLAYER_CAR_HEIGHT = 80
ENEMY_CAR_HEIGHT = 80
ROAD_LANES = [215, 340, 460, 585]
ROAD_TOP = -100
COLLISION_INSET = 10

# Initial Settings
INITIAL_BLOCK_SPEED = 5
INITIAL_MAX_BLOCKS = 3
LEVEL_UP_SCORE = 1000

# Spawn Rates
BLOCK_SPAWN_CHANCE = 3
POWERUP_SPAWN_CHANCE = 250
