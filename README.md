# AwasDitabrak 🚗💨

**AwasDitabrak** (Watch Out for the Crash!) is an enhanced 2D arcade game built using Python and Pygame. Test your reflexes as you navigate through traffic, collect power-ups, select difficulty levels, and try to beat your highest score!

## 🌟 Features

### Core Gameplay
- **Smooth Lane Transitions:** Fluid movement between 4 lanes with smooth animations
- **Dynamic Difficulty:** Game gets progressively faster as you level up
- **Persistent High Score:** Your best score is saved locally for tracking progress

### Power-up System (4 Types!)
- **🛡 Shield (Blue):** Absorbs one collision, lasts 5 seconds
- **⚡ Speed Boost (Green):** Doubles block speed and makes the game more exciting, lasts 4 seconds
- **2️⃣ Double Points (Yellow):** Earn 2x points temporarily, lasts 6 seconds
- **★ Invincibility (Red):** Complete immunity from collisions, lasts 3 seconds

### Menu & Navigation
- **Main Menu:** Start game, view high score, or quit
- **Difficulty Selection:** Choose between Easy, Normal, or Hard
- **Pause Functionality:** Press SPACE to pause/resume anytime
- **Game Over Screen:** Shows your final score, level reached, blocks dodged, and whether you beat the high score

### Enhanced Controls
- **Movement:** Use `A`/`D` keys OR `Arrow Keys` (Left/Right)
- **Pause:** `SPACE` to pause/resume during gameplay
- **Navigation:** `Arrow Keys` (Up/Down) to select menu items
- **Menu Actions:** `ENTER` to confirm, `M` for menu, `R` to restart, `ESC` to return to menu

### Visual Enhancements
- **Particle Effects:** 
  - Colorful burst effect when collecting power-ups
  - Red collision particles on crash
  - Yellow star particles on level-up
- **Shield Glow:** Blue circle glow around player when shield is active
- **Status Indicators:** Real-time display of active power-ups and remaining duration
- **Level Display:** See your current level, difficulty, and game statistics

### Difficulty Levels
| Difficulty | Speed | Max Blocks | Description |
|-----------|-------|-----------|-------------|
| **Easy** | 0.8x | -1 | Slower blocks, easier gameplay |
| **Normal** | 1.0x | +0 | Balanced challenge |
| **Hard** | 1.3x | +1 | Faster blocks, more intense |

## 🎮 Controls

### During Gameplay
| Key | Action |
|-----|--------|
| **A** or **←** | Move Left |
| **D** or **→** | Move Right |
| **SPACE** | Pause/Resume |
| **ESC** | Return to Menu |

### In Menus
| Key | Action |
|-----|--------|
| **↑/↓** | Navigate Menu |
| **ENTER** | Select Option |
| **SPACE** | Return/Confirm |
| **M** | Go to Main Menu |
| **R** | Restart Game |

## 📁 Project Structure

The code is organized into modular components for better maintainability:

```
AwasDitabrak/
├── main.py              # Entry point
├── game.py              # Main game controller (350 lines)
├── constants.py         # Configuration values
├── game_state.py        # Game state management
├── menu.py              # Menu system
├── ui_renderer.py       # UI rendering
├── powerup.py           # Power-up mechanics
├── particle.py          # Visual effects
└── MODULES.md           # Technical documentation
```

For detailed module documentation, see [MODULES.md](MODULES.md).

## 🛠️ Prerequisites
Ensure you have Python 3.7+ installed and pygame library:

```bash
pip install -r requirements.txt
```

Or use the included virtual environment:
```bash
./venv/bin/python main.py
```

## 🚀 How to Play

1. **Start the Game:** Run `python AwasDitabrak.py`
2. **Select Difficulty:** Choose Easy, Normal, or Hard
3. **Avoid Traffic:** Use A/D or Arrow keys to dodge incoming cars
4. **Collect Power-ups:** Grab colored orbs to activate special abilities
5. **Survive & Score:** Each passing car increases your score
6. **Level Up:** Reach score thresholds to increase difficulty and speed
7. **Beat Your Score:** Try to beat your previous high score!

## 🎯 Game Mechanics

- **Scoring:** +1 point per frame normally, +2 with Double Points active
- **Level Progression:** Each level requires 1000 × level points (1000 for level 2, 2000 for level 3, etc.)
- **Speed Scaling:** Block speed increases slightly each level, more on Hard difficulty
- **Collision Detection:** Slightly inset from sprite edges for better gameplay feel
- **Invincible Frames:** After activating shield, it blocks exactly one collision then expires

## 📊 Statistics Tracked

- **Current Score:** Points accumulated in current game
- **High Score:** Best score across all games
- **Level:** Current game level
- **Blocks Dodged:** Total obstacles successfully avoided
- **Power-ups Collected:** Total power-up pickups
- **Difficulty:** Current difficulty level

## 🕶 Asset Requirements

The game requires the following image files in the same directory:
- `car.png` - Player car sprite
- `car2.png` - Enemy car sprite (will be flipped)
- `road.png` - Background road texture

If any asset is missing, the game will create colored rectangles as fallback.

## 💾 Save Files

- `high_score.txt` - Stores your highest score (auto-created on first game)
