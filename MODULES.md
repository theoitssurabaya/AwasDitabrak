# AwasDitabrak Module Structure

This document describes the modular architecture of AwasDitabrak.

## Directory Overview

```
AwasDitabrak/
├── main.py              # Entry point
├── AwasDitabrak.py      # Backward compatibility wrapper
├── game.py              # Main game controller
├── constants.py         # Configuration and constants
├── game_state.py        # Game state management
├── menu.py              # Menu system and enums
├── ui_renderer.py       # UI and HUD rendering
├── powerup.py           # Power-up system
├── particle.py          # Particle effects
├── requirements.txt     # Python dependencies
└── README.md            # User documentation
```

## Module Descriptions

### **main.py** (Entry Point)
- Simple entry point for running the game
- Initializes pygame and starts the game loop
- Usage: `python main.py`

### **AwasDitabrak.py** (Backward Compatibility)
- Wrapper that imports from main.py
- Allows running with `python AwasDitabrak.py`
- Maintains compatibility with old usage patterns

### **game.py** (Main Controller) - ~350 lines
The core game loop and controller.

**Key Classes:**
- `Game`: Main game controller
  - `__init__()`: Initialize all systems
  - `start_game(difficulty)`: Start a new game
  - `handle_*_input()`: Input handlers for different game modes
  - `update_gameplay()`: Update game logic each frame
  - `render()`: Render current screen
  - `run()`: Main game loop

**Responsibilities:**
- Asset loading and management
- Event handling and input processing
- Game loop orchestration
- Mode switching (menu → playing → paused → gameover)
- Collision detection and response
- Scoring and level progression

**Key Methods:**
```python
game = Game()              # Initialize
game.start_game(Difficulty.NORMAL)  # Start new game
game.run()               # Run main loop
```

### **constants.py** (Configuration) - ~40 lines
All static configuration values.

**Contents:**
- Screen dimensions (SCREEN_WIDTH, SCREEN_HEIGHT)
- Colors (WHITE, BLUE, RED, etc.)
- Asset paths (PLAYER_CAR_IMAGE, ROAD_IMAGE)
- Game settings (FPS, INITIAL_BLOCK_SPEED)
- Road configuration (LANES, ROAD_TOP)
- Spawn rates and probabilities

**Usage:**
```python
from constants import SCREEN_WIDTH, BLUE, INITIAL_MAX_BLOCKS
```

### **game_state.py** (State Management) - ~80 lines
Encapsulates all game state.

**Key Classes:**
- `GameState`: Complete game state container

**Attributes:**
- Player state: `current_lane_index`, `player_x`, `player_y`
- Game data: `score`, `level`, `blocks`, `power_ups`, `particles`
- Power-ups: `power_up_manager` (PowerUpManager instance)
- Statistics: `blocks_dodged`, `powerups_collected`
- Difficulty settings: `block_speed`, `max_blocks`, `level_speed_increase`

**Key Methods:**
```python
state = GameState(Difficulty.NORMAL)
state.reset()              # Reset for new game
state.add_particle(...)    # Create particle effect
state.check_score_milestone()  # Check for level up
state.level_up()           # Increase level and difficulty
```

### **menu.py** (Menu System) - ~120 lines
All menu-related functionality.

**Key Classes:**
- `GameMode`: Enum for game states
- `Difficulty`: Enum for difficulty levels
- `DifficultySettings`: Dataclass for difficulty configuration
- `MenuScreen`: Renders and manages menus

**Key Functions:**
- `create_fonts()`: Initialize pygame fonts

**Enums:**
```python
GameMode.MENU, DIFFICULTY_SELECT, PLAYING, PAUSED, GAME_OVER
Difficulty.EASY, NORMAL, HARD
```

**Configuration:**
```python
DIFFICULTY_CONFIG  # Maps difficulty to settings
```

**Menu Rendering Methods:**
```python
menu.render_main_menu(screen, high_score)
menu.render_difficulty_select(screen)
menu.render_pause_menu(screen)
menu.render_game_over(screen, game_state)
```

### **powerup.py** (Power-up System) - ~110 lines
Power-up mechanics and management.

**Key Classes:**
- `PowerUp`: Individual power-up collectible
- `PowerUpManager`: Tracks active power-ups

**PowerUp Types:**
- `shield`: Blue, 5 seconds - blocks one collision
- `speed`: Green, 4 seconds - 1.5x block speed
- `double`: Yellow, 6 seconds - 2x points
- `invincible`: Red, 3 seconds - immune to collisions

**PowerUp Methods:**
```python
power_up = PowerUp(x, y, "shield")
power_up.draw(screen)
```

**PowerUpManager Methods:**
```python
manager = PowerUpManager()
manager.apply_powerup("shield")           # Activate
manager.update()                          # Each frame
manager.is_active("shield")               # Check status
manager.get_remaining_time("shield")      # Duration left
manager.deactivate_all()                  # Clear all
```

### **particle.py** (Visual Effects) - ~40 lines
Particle effect system.

**Key Classes:**
- `Particle`: Individual visual particle

**Usage:**
```python
particle = Particle(x, y, vx, vy, color, lifetime)
particle.update()      # Each frame
particle.draw(screen)  # Render
particle.is_alive()    # Check if visible
```

**Physics:**
- Velocity-based movement
- Gravity applied each frame
- Fades out over lifetime
- Size decreases as it ages

### **ui_renderer.py** (HUD & Effects) - ~80 lines
User interface rendering.

**Key Classes:**
- `UIRenderer`: Static methods for UI rendering

**Static Methods:**
```python
UIRenderer.render_hud(screen, game_state, fonts)
# Renders: Score, Level, High Score, Active Power-ups, Difficulty

UIRenderer.render_particles(screen, particles)
# Renders all particle effects

UIRenderer.render_shield_glow(screen, player_x, player_y, width, height)
# Renders shield visual effect
```

## Data Flow

### Game Startup
1. `main.py` initializes pygame
2. `Game.__init__()` loads assets, creates MenuScreen
3. `Game.run()` enters main loop

### Main Loop (Each Frame)
1. **Event Handling**: Input processing based on current mode
2. **Update**: Game logic updates (if PLAYING mode)
   - Player movement
   - Block spawning and movement
   - Collision detection
   - Score/level updates
   - Power-up duration management
3. **Render**: Draw current screen
4. **Clock**: Sync to FPS

### Game Modes
- `MENU`: Display main menu
- `DIFFICULTY_SELECT`: Select difficulty
- `PLAYING`: Active gameplay
- `PAUSED`: Game paused, show pause menu
- `GAME_OVER`: Game over, show stats

### Collision Detection
1. Create player rect with inset
2. Check against block rects
3. Check against power-up rects
4. Apply effects (shield, invincible, damage)
5. Create particles for feedback

## Module Dependencies

```
main.py
  └─ game.py
      ├─ constants.py
      ├─ menu.py
      │   └─ constants.py
      ├─ game_state.py
      │   ├─ particle.py
      │   ├─ powerup.py
      │   │   └─ constants.py
      │   └─ menu.py
      ├─ powerup.py
      │   └─ constants.py
      ├─ ui_renderer.py
      │   ├─ constants.py
      │   └─ particle.py
      └─ pygame
```

## Adding New Features

### Add a New Power-up Type
1. Add to `PowerUp.POWER_UP_TYPES` in `powerup.py`
2. Add handling in `game.py` collision detection
3. Add UI display in `ui_renderer.py`

### Add a New Menu Screen
1. Add method to `MenuScreen` in `menu.py`
2. Add corresponding `GameMode` enum value
3. Call in `game.py` render and input methods

### Modify Game Balance
1. Edit constants in `constants.py`
2. Edit difficulty config in `menu.py`
3. Adjust spawn rates, speeds, durations

## Testing Individual Modules

```bash
# Test imports
./venv/bin/python -c "from game import Game; print('OK')"

# Test game state
./venv/bin/python -c "from game_state import GameState; from menu import Difficulty; s = GameState(Difficulty.NORMAL); print('OK')"

# Test power-ups
./venv/bin/python -c "from powerup import PowerUpManager; m = PowerUpManager(); m.apply_powerup('shield'); print('OK')"
```

## Performance Considerations

- **Particle Limit**: Max ~50 particles active simultaneously
- **Block Limit**: Max blocks determined by difficulty
- **FPS**: Fixed at 60 FPS for consistent gameplay
- **Memory**: All game state held in GameState instance

## Future Improvements

- Add sound system module
- Add level/wave system
- Add achievements/unlockables
- Add settings menu (volume, difficulty preset)
- Add pause save/load functionality
- Separate collision system into own module
