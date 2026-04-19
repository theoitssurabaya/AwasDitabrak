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
        player_width, player_height = self.player_img.get_size()
        self.game_state.player_x = ROAD_LANES[self.game_state.current_lane_index] - player_width // 2
        self.game_state.player_y = SCREEN_HEIGHT - player_height - 20
        self.game_state.target_x = self.game_state.player_x
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
                    self.game_state.current_lane_index = max(0, self.game_state.current_lane_index - 1)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.game_state.current_lane_index = min(len(ROAD_LANES) - 1,
                                                             self.game_state.current_lane_index + 1)
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

    def update_gameplay(self):
        player_width, player_height = self.player_img.get_size()
        block_width, block_height = self.block_img.get_size()

        current_block_speed = self.game_state.block_speed
        if self.game_state.power_up_manager.is_active("speed"):
            current_block_speed *= 1.5

        target_x = ROAD_LANES[self.game_state.current_lane_index] - player_width // 2
        if self.game_state.player_x != target_x:
            self.game_state.player_x += (target_x - self.game_state.player_x) // 5

        active_lanes = [block[2] for block in self.game_state.blocks]
        if len(self.game_state.blocks) < self.game_state.max_blocks:
            available_lanes = [lane for lane in ROAD_LANES if lane not in active_lanes]
            if available_lanes and random.randint(1, 100) <= BLOCK_SPAWN_CHANCE:
                new_lane = random.choice(available_lanes)
                self.game_state.blocks.append([new_lane - block_width // 2, ROAD_TOP, new_lane])

        if random.randint(1, POWERUP_SPAWN_CHANCE) == 1:
            power_lane = random.choice(ROAD_LANES)
            power_type = random.choice(list(PowerUp.POWER_UP_TYPES.keys()))
            self.game_state.power_ups.append(PowerUp(power_lane, ROAD_TOP, power_type))

        for block in self.game_state.blocks:
            block[1] += current_block_speed
        for power_up in self.game_state.power_ups:
            power_up.y += current_block_speed // 2

        self.game_state.blocks = [block for block in self.game_state.blocks if block[1] < SCREEN_HEIGHT]
        self.game_state.power_ups = [p for p in self.game_state.power_ups if p.y < SCREEN_HEIGHT]

        self.game_state.update_particles()
        self.game_state.power_up_manager.update()

        player_rect = pygame.Rect(self.game_state.player_x + 10, self.game_state.player_y + 10,
                                 player_width - 20, player_height - 20)

        blocks_to_remove = []
        for block in self.game_state.blocks:
            block_rect = pygame.Rect(block[0] + 10, block[1] + 10, block_width - 20, block_height - 20)
            if player_rect.colliderect(block_rect):
                blocks_to_remove.append(block)
                for _ in range(5):
                    self.game_state.add_particle(
                        self.game_state.player_x + player_width // 2,
                        self.game_state.player_y + player_height // 2,
                        random.uniform(-3, 3), random.uniform(-3, 1),
                        RED, 30
                    )

                if self.game_state.power_up_manager.is_active("invincible"):
                    pass
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

        powerups_to_remove = []
        for power_up in self.game_state.power_ups:
            pu_rect = pygame.Rect(power_up.x - power_up.radius, power_up.y - power_up.radius,
                                 power_up.radius * 2, power_up.radius * 2)
            if player_rect.colliderect(pu_rect):
                powerups_to_remove.append(power_up)
                self.game_state.power_up_manager.apply_powerup(power_up.type)
                self.game_state.powerups_collected += 1

                color = PowerUp.POWER_UP_TYPES[power_up.type]["color"]
                for _ in range(8):
                    self.game_state.add_particle(
                        power_up.x, power_up.y,
                        random.uniform(-4, 4), random.uniform(-5, -1),
                        color, 40
                    )

        self.game_state.power_ups = [p for p in self.game_state.power_ups if p not in powerups_to_remove]

        score_increment = 1
        if self.game_state.power_up_manager.is_active("double"):
            score_increment = 2
        self.game_state.score += score_increment

        if self.game_state.check_score_milestone():
            self.game_state.level_up()

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
            self.screen.blit(self.background_img, (0, 0))

            for block in self.game_state.blocks:
                self.screen.blit(self.block_img, (block[0], block[1]))

            for power_up in self.game_state.power_ups:
                power_up.draw(self.screen)

            UIRenderer.render_particles(self.screen, self.game_state.particles)

            if self.game_state.power_up_manager.is_active("shield"):
                UIRenderer.render_shield_glow(self.screen, self.game_state.player_x,
                                             self.game_state.player_y,
                                             self.player_img.get_width(),
                                             self.player_img.get_height())

            self.screen.blit(self.player_img, (int(self.game_state.player_x), int(self.game_state.player_y)))

            UIRenderer.render_hud(self.screen, self.game_state, self.fonts, SCREEN_WIDTH)

            if self.mode == GameMode.PAUSED:
                self.menu_screen.render_pause_menu(self.screen)

        elif self.mode == GameMode.GAME_OVER:
            self.screen.blit(self.background_img, (0, 0))
            self.menu_screen.render_game_over(self.screen, self.game_state)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
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
            self.clock.tick(FPS)

        self.save_high_score()
        pygame.quit()
