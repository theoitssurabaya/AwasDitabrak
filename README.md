# 🚗 Awas Ditabrak - Watch Out for Crash!

Fun game make with Python and Pygame. You drive, avoid metal beasts (cars), grab shiny round things (coins), and get big score!

Game have new pretty things! Screen shake, floating words, road lines go fast. Works in magic web browser!

## 🌐 Play on Magic Web

No install! Game use WebAssembly magic (`pygbag`).
If use GitHub Pages, just open browser and play!

## 🎮 Quick Start (Desktop)

### Need These First
- Python 3.12+
- Pygame 2.6+
- Pygbag 0.9.3+

### How to Install

```bash
# Get things game need
pip install -r requirements.txt

# Or use magic box (venv)
source venv/bin/activate
```

### Run Game on Big Box

```bash
python main.py
```

### Build for Web

```bash
pygbag --build .
```
Make game folder in `build/web/`.

## 🕹️ How to Play

### Button Smash

| What Do | Buttons |
|--------|------|
| Go Left | `A` or `←` |
| Go Right | `D` or `→` |
| Stop Game | `SPACE` |
| Go Back | `ESC` |
| Move in Menu | `↑` `↓` |
| Pick Thing | `ENTER` |
| Start Over | `R` (When Dead) |
| Menu | `M` (When Dead) |

### What to Do

1. **Not Die**: Dodge zig-zag metal beasts on big path.
2. **Take Things**: Grab shiny coins for +50. Grab glowing boxes for magic power.
3. **Get Big Number**: Stay alive, number go up!
4. **Get Harder**: Number get big, game get fast!
5. **Be the Best**: Get biggest number ever!

## ✨ Pretty Things & Magic

### Eye Candy & Ear Candy
- **Camera Shake**: Screen go wobble when you steer hard!
- **Fast Road Lines**: Lines zoom past, make you feel fast!
- **Floating Words**: Grab shiny thing, words float up!
- **Dust & Sparkles**: Smoke from car, shapes explode when crash, magic glow when power-up active!
- **Red Freeze**: Die, screen turn red and freeze. Much sad.
- **Magic Noise**: Menu have slow drum, game have fast drum! You hear all!

### 4 Magic Powers

| Power | Color | Time | What Do |
|----------|-------|----------|--------|
| **Shield** 🛡️ | Blue | 5s | Stop one crash! |
| **Go Fast** ⚡ | Green | 4s | Bad things move faster! |
| **Two Times** 2️⃣ | Yellow | 6s | Number go up twice as fast! |
| **No Hurt** ★ | Red | 3s | Cannot die! |

### 3 Hardness Levels

| Hardness | Speed | Bad Things | Feel |
|-----------|-------|-------------|---------|
| **Baby** | 0.8x | 2 | Sleepy |
| **Normal** | 1.0x | 3 | Good |
| **Ooga Booga**| 1.3x | 4 | Crazy |

## 🏗️ How Game Made

- **Pygame Sprites**: Game things use `pygame.sprite.Sprite`. Put in `pygame.sprite.Group` to draw fast and hit fast.
- **Asyncio Loop**: Game run with `async def`. Do `await asyncio.sleep(0)`. Make sure web browser not break.
- **Time Magic (dt)**: Move, shake, and sparkles use time math. Game always same speed on any box.

## 📁 Cave Drawings Structure

```
AwasDitabrak/
├── assets/images/          # Pictures
├── src/                    # Brain of game
│   ├── constants.py        # Magic numbers
│   ├── core/
│   │   ├── game.py        # Big game loop
│   │   └── game_state.py  # Groups of things
│   ├── ui/
│   │   ├── menu.py        # Pretty menus
│   │   └── ui_renderer.py # Draw score
│   └── entities/
│       ├── coin.py        # Shiny things
│       ├── enemy.py       # Bad zig-zag things
│       ├── particle.py    # Sparkles & Words
│       ├── player.py      # You
│       └── powerup.py     # Magic boxes
├── build/web/             # Web magic
├── main.py                # Start here
├── requirements.txt       # Things needed
└── README.md              # You look at this
```

## 📄 License

Free to use! Make game yours!

## 🤝 Help Make Better

Copy, fix, make more fun!
