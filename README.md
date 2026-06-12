# 🚗 Awas Ditabrak - Watch Out for the Crash!

An addictive 2D arcade game built with Python and Pygame. Navigate through traffic, collect coins and power-ups, and beat your high score!

The game has been recently overhauled with **advanced cinematic visuals** (camera sway, floating text, parallax roads) and is completely compiled for the web using **WebAssembly**!

## 🌐 Play the Web Version

You don't need to install anything to play! The game is compiled to WebAssembly via `pygbag`.
If you are hosting this repository on GitHub Pages using the `gh-pages` branch, you can play the game instantly in your browser.

## 🎮 Quick Start (Desktop)

### Prerequisites
- Python 3.12+
- Pygame 2.6+
- Pygbag 0.9.3+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the included virtual environment
source venv/bin/activate
```

### Run the Game Locally

```bash
python main.py
```

### Build for Web (WebAssembly)

```bash
pygbag --build .
```
This generates a deployable static web bundle in `build/web/`.

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

1. **Survive**: Avoid incoming zig-zagging cars on the highway.
2. **Collect**: Grab coins for +50 points and power-ups for special abilities.
3. **Score**: Earn points continuously every second you survive.
4. **Level Up**: Reach score milestones to increase difficulty.
5. **Beat High Score**: Try to beat your best score.

## ✨ Features & Visuals

### Cinematic Visual System
- **Camera Sway**: The entire game camera sways physically based on your steering momentum.
- **Parallax Road Dashes**: High-speed scrolling dashed lines generate an intense sense of velocity.
- **Floating Feedback**: Collecting coins (+50) or Power-Ups spawns satisfying floating pop-up text.
- **Particle System**: Exhaust trails emit from your car, violent geometry bursts occur on crashes, and colored auras trail your car when power-ups are active!
- **Frozen Crash-Cam**: Dying freezes the game state and washes the screen in a dramatic red overlay.

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

## 🏗️ Architecture

- **Pygame Sprites**: All game entities inherit from `pygame.sprite.Sprite` and are batched via `pygame.sprite.Group` for hyper-efficient rendering and collision detection.
- **Asyncio Loop**: The game loop runs natively as an `async def` and yields `await asyncio.sleep(0)` every frame. This guarantees that the game doesn't block the browser's JavaScript event loop when exported via Pygbag.
- **Delta Time (dt)**: All movement, physics, animations, and particle lifetimes are multiplied by delta time, ensuring the game runs at the exact same speed regardless of monitor refresh rate or lag spikes.

## 📁 Project Structure

```
AwasDitabrak/
├── assets/images/          # Game sprites
├── src/                    # Source code
│   ├── constants.py        # Game configuration
│   ├── core/
│   │   ├── game.py        # Main async game loop
│   │   └── game_state.py  # Centralized sprite groups
│   ├── ui/
│   │   ├── menu.py        # Animated overlays & UI
│   │   └── ui_renderer.py # HUD rendering
│   └── entities/
│       ├── coin.py        # Pulsing coin sprites
│       ├── enemy.py       # Zig-zag rotation physics
│       ├── particle.py    # Particles & Floating Text
│       ├── player.py      # Player physics & bounds
│       └── powerup.py     # Power-up drop system
├── build/web/             # Pygbag generated WASM deployment
├── main.py                # Asyncio Entry point
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## 📄 License

This project is free to use and modify.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!
