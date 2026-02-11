# Tank Battle Game - Development Learnings

## 2026-02-10 - Project Completion

### Technical Decisions
- **pygame-ce vs pygame**: Used pygame-ce 2.5.6 instead of pygame 2.6.1 due to better wheel support on macOS (avoids SDL compilation issues)
- **Python Version**: Pinned to Python 3.11 for compatibility with pygame-ce
- **Package Management**: Used uv for 10-100x faster dependency resolution compared to pip

### Architecture Patterns
- **Sprite-based Architecture**: Used pygame.sprite.Sprite for all game objects (PlayerTank, EnemyTank, Bullet, Brick, Steel)
- **Group Management**: Organized sprites into Groups (enemies, bullets, all_sprites) for batch updates and collision detection
- **Game Loop Pattern**: Standard pygame loop - event handling → update → draw → flip
- **Procedural Graphics**: All graphics generated via pygame.draw (no external assets needed)

### Implementation Details

#### Bullet System
- Simple vector-based movement (direction * speed)
- Automatic boundary checking (kill when out of bounds)
- Owner tracking ('player' or 'enemy') for collision filtering

#### Map Generation
- 20x15 grid (40px tiles) = 800x600 window
- Random obstacle placement (30-50 obstacles)
- Player spawn protection (clear area at bottom center)
- 60% bricks (destructible) / 40% steel (indestructible)

#### Enemy AI
- Random direction changes every 1-2 seconds
- Simple obstacle avoidance (change direction on collision)
- Automatic shooting with cooldown (1.5-3 seconds based on type)
- Three enemy types: Basic (red, 1 HP), Fast (green, 1 HP), Heavy (gray, 2 HP)

#### Collision Detection
- Player bullets → Enemies: Kill enemy, +100 score
- Enemy bullets → Player: Reduce lives, trigger invincibility
- Bullets → Map: Destroy brick, stop at steel

### Challenges & Solutions
1. **SDL Build Issues**: pygame 2.6.1 requires SDL headers on macOS. Solution: Use pygame-ce which has pre-built wheels.
2. **Import Path Issues**: src/ directory structure requires proper PYTHONPATH or relative imports. Solution: Used explicit imports in game.py.
3. **Tank Movement**: Initial update() method conflict between manual and automatic control. Solution: Separated handle_input() from move() methods.

### QA Verification Results
All Definition of Done items verified:
- ✅ Game launches and runs at 60 FPS
- ✅ Player movement (arrow keys) and shooting (space)
- ✅ Enemy AI with automatic movement and shooting
- ✅ Random map generation with obstacles
- ✅ Collision detection (bullet-enemy, bullet-player, bullet-map)
- ✅ Game over (lives = 0) and victory (all enemies dead) conditions
- ✅ Scoring system (+100 per enemy)

### File Structure
```
tank-war/
├── main.py (3.6K) - Game loop and initialization
├── src/
│   ├── bullet.py (4.0K) - Bullet class
│   ├── enemy.py (8.0K) - EnemyTank with AI
│   ├── game.py (4.6K) - Game manager
│   ├── map.py (6.9K) - Map, Brick, Steel classes
│   └── tank.py (10K) - PlayerTank class
└── pyproject.toml - uv project config
```

### Performance Notes
- 60 FPS stable on modern hardware
- No memory leaks detected in testing
- Sprite groups efficiently handle collision detection

### Future Enhancements (Out of Scope)
- Power-ups (shield, speed boost, rapid fire)
- Multiple levels with increasing difficulty
- Sound effects and background music
- High score persistence
- Two-player mode
