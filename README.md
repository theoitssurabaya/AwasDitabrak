# 🚗 Awas Ditabrak - Watch Out for the Crash!

An addictive 2D arcade game built with Python and Pygame. Navigate through traffic, collect power-ups, and beat your high score!

## 🎮 Quick Start

### Prerequisites
- Python 3.7+
- Pygame 2.6+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the included virtual environment
./venv/bin/python main.py
```

### Run the Game

```bash
python main.py
```

or (backward compatible):

```bash
python AwasDitabrak.py
```

## 🕹️ How to Play

### Controls

| Action | Keys |
|--------|------|
| Move Left | `A` or `←` |
| Move Right | `D` or `→` |
| Pause Game | `SPACE` |
| Return to Menu | `ESC` |
| Navigate Menus | `↑` `↓` |
| Select Menu Item | `ENTER` |
| Restart Game | `R` (on Game Over) |
| Go to Menu | `M` (on Game Over) |

### Objective

1. **Survive**: Avoid incoming cars on the highway
2. **Collect**: Grab power-ups for special abilities
3. **Score**: Earn points every second you survive
4. **Level Up**: Reach score milestones to increase difficulty
5. **Beat High Score**: Try to beat your best score

### Gameplay Tips

- Watch the power-up timers on the right side of the screen
- Speed changes during speed boost - adjust your timing
- Double points multiplier doesn't double power-up spawn rate
- Invincibility makes you immune but you can still collect power-ups
- Easy mode gives you more breathing room to learn controls

## ✨ Features

### 4 Power-Up Types

| Power-Up | Color | Duration | Effect |
|----------|-------|----------|--------|
| **Shield** 🛡️ | Blue | 5s | Absorbs one collision |
| **Speed Boost** ⚡ | Green | 4s | Blocks move 1.5x faster |
| **Double Points** 2️⃣ | Yellow | 6s | Earn 2x score |
| **Invincible** ★ | Red | 3s | Immune to collisions |

### 3 Difficulty Levels

| Difficulty | Speed | Block Limit | Feeling |
|-----------|-------|-------------|---------|
| **Easy** | 0.8x | 2 blocks | Relaxed |
| **Normal** | 1.0x | 3 blocks | Balanced |
| **Hard** | 1.3x | 4 blocks | Intense |

### Visual Effects

- Particle effects for collisions, pickups, and level-ups
- Shield glow animation when shield is active
- Smooth lane transitions
- Screen updates at 60 FPS

### Game Statistics

Track your progress with:
- Current score and high score
- Current level
- Blocks dodged
- Power-ups collected
- Active difficulty level

## 📁 Project Structure

```
AwasDitabrak/
├── assets/images/          # Game sprites
│   ├── car.png            # Player car
│   ├── car2.png           # Enemy cars
│   └── road.png           # Background
├── src/                    # Source code
│   ├── constants.py        # Game configuration
│   ├── core/
│   │   ├── game.py        # Main game controller
│   │   └── game_state.py  # Game state management
│   ├── ui/
│   │   ├── menu.py        # Menu system & difficulty
│   │   └── ui_renderer.py # HUD rendering
│   └── entities/
│       ├── particle.py    # Visual effects
│       └── powerup.py     # Power-up system
├── main.py                # Entry point
├── AwasDitabrak.py        # Backward compatibility wrapper
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🎯 Game Mechanics

### Scoring

- **Base**: +1 point per frame
- **With Double Points**: +2 points per frame
- **Per Second**: ~60 points/second (60 FPS)

### Level Progression

- **Level 2**: 1,000 points
- **Level 3**: 2,000 points
- **Level N**: N × 1,000 points

Each level increases block speed and max concurrent blocks.

### Collision Detection

- Player collision area is inset by 10 pixels for better feel
- Blocks must fully overlap with player hitbox to register collision
- Power-ups have larger collision radius for easier pickup

### Speed Mechanics

- Speed affects block movement and power-up drop speed
- Speed boost multiplies current speed by 1.5x
- Level-up increases speed gradually (1.0 base + 0.5-1.5 per level depending on difficulty)

## 🏗️ Architecture

### Game Loop (60 FPS)

1. **Input**: Capture keyboard events
2. **Update**: 
   - Move player based on input
   - Move blocks and power-ups
   - Check collisions
   - Update power-up durations
   - Update particles
   - Check score milestones
3. **Render**: Draw current game state
4. **Sync**: Lock to 60 FPS

### Game States

- `MENU`: Main menu screen
- `DIFFICULTY_SELECT`: Choose difficulty
- `PLAYING`: Active gameplay
- `PAUSED`: Game paused
- `GAME_OVER`: Final score screen

### Key Classes

- **Game**: Main controller, handles loop and events
- **GameState**: Stores all game data
- **MenuScreen**: Renders all menu screens
- **PowerUpManager**: Tracks active power-ups
- **UIRenderer**: Draws HUD and effects
- **Particle**: Visual effect objects

## 📊 Performance

- **FPS**: Fixed 60 FPS
- **Max Particles**: ~50 active simultaneously
- **Max Blocks**: Depends on difficulty (2-4)
- **Memory**: < 50 MB typical usage

## 🐛 Troubleshooting

### Game Won't Start
- Ensure Python 3.7+ is installed
- Check pygame is installed: `pip install pygame`
- Verify asset files exist in `assets/images/`

### Missing Graphics
- Check `assets/images/` folder contains car.png, car2.png, road.png
- If missing, game creates colored placeholders (still playable)

### Imports Fail
- Ensure you're running from the project root directory
- Check all `__init__.py` files exist in src folders

### Game Runs Slow
- Close other applications
- Check CPU usage (pygame should use < 5% CPU)
- Verify FPS counter shows ~60 FPS

## 🎓 Learning Resources

This project demonstrates:

- **Object-Oriented Programming**: Class-based architecture
- **Game Development**: Game loop, collision detection, state management
- **Python**: Modules, packages, imports, error handling
- **Pygame**: Sprites, event handling, rendering, collision
- **Code Organization**: Modular design, separation of concerns

## 📝 Future Improvements

Possible enhancements:
- Sound effects and background music
- Multiple lives system
- Combo counter
- Wave/stage system
- Leaderboard
- Settings menu (volume, keybindings)
- Mobile touch controls
- Achievements/unlockables

## 📄 License

This project is free to use and modify.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

**Enjoy the game! Try to beat your high score! 🏁**
