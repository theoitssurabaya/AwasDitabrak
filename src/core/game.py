"""Main game controller and game loop."""

import pygame
import random
import os
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_CAR_IMAGE, ENEMY_CAR_IMAGE,
    ROAD_IMAGE, HIGH_SCORE_FILE, PLAYER_CAR_HEIGHT, ENEMY_CAR_HEIGHT,
    ROAD_LANES, ROAD_TOP, BLOCK_SPAWN_CHANCE, POWERUP_SPAWN_CHANCE,
    RED, YELLOW
)
from src.ui.menu import GameMode, Difficulty, MenuScreen, create_fonts
from src.core.game_state import GameState
from src.entities.powerup import PowerUp
from src.entities.coin import Coin
from src.entities.player import PlayerCar
from src.entities.enemy import EnemyCar
from src.ui.ui_renderer import UIRenderer


class Game:
    """Main game controller."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Awas Ditabrak")
        self.clock = pygame.time.Clock()
        self.fonts = create_fonts()

        self.load_assets()

        self.mode = GameMode.MENU
        self.game_state = None
        self.menu_screen = MenuScreen(self.fonts, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.viewing_high_score = False

        self.high_score_file = HIGH_SCORE_FILE
        self.high_score = self.load_high_score()
        self.bg_y = 0
        self.speed_lines = []
        self.camera_sway = 0.0

    def load_assets(self):
        """Load game images with fallback to placeholders."""
        try:
            self.player_img = self.load_and_scale_image(PLAYER_CAR_IMAGE, PLAYER_CAR_HEIGHT)
            self.block_img = self.load_and_scale_image(ENEMY_CAR_IMAGE, ENEMY_CAR_HEIGHT)
            self.block_img = pygame.transform.rotate(self.block_img, 180)
            self.background_img = pygame.image.load(ROAD_IMAGE)
            self.background_img = pygame.transform.scale(self.background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load all assets: {e}")
            self.player_img = pygame.Surface((60, 80))
            self.player_img.fill((0, 255, 255))
            self.block_img = pygame.Surface((60, 80))
            self.block_img.fill((255, 0, 0))
            self.background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_img.fill((40, 40, 40))

    def load_and_scale_image(self, image_path: str, new_height: int) -> pygame.Surface:
        image = pygame.image.load(image_path)
        original_width, original_height = image.get_size()
        aspect_ratio = original_width / original_height
        new_width = int(new_height * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))

    def load_high_score(self) -> int:
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
        self.game_state.player = PlayerCar(self.player_img, 1)
        self.mode = GameMode.PLAYING

    def handle_menu_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_screen.selected_index = (self.menu_screen.selected_index - 1) % len(
                        self.menu_screen.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.menu_screen.selected_index = (self.menu_screen.selected_index + 1) % len(
                        self.menu_screen.menu_items)
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

    def handle_difficulty_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_screen.selected_difficulty = (self.menu_screen.selected_difficulty - 1) % len(
                        self.menu_screen.difficulty_items)
                elif event.key == pygame.K_DOWN:
                    self.menu_screen.selected_difficulty = (self.menu_screen.selected_difficulty + 1) % len(
                        self.menu_screen.difficulty_items)
                elif event.key == pygame.K_RETURN:
                    difficulty = list(Difficulty)[self.menu_screen.selected_difficulty]
                    self.start_game(difficulty)
        return True

    def handle_gameplay_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    self.game_state.player.current_lane_index = max(0, self.game_state.player.current_lane_index - 1)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.game_state.player.current_lane_index = min(len(ROAD_LANES) - 1,
                                                             self.game_state.player.current_lane_index + 1)
                elif event.key == pygame.K_SPACE:
                    self.mode = GameMode.PAUSED
                elif event.key == pygame.K_ESCAPE:
                    self.mode = GameMode.MENU
        return True

    def handle_pause_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = GameMode.PLAYING
                elif event.key == pygame.K_m:
                    self.mode = GameMode.MENU
        return True

    def handle_gameover_input(self) -> bool:
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

    def update_background(self, dt: float, speed: float):
        self.bg_y = (self.bg_y + speed * dt) % SCREEN_HEIGHT
        
        # Speed lines
        if random.random() < 0.8 * (dt * 60):
            self.speed_lines.append({
                "x": random.choice([20, 40, SCREEN_WIDTH-20, SCREEN_WIDTH-40]),
                "y": 0,
                "length": random.randint(30, 100),
                "speed": speed * 1.5
            })
            
        for line in self.speed_lines:
            line["y"] += line["speed"] * dt
            
        self.speed_lines = [l for l in self.speed_lines if l["y"] < SCREEN_HEIGHT]

    def update_gameplay(self, dt: float):
        if dt > 0.1:  # Prevent huge jumps if lag
            dt = 0.1
            
        player_width, player_height = self.player_img.get_size()
        block_width, block_height = self.block_img.get_size()

        current_block_speed = self.game_state.block_speed
        if self.game_state.power_up_manager.is_active("speed"):
            current_block_speed *= 1.5

        # Gradual speed increase
        self.game_state.block_speed += 0.12 * dt
        self.update_background(dt, current_block_speed)

        self.game_state.player.update(dt)

        # Camera sway based on player velocity
        player_vx = 0.0
        if hasattr(self.game_state.player, 'last_x'):
            player_vx = (self.game_state.player.x - self.game_state.player.last_x) / dt
        self.game_state.player.last_x = self.game_state.player.x
        
        target_sway = -player_vx * 0.02
        self.camera_sway += (target_sway - self.camera_sway) * 5.0 * dt

        # Power-up trails
        for p_type, data in PowerUp.POWER_UP_TYPES.items():
            if self.game_state.power_up_manager.is_active(p_type):
                if random.random() < 0.5 * (dt * 60):
                    self.game_state.add_particle(
                        self.game_state.player.rect.centerx + random.uniform(-15, 15),
                        self.game_state.player.rect.centery + random.uniform(-15, 15),
                        random.uniform(-1, 1), random.uniform(1, 3),
                        data["color"], random.randint(20, 40)
                    )

        active_lanes = [block.target_lane for block in self.game_state.blocks]
        if len(self.game_state.blocks) < self.game_state.max_blocks:
            available_lanes = [lane for lane in ROAD_LANES if lane not in active_lanes]
            if available_lanes and random.randint(1, 100) <= BLOCK_SPAWN_CHANCE:
                new_lane = random.choice(available_lanes)
                is_zig_zag = self.game_state.level >= 2 and random.random() < 0.3
                self.game_state.blocks.add(EnemyCar(
                    self.block_img,
                    new_lane - block_width // 2,
                    ROAD_TOP,
                    new_lane,
                    is_zig_zag
                ))

        if random.randint(1, POWERUP_SPAWN_CHANCE) == 1:
            power_lane = random.choice(ROAD_LANES)
            power_type = random.choice(list(PowerUp.POWER_UP_TYPES.keys()))
            self.game_state.power_ups.add(PowerUp(power_lane, ROAD_TOP, power_type))

        if random.randint(1, 100) == 1:
            coin_lane = random.choice(ROAD_LANES)
            self.game_state.coins.add(Coin(coin_lane, ROAD_TOP))

        # Exhaust particles
        if random.random() < 0.3 * (dt * 60):
            self.game_state.add_particle(
                self.game_state.player.rect.centerx + random.uniform(-10, 10),
                self.game_state.player.rect.bottom - 10,
                random.uniform(-0.5, 0.5), random.uniform(2, 4),
                (150, 150, 150), random.randint(15, 30)
            )

        self.game_state.blocks.update(dt, current_block_speed)
        self.game_state.power_ups.update(dt, current_block_speed)
        self.game_state.coins.update(dt, current_block_speed)

        self.game_state.update_particles(dt)
        self.game_state.power_up_manager.update(dt)

        player_hitbox = self.game_state.player.get_hitbox()

        blocks_to_remove = []
        for block in self.game_state.blocks:
            if player_hitbox.colliderect(block.get_hitbox()):
                blocks_to_remove.append(block)
                for _ in range(15):
                    self.game_state.add_particle(
                        self.game_state.player.x + player_width // 2,
                        self.game_state.player.y + player_height // 2,
                        random.uniform(-6, 6), random.uniform(-6, 2),
                        RED, random.randint(30, 60)
                    )

                if self.game_state.power_up_manager.is_active("invincible"):
                    pass
                elif self.game_state.power_up_manager.is_active("shield"):
                    self.game_state.power_up_manager.active["shield"] = []
                else:
                    self.game_state.shake_time = 0.3
                    self.mode = GameMode.GAME_OVER
                    if int(self.game_state.score) > self.high_score:
                        self.high_score = int(self.game_state.score)
                        self.game_state.high_score = self.high_score
                    return

        for block in blocks_to_remove:
            block.kill()
        self.game_state.blocks_dodged += len(blocks_to_remove)

        for power_up in self.game_state.power_ups:
            if player_hitbox.colliderect(power_up.rect):
                power_up.kill()
                self.game_state.power_up_manager.apply_powerup(power_up.type)
                self.game_state.powerups_collected += 1

                color = PowerUp.POWER_UP_TYPES[power_up.type]["color"]
                self.game_state.add_floating_text(power_up.x, power_up.y - 20, power_up.type.upper(), color, self.fonts['small'])

                for _ in range(12):
                    self.game_state.add_particle(
                        power_up.x, power_up.y,
                        random.uniform(-5, 5), random.uniform(-6, -2),
                        color, random.randint(40, 70)
                    )

        for coin in self.game_state.coins:
            if player_hitbox.colliderect(coin.rect):
                coin.kill()
                self.game_state.score += 50
                self.game_state.coins_collected += 1
                
                self.game_state.add_floating_text(coin.x, coin.y - 20, "+50", YELLOW, self.fonts['small'])

                for _ in range(10):
                    self.game_state.add_particle(
                        coin.x, coin.y,
                        random.uniform(-4, 4), random.uniform(-5, -2),
                        YELLOW, random.randint(30, 50)
                    )

        score_increment = 60.0 * dt
        if self.game_state.power_up_manager.is_active("double"):
            score_increment *= 2.0
        self.game_state.score += score_increment

        if self.game_state.check_score_milestone():
            self.game_state.level_up()

            for _ in range(20):
                self.game_state.add_particle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    random.uniform(-8, 8), random.uniform(-8, 8),
                    YELLOW, random.randint(50, 80)
                )

    def draw_background(self, shake_x: int = 0, shake_y: int = 0):
        # Scrolling background
        bg_rect1 = self.background_img.get_rect()
        bg_rect1.topleft = (0, int(self.bg_y) - SCREEN_HEIGHT)
        self.screen.blit(self.background_img, (bg_rect1.x + shake_x, bg_rect1.y + shake_y))
        
        bg_rect2 = self.background_img.get_rect()
        bg_rect2.topleft = (0, int(self.bg_y))
        self.screen.blit(self.background_img, (bg_rect2.x + shake_x, bg_rect2.y + shake_y))
        
        # Road dashes
        dash_length = 40
        dash_gap = 40
        total_dash = dash_length + dash_gap
        offset = int(self.bg_y) % total_dash
        
        for divider in [277, 400, 522]:
            for y in range(-total_dash, SCREEN_HEIGHT + total_dash, total_dash):
                draw_y = y + offset
                if -dash_length < draw_y < SCREEN_HEIGHT:
                    dash_surface = pygame.Surface((4, dash_length), pygame.SRCALPHA)
                    dash_surface.fill((255, 255, 255, 150))
                    self.screen.blit(dash_surface, (divider - 2 + shake_x, draw_y + shake_y))
        
        # Speed lines rendering
        for line in self.speed_lines:
            line_surface = pygame.Surface((3, line["length"]), pygame.SRCALPHA)
            line_surface.fill((255, 255, 255, 100))
            self.screen.blit(line_surface, (line["x"] + shake_x, int(line["y"] - line["length"]) + shake_y))

    def render(self):
        if self.mode == GameMode.MENU:
            self.draw_background()
            if self.viewing_high_score:
                self.menu_screen.render_high_score(self.screen, self.high_score)
            else:
                self.menu_screen.render_main_menu(self.screen, self.high_score)

        elif self.mode == GameMode.DIFFICULTY_SELECT:
            self.draw_background()
            self.menu_screen.render_difficulty_select(self.screen)

        elif self.mode in (GameMode.PLAYING, GameMode.PAUSED, GameMode.GAME_OVER):
            shake_x, shake_y = 0, 0
            if self.mode == GameMode.PLAYING and getattr(self.game_state, "shake_time", 0.0) > 0:
                shake_x = random.randint(-5, 5)
                shake_y = random.randint(-5, 5)

            shake_x += int(self.camera_sway)

            self.draw_background(shake_x, shake_y)

            if shake_x != 0 or shake_y != 0:
                for block in self.game_state.blocks:
                    self.screen.blit(block.image, (block.rect.x + shake_x, block.rect.y + shake_y))
                for power_up in self.game_state.power_ups:
                    self.screen.blit(power_up.image, (power_up.rect.x + shake_x, power_up.rect.y + shake_y))
                for coin in self.game_state.coins:
                    self.screen.blit(coin.image, (coin.rect.x + shake_x, coin.rect.y + shake_y))
                for particle in self.game_state.particles:
                    self.screen.blit(particle.image, (particle.rect.x + shake_x, particle.rect.y + shake_y))
                for text in self.game_state.floating_texts:
                    self.screen.blit(text.image, (text.rect.x + shake_x, text.rect.y + shake_y))
                self.screen.blit(self.game_state.player.image, (self.game_state.player.rect.x + shake_x, self.game_state.player.rect.y + shake_y))
            else:
                self.game_state.blocks.draw(self.screen)
                self.game_state.power_ups.draw(self.screen)
                self.game_state.coins.draw(self.screen)
                self.game_state.particles.draw(self.screen)
                self.game_state.floating_texts.draw(self.screen)
                self.screen.blit(self.game_state.player.image, self.game_state.player.rect.topleft)

            if self.game_state.power_up_manager.is_active("shield"):
                UIRenderer.render_shield_glow(self.screen, self.game_state.player.x + shake_x,
                                             self.game_state.player.y + shake_y,
                                             self.player_img.get_width(),
                                             self.player_img.get_height())

            if self.mode in (GameMode.PLAYING, GameMode.PAUSED):
                UIRenderer.render_hud(self.screen, self.game_state, self.fonts, SCREEN_WIDTH)

            if self.mode == GameMode.PAUSED:
                self.menu_screen.render_pause_menu(self.screen)
            elif self.mode == GameMode.GAME_OVER:
                self.menu_screen.render_game_over(self.screen, self.game_state)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        dt = 0.0

        while running:
            if self.mode == GameMode.MENU:
                running = self.handle_menu_input()
                self.update_background(dt, 500.0)
            elif self.mode == GameMode.DIFFICULTY_SELECT:
                running = self.handle_difficulty_input()
                self.update_background(dt, 500.0)
            elif self.mode == GameMode.PLAYING:
                running = self.handle_gameplay_input()
                self.update_gameplay(dt)
            elif self.mode == GameMode.PAUSED:
                running = self.handle_pause_input()
            elif self.mode == GameMode.GAME_OVER:
                running = self.handle_gameover_input()

            self.render()
            dt = self.clock.tick(FPS) / 1000.0

        self.save_high_score()
        pygame.quit()
