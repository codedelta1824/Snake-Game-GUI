# Snake-Game-GUI
This project is a desktop recreation of the classic Google Play Games Snake, built entirely in Python (utilizing the Pygame library for rendering and input handling).  The game operates on a 2D grid matrix where a continuous while loop serves as the game's heartbeat, processing events, updating mechanics, and redrawing

🗂️ A professional, comprehensive README.md file tailored specifically to your project's architecture has been generated.

#📜 Brief Summary of the Generated Documentation
This README.md explicitly captures the Python and Pygame-based structure of your Google Play Games Snake Clone, adhering strictly to your file map:

#Project Overview: 
Focuses on a native Python implementation using Pygame to match the iconic look, fluid 2D grid matrix mechanics, and progressive difficulty of the Google Play version.

Folder Structure: Maps out your layout cleanly:
Snake Game GUI/
├── main.py
└── src/
    ├── config.py
    ├── states.py
    └── ui.py

Core Logic: Explains the frame-rate-locked game loop, coordinate tuple manipulation for the snake array (insert at head / pop at tail), non-overlapping food generation logic, and input sanitization (preventing immediate 180-degree self-collisions).

Modular Breakdown:

main.py: The entry point managing instantiation, event routing, and the execution loop.

config.py: Centralized storage for grid math, RGB colors, screen sizing, and difficulty speed scaling.

states.py: A clean Finite State Machine handling MENU, PLAYING, PAUSED, and GAME_OVER.

ui.py: Handles rendering text layers, drawing grid-aligned rectangles, and formatting score counters.
    
