# Snake-Game-GUI

A polished desktop Snake game built in Python with Pygame. The project features a modern UI, WASD/arrow-key controls, a pause button, score tracking, and a game-over flow with restart support.

## Features
- Professional game window with a clean HUD
- Smooth snake movement on a grid-based board
- Controls using WASD or arrow keys
- Pause and resume with P, Escape, or the on-screen button
- Score and high-score tracking
- Menu, gameplay, pause, and game-over states

## Project Structure
- main.py: Game loop, input handling, and state transitions
- src/config.py: Colors, sizing, and board constants
- src/states.py: Game states for menu, playing, paused, and game over
- src/ui.py: Rendering helpers, buttons, overlays, and HUD

## Installation
1. Install Python 3.10+.
2. Install Pygame:
   ```bash
   pip install pygame
   ```

## Run the Game
```bash
python main.py
```

## Controls
- WASD or Arrow Keys: Move the snake
- P or Escape: Pause/Resume
- Mouse: Click the on-screen buttons

## Notes
The game uses the standard library and Pygame for rendering and input handling.
    
