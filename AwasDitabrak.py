import pygame
import random
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

# Initialize Pygame
pygame.init()
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

# Font
pygame.font.init()
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 36)
font_small = pygame.font.SysFont("arial", 24)
font_tiny = pygame.font.SysFont("arial", 18)


class GameMode(Enum):
    MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5


class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


@dataclass
class DifficultySettings:
    block_speed_multiplier: float
    max_blocks_offset: int
    level_speed_increase: float
    description: str


DIFFICULTY_CONFIG = {
    Difficulty.EASY: DifficultySettings(
        block_speed_multiplier=0.8,
        max_blocks_offset=-1,
        level_speed_increase=0.5,
        description="Slow and steady"
    ),
    Difficulty.NORMAL: DifficultySettings(
        block_speed_multiplier=1.0,
        max_blocks_offset=0,
        level_speed_increase=1.0,
        description="Balanced"
    ),
    Difficulty.HARD: DifficultySettings(
        block_speed_multiplier=1.3,
        max_blocks_offset=1,
        level_speed_increase=1.5,
        description="Fast and furious"
    ),
}


class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.2  # gravity

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = max(2, int(5 * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)


class PowerUp:
    POWER_UP_TYPES = {
        "shield": {"color": BLUE, "duration": 300, "icon": "🛡"},
        "speed": {"color": GREEN, "duration": 240, "icon": "⚡"},
        "double": {"color": YELLOW, "duration": 360, "icon": "2x"},
        "invincible": {"color": RED, "duration": 180, "icon": "★"},
    }

    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 20
        self.duration = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.POWER_UP_TYPES[self.type]["color"],
                          (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)


class PowerUpManager:
    def __init__(self):
        self.active: Dict[str, List] = {
            "shield": [],
            "speed": [],
            "double": [],
            "invincible": []
        }

    def apply_powerup(self, power_type):
        self.active[power_type].append(PowerUp.POWER_UP_TYPES[power_type]["duration"])

    def update(self):
        for power_type in self.active:
            self.active[power_type] = [d - 1 for d in self.active[power_type] if d > 0]

    def is_active(self, power_type):
        return len(self.active[power_type]) > 0

    def get_remaining_time(self, power_type):
        if self.active[power_type]:
            return self.active[power_type][0]
        return 0

    def deactivate_all(self):
        for power_type in self.active:
            self.active[power_type] = []


class GameState:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        diff_config = DIFFICULTY_CONFIG[difficulty]

        # Player
        self.current_lane_index = 1
        self.player_x = 0
        self.player_y = 0
        self.target_x = 0

        # Game mechanics
        self.score = 0
        self.level = 1
        self.level_up_score = 1000
        self.high_score = 0

        # Collections
        self.blocks = []
        self.power_ups = []
        self.particles = []

        # Game settings
        self.base_block_speed = 5
        self.block_speed = 5 * diff_config.block_speed_multiplier
        self.max_blocks = 3 + diff_config.max_blocks_offset
        self.level_speed_increase = diff_config.level_speed_increase

        # Power-ups
        self.power_up_manager = PowerUpManager()

        # Stats
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def reset(self):
        self.score = 0
        self.level = 1
        self.blocks.clear()
        self.power_ups.clear()
        self.particles.clear()
        self.power_up_manager.deactivate_all()
        self.block_speed = self.base_block_speed * DIFFICULTY_CONFIG[self.difficulty].block_speed_multiplier
        self.blocks_dodged = 0
        self.powerups_collected = 0

    def add_particle(self, x, y, vx, vy, color, lifetime):
        self.particles.append(Particle(x, y, vx, vy, color, lifetime))


class UIRenderer:
    @staticmethod
    def render_hud(screen, game_state: GameState):
        # Score
        score_text = font_small.render(f"Score: {game_state.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # High Score
        high_score_text = font_small.render(f"High Score: {game_state.high_score}", True, YELLOW)
        screen.blit(high_score_text, (10, 35))

        # Level
        level_text = font_small.render(f"Level: {game_state.level}", True, CYAN)
        screen.blit(level_text, (10, 60))

        # Active power-ups indicator
        power_y = 10
        if game_state.power_up_manager.is_active("shield"):
            remaining = game_state.power_up_manager.get_remaining_time("shield")
            shield_text = font_tiny.render(f"Shield: {remaining // 60 + 1}s", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("speed"):
            remaining = game_state.power_up_manager.get_remaining_time("speed")
            speed_text = font_tiny.render(f"Speed Boost: {remaining // 60 + 1}s", True, GREEN)
            screen.blit(speed_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("double"):
            remaining = game_state.power_up_manager.get_remaining_time("double")
            double_text = font_tiny.render(f"2x Points: {remaining // 60 + 1}s", True, YELLOW)
            screen.blit(double_text, (SCREEN_WIDTH - 150, power_y))
            power_y += 25

        if game_state.power_up_manager.is_active("invincible"):
            remaining = game_state.power_up_manager.get_remaining_time("invincible")
            invincible_text = font_tiny.render(f"Invincible: {remaining // 60 + 1}s", True, RED)
            screen.blit(invincible_text, (SCREEN_WIDTH - 150, power_y))

        # Difficulty indicator
        diff_name = game_state.difficulty.name
        diff_text = font_tiny.render(f"Difficulty: {diff_name}", True, GRAY)
        screen.blit(diff_text, (SCREEN_WIDTH // 2 - 60, 10))

    @staticmethod
    def render_particles(screen, particles: List[Particle]):
        for particle in particles:
            particle.draw(screen)

    @staticmethod
    def render_shield_glow(screen, player_x, player_y, player_width, player_height):
        pygame.draw.circle(screen, (100, 150, 255),
                          (int(player_x + player_width // 2), int(player_y + player_height // 2)),
                          int(player_width // 2 + 15), 2)


class MenuScreen:
    def __init__(self):
        self.menu_items = ["START GAME", "VIEW HIGH SCORE", "QUIT"]
        self.selected_index = 0
        self.difficulty_items = ["EASY", "NORMAL", "HARD"]
        self.selected_difficulty = 1

    def render_main_menu(self, screen, high_score):
        screen.fill(BLACK)

        title = font_large.render("AWAS DITABRAK", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        subtitle = font_medium.render("Watch Out for the Crash!", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))

        for i, item in enumerate(self.menu_items):
            color = YELLOW if i == self.selected_index else WHITE
            text = font_medium.render(item, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240 + i * 50))

        controls = font_tiny.render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 40))

    def render_high_score(self, screen, high_score):
        screen.fill(BLACK)

        title = font_large.render("HIGH SCORE", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        score_text = font_large.render(str(high_score), True, CYAN)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))

        back = font_medium.render("Press SPACE to return", True, WHITE)
        screen.blit(back, (SCREEN_WIDTH // 2 - back.get_width() // 2, SCREEN_HEIGHT - 60))

    def render_difficulty_select(self, screen):
        screen.fill(BLACK)

        title = font_large.render("SELECT DIFFICULTY", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        for i, item in enumerate(self.difficulty_items):
            color = YELLOW if i == self.selected_difficulty else WHITE
            text = font_medium.render(item, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240 + i * 60))

        descriptions = [
            "Slower blocks, easier gameplay",
            "Balanced difficulty",
            "Faster blocks, more challenging"
        ]
        desc = font_small.render(descriptions[self.selected_difficulty], True, GRAY)
        screen.blit(desc, (SCREEN_WIDTH // 2 - desc.get_width() // 2, 450))

        controls = font_tiny.render("↑↓ Navigate  | ENTER Select", True, GRAY)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 40))

    def render_pause_menu(self, screen):
        screen.fill((0, 0, 0, 128))
        pygame.draw.rect(screen, (50, 50, 50),
                        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 200))

        title = font_large.render("PAUSED", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        resume = font_medium.render("Press SPACE to Resume", True, WHITE)
        screen.blit(resume, (SCREEN_WIDTH // 2 - resume.get_width() // 2, SCREEN_HEIGHT // 2))

        menu = font_medium.render("Press M for Menu", True, WHITE)
        screen.blit(menu, (SCREEN_WIDTH // 2 - menu.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def render_game_over(self, screen, game_state: GameState):
        screen.fill(BLACK)

        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 80))

        score_text = font_medium.render(f"Final Score: {game_state.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 180))

        if game_state.score > game_state.high_score:
            new_high = font_medium.render("NEW HIGH SCORE!", True, CYAN)
            screen.blit(new_high, (SCREEN_WIDTH // 2 - new_high.get_width() // 2, 230))
        else:
            high_score_text = font_small.render(f"High Score: {game_state.high_score}", True, WHITE)
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 230))

        stats = font_small.render(f"Level Reached: {game_state.level} | Blocks Dodged: {game_state.blocks_dodged}", True, WHITE)
        screen.blit(stats, (SCREEN_WIDTH // 2 - stats.get_width() // 2, 300))

        restart_text = font_medium.render("Press R to Restart or M for Menu", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 80))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Awas Ditabrak")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Load assets
        self.load_assets()

        # Game state
        self.mode = GameMode.MENU
        self.game_state = None
        self.menu_screen = MenuScreen()
        self.viewing_high_score = False

        # Load high score
        self.high_score_file = "high_score.txt"
        self.high_score = self.load_high_score()

    def load_assets(self):
        """Load game images with error handling"""
        try:
            self.player_img = self.load_and_scale_image("car.png", 80)
            self.block_img = self.load_and_scale_image("car2.png", 80)
            self.block_img = pygame.transform.rotate(self.block_img, 180)
            self.background_img = pygame.image.load("road.png")
            self.background_img = pygame.transform.scale(self.background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load all assets: {e}")
            # Create placeholder surfaces if assets fail to load
            self.player_img = pygame.Surface((60, 80))
            self.player_img.fill(CYAN)
            self.block_img = pygame.Surface((60, 80))
            self.block_img.fill(RED)
            self.background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_img.fill((40, 40, 40))

    def load_and_scale_image(self, image_path, new_height):
        image = pygame.image.load(image_path)
        original_width, original_height = image.get_size()
        aspect_ratio = original_width / original_height
        new_width = int(new_height * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))

    def load_high_score(self):
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, "r") as file:
                    return int(file.read().strip())
            except:
                return 0
        return 0

    def save_high_score(self):
        with open(self.high_score_file, "w") as file:
            file.write(str(self.high_score))

    def start_game(self, difficulty: Difficulty):
        self.game_state = GameState(difficulty)
        self.game_state.high_score = self.high_score
        player_width, player_height = self.player_img.get_size()
        LANES = [215, 340, 460, 585]
        self.game_state.player_x = LANES[self.game_state.current_lane_index] - player_width // 2
        self.game_state.player_y = SCREEN_HEIGHT - player_height - 20
        self.game_state.target_x = self.game_state.player_x
        self.mode = GameMode.PLAYING

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_screen.selected_index = (self.menu_screen.selected_index - 1) % len(self.menu_screen.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.menu_screen.selected_index = (self.menu_screen.selected_index + 1) % len(self.menu_screen.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.menu_screen.selected_index == 0:
                        self.mode = GameMode.DIFFICULTY_SELECT
                    elif self.menu_screen.selected_index == 1:
                        self.viewing_high_score = True
                    elif self.menu_screen.selected_index == 2:
                        return False
                elif event.key == pygame.K_SPACE and self.viewing_high_score:
                    self.viewing_high_score = False
        return True

    def handle_difficulty_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_screen.selected_difficulty = (self.menu_screen.selected_difficulty - 1) % len(self.menu_screen.difficulty_items)
                elif event.key == pygame.K_DOWN:
                    self.menu_screen.selected_difficulty = (self.menu_screen.selected_difficulty + 1) % len(self.menu_screen.difficulty_items)
                elif event.key == pygame.K_RETURN:
                    difficulty = list(Difficulty)[self.menu_screen.selected_difficulty]
                    self.start_game(difficulty)
        return True

    def handle_gameplay_input(self):
        LANES = [215, 340, 460, 585]
        player_width, _ = self.player_img.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    self.game_state.current_lane_index = max(0, self.game_state.current_lane_index - 1)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.game_state.current_lane_index = min(len(LANES) - 1, self.game_state.current_lane_index + 1)
                elif event.key == pygame.K_SPACE:
                    self.mode = GameMode.PAUSED
                elif event.key == pygame.K_ESCAPE:
                    self.mode = GameMode.MENU
        return True

    def handle_pause_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = GameMode.PLAYING
                elif event.key == pygame.K_m:
                    self.mode = GameMode.MENU
        return True

    def handle_gameover_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.mode = GameMode.DIFFICULTY_SELECT
                    self.menu_screen.selected_difficulty = 1
                elif event.key == pygame.K_m:
                    self.mode = GameMode.MENU
        return True

    def update_gameplay(self):
        LANES = [215, 340, 460, 585]
        ROAD_TOP = -100
        player_width, player_height = self.player_img.get_size()
        block_width, block_height = self.block_img.get_size()

        # Apply speed boost if active
        current_block_speed = self.game_state.block_speed
        if self.game_state.power_up_manager.is_active("speed"):
            current_block_speed *= 1.5

        # Smooth player movement
        target_x = LANES[self.game_state.current_lane_index] - player_width // 2
        if self.game_state.player_x != target_x:
            self.game_state.player_x += (target_x - self.game_state.player_x) // 5

        # Add new blocks
        active_lanes = [block[2] for block in self.game_state.blocks]
        if len(self.game_state.blocks) < self.game_state.max_blocks:
            available_lanes = [lane for lane in LANES if lane not in active_lanes]
            if available_lanes and random.randint(1, 100) <= 3:
                new_lane = random.choice(available_lanes)
                self.game_state.blocks.append([new_lane - block_width // 2, ROAD_TOP, new_lane])

        # Spawn power-ups
        if random.randint(1, 250) == 1:
            power_lane = random.choice(LANES)
            power_type = random.choice(list(PowerUp.POWER_UP_TYPES.keys()))
            self.game_state.power_ups.append(PowerUp(power_lane, ROAD_TOP, power_type))

        # Move blocks and power-ups
        for block in self.game_state.blocks:
            block[1] += current_block_speed
        for power_up in self.game_state.power_ups:
            power_up.y += current_block_speed // 2

        # Remove off-screen elements
        self.game_state.blocks = [block for block in self.game_state.blocks if block[1] < SCREEN_HEIGHT]
        self.game_state.power_ups = [p for p in self.game_state.power_ups if p.y < SCREEN_HEIGHT]

        # Update particles
        for particle in self.game_state.particles:
            particle.update()
        self.game_state.particles = [p for p in self.game_state.particles if p.is_alive()]

        # Check collisions with blocks
        player_rect = pygame.Rect(self.game_state.player_x + 10, self.game_state.player_y + 10,
                                 player_width - 20, player_height - 20)

        blocks_to_remove = []
        for block in self.game_state.blocks:
            block_rect = pygame.Rect(block[0] + 10, block[1] + 10, block_width - 20, block_height - 20)
            if player_rect.colliderect(block_rect):
                blocks_to_remove.append(block)
                # Collision effect
                for _ in range(5):
                    self.game_state.add_particle(
                        self.game_state.player_x + player_width // 2,
                        self.game_state.player_y + player_height // 2,
                        random.uniform(-3, 3), random.uniform(-3, 1),
                        RED, 30
                    )

                if self.game_state.power_up_manager.is_active("invincible"):
                    pass  # Invincible, ignore collision
                elif self.game_state.power_up_manager.is_active("shield"):
                    self.game_state.power_up_manager.active["shield"] = []
                else:
                    self.mode = GameMode.GAME_OVER
                    if self.game_state.score > self.high_score:
                        self.high_score = self.game_state.score
                        self.game_state.high_score = self.high_score
                    return

        self.game_state.blocks = [b for b in self.game_state.blocks if b not in blocks_to_remove]
        self.game_state.blocks_dodged += len(blocks_to_remove)

        # Check collisions with power-ups
        powerups_to_remove = []
        for power_up in self.game_state.power_ups:
            pu_rect = pygame.Rect(power_up.x - power_up.radius, power_up.y - power_up.radius,
                                 power_up.radius * 2, power_up.radius * 2)
            if player_rect.colliderect(pu_rect):
                powerups_to_remove.append(power_up)
                self.game_state.power_up_manager.apply_powerup(power_up.type)
                self.game_state.powerups_collected += 1

                # Pickup effect
                color = PowerUp.POWER_UP_TYPES[power_up.type]["color"]
                for _ in range(8):
                    self.game_state.add_particle(
                        power_up.x, power_up.y,
                        random.uniform(-4, 4), random.uniform(-5, -1),
                        color, 40
                    )

        self.game_state.power_ups = [p for p in self.game_state.power_ups if p not in powerups_to_remove]

        # Update power-ups
        self.game_state.power_up_manager.update()

        # Update score
        score_increment = 1
        if self.game_state.power_up_manager.is_active("double"):
            score_increment = 2
        self.game_state.score += score_increment

        # Check level up
        if self.game_state.score >= self.game_state.level * self.game_state.level_up_score:
            self.game_state.level += 1
            self.game_state.block_speed += self.game_state.level_speed_increase
            self.game_state.max_blocks += 1

            # Level up effect
            for _ in range(10):
                self.game_state.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    random.uniform(-5, 5), random.uniform(-5, 5),
                    YELLOW, 50
                )

    def render(self):
        if self.mode == GameMode.MENU:
            if self.viewing_high_score:
                self.menu_screen.render_high_score(self.screen, self.high_score)
            else:
                self.menu_screen.render_main_menu(self.screen, self.high_score)

        elif self.mode == GameMode.DIFFICULTY_SELECT:
            self.menu_screen.render_difficulty_select(self.screen)

        elif self.mode in (GameMode.PLAYING, GameMode.PAUSED):
            # Draw background
            self.screen.blit(self.background_img, (0, 0))

            # Draw blocks
            for block in self.game_state.blocks:
                self.screen.blit(self.block_img, (block[0], block[1]))

            # Draw power-ups
            for power_up in self.game_state.power_ups:
                power_up.draw(self.screen)

            # Draw particles
            UIRenderer.render_particles(self.screen, self.game_state.particles)

            # Draw shield glow
            if self.game_state.power_up_manager.is_active("shield"):
                UIRenderer.render_shield_glow(self.screen, self.game_state.player_x,
                                             self.game_state.player_y,
                                             self.player_img.get_width(),
                                             self.player_img.get_height())

            # Draw player
            self.screen.blit(self.player_img, (int(self.game_state.player_x), int(self.game_state.player_y)))

            # Draw HUD
            UIRenderer.render_hud(self.screen, self.game_state)

            # Draw pause menu if paused
            if self.mode == GameMode.PAUSED:
                self.menu_screen.render_pause_menu(self.screen)

        elif self.mode == GameMode.GAME_OVER:
            self.screen.blit(self.background_img, (0, 0))
            self.menu_screen.render_game_over(self.screen, self.game_state)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            if self.mode == GameMode.MENU:
                running = self.handle_menu_input()
            elif self.mode == GameMode.DIFFICULTY_SELECT:
                running = self.handle_difficulty_input()
            elif self.mode == GameMode.PLAYING:
                running = self.handle_gameplay_input()
                self.update_gameplay()
            elif self.mode == GameMode.PAUSED:
                running = self.handle_pause_input()
            elif self.mode == GameMode.GAME_OVER:
                running = self.handle_gameover_input()

            self.render()
            self.clock.tick(self.FPS)

        # Save high score before exiting
        self.save_high_score()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
