import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Awas Ditabrak")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load and scale images
def load_and_scale_image(image_path, new_height):
    image = pygame.image.load(image_path)
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    new_width = int(new_height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, new_height))

# Load assets
player_img = load_and_scale_image("car.png", 80)  
block_img = load_and_scale_image("car2.png", 80)  
block_img = pygame.transform.rotate(block_img, 180)  
background_img = pygame.image.load("road.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  

# Player dimensions
player_width, player_height = player_img.get_size()

# Lanes and initial positions
LANES = [215, 340, 460, 585]
ROAD_TOP = -100

# Player settings
current_lane_index = 1
player_x = LANES[current_lane_index] - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 20
target_x = player_x  

# Blocks and power-ups
blocks = []
power_ups = []
block_speed = 5
MAX_BLOCKS = 3
POWER_UP_TYPES = ["shield"]

# Score and levels
score = 0
level = 1
level_up_score = 1000
shield_active = False
high_score_file = "high_score.txt"
high_score = 0

# Load high score
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read().strip())

# Font
font = pygame.font.SysFont(None, 36)

# Draw functions
def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_block(block):
    screen.blit(block_img, (block[0], block[1]))

def draw_power_up(power_up):
    pygame.draw.circle(screen, BLUE, (power_up[0], power_up[1]), 20)

def display_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def game_over_screen():
    screen.fill((0, 0, 0))
    display_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, YELLOW)
    display_text("Press R to Restart or Q to Quit", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()

# Main game loop
running = True
game_over = False

while running:
    if not game_over:
        # Draw background
        screen.blit(background_img, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  
                    current_lane_index = max(0, current_lane_index - 1)
                if event.key == pygame.K_d:  # Move right
                    current_lane_index = min(len(LANES) - 1, current_lane_index + 1)
        
        # Smooth lane transition animation
        target_x = LANES[current_lane_index] - player_width // 2
        if player_x != target_x:
            player_x += (target_x - player_x) // 5  

        # Add new blocks
        active_lanes = [block[2] for block in blocks]
        if len(blocks) < MAX_BLOCKS:
            available_lanes = [lane for lane in LANES if lane not in active_lanes]
            if available_lanes and random.randint(1, 100) <= 3:  
                new_lane = random.choice(available_lanes)
                blocks.append([new_lane - block_img.get_width() // 2, ROAD_TOP, new_lane])

        # Spawn power-ups
        if random.randint(1, 300) == 1:  
            power_lane = random.choice(LANES)
            power_ups.append([power_lane, ROAD_TOP, "shield"])

        # Move blocks and power-ups
        for block in blocks:
            block[1] += block_speed
        for power_up in power_ups:
            power_up[1] += block_speed // 2

        # Remove off-screen elements
        blocks = [block for block in blocks if block[1] < SCREEN_HEIGHT]
        power_ups = [power_up for power_up in power_ups if power_up[1] < SCREEN_HEIGHT]

        # Check for collisions with blocks
        player_rect = pygame.Rect(player_x + 10, player_y + 10, player_width - 20, player_height - 20)
        for block in blocks:
            block_rect = pygame.Rect(block[0] + 10, block[1] + 10, block_img.get_width() - 20, block_img.get_height() - 20)
            if player_rect.colliderect(block_rect):
                if shield_active:
                    shield_active = False  
                    blocks.remove(block)  
                else:
                    # Game over
                    if score > high_score:
                        high_score = score
                    game_over = True

        # Check for power-up collection
        for power_up in power_ups:
            power_up_rect = pygame.Rect(power_up[0] - 20, power_up[1] - 20, 40, 40)
            if player_rect.colliderect(power_up_rect):
                if power_up[2] == "shield":
                    shield_active = True
                power_ups.remove(power_up)

        # Update score and level
        score += 1
        if score >= level * level_up_score:
            level += 1
            block_speed += 1
            MAX_BLOCKS += 1

        # Draw player, blocks, and power-ups
        draw_player(player_x, player_y)
        for block in blocks:
            draw_block(block)
        for power_up in power_ups:
            draw_power_up(power_up)

        # Display score, high score, and shield status
        display_text(f"Score: {score}", 10, 10)
        display_text(f"High Score: {high_score}", 10, 40)
        if shield_active:
            display_text("Shield Active!", SCREEN_WIDTH // 2 - 100, 10, BLUE)

        pygame.display.flip()
        clock.tick(FPS)

    else:
        # Game over screen
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    score = 0
                    level = 1
                    block_speed = 5
                    MAX_BLOCKS = 3
                    blocks.clear()
                    power_ups.clear()
                    shield_active = False
                    game_over = False
                if event.key == pygame.K_q:  # Quit game
                    running = False

# Save high score when exiting
if score > high_score:
    high_score = score
with open(high_score_file, "w") as file:
    file.write(str(high_score))

pygame.quit()
