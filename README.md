# Funny Game

A 2D survival shooter game built with Pygame where players face waves of different enemy types across changing environments.

## Game Overview

Funny Game is a wave-based 2D shooter where you control a character that must survive against increasingly difficult waves of enemies. As you progress, the environment changes and the challenge increases. The game features different types of enemies, each with unique behaviors and attack patterns.

## Features

- **Wave-based progression system** - Face increasingly difficult challenges as you advance
- **Multiple enemy types**:
  - Basic melee enemies that chase the player
  - Projectile enemies that attack from a distance
  - Fluid enemies that can release special effects (likely area damage)
- **Dynamic environments** - Maps change as you progress through waves
- **Health system** - Manage your character's health to survive
- **Shooting mechanics** - Aim and shoot at enemies to defeat them
- **Game states** - Main menu, gameplay, tutorial, and pause functionality

## Installation

### Requirements
- Python 3.x
- Pygame

### Steps
1. Ensure Python is installed on your system
2. Install Pygame using pip:
   ```
   pip install pygame
   ```
3. Clone or download this repository
4. Make sure you have the required resource folders:
   - `Images/` - Contains all game sprites and textures
   - `Fonts/` - Contains game fonts
5. Run the game by executing:
   ```
   python Main.py
   ```

## How to Play

### Controls
- **Movement**: WASD or Arrow keys to move your character
- **Shooting**: Mouse click to shoot in the direction of your cursor
- **Pause**: ESC key to pause the game
- **Menu Navigation**: Mouse to select menu options

### Gameplay
- Survive as many waves as possible
- Defeat enemies to progress to the next wave
- The environment changes as you reach certain wave milestones
- The game ends when your character's health reaches zero

## File Structure

The game is built with an object-oriented approach, with each component in its own file:

- `Main.py` - Game entry point, contains the main game loop, menu system, and wave management
- `Player.py` - Player class with movement, shooting, and health management
- `Enemy.py` - Base enemy class with movement and collision detection
- `ProjectileEnemy.py` - Enemy subclass that can fire projectiles at the player
- `FluidEnemy.py` - Enemy subclass with special area effect attacks
- `Projectile.py` - Projectile class used by both player and enemies
- `Target.py` - Target class for destructible objects in the game

## Technical Details

The game is built using Pygame, a set of Python modules designed for writing video games. It utilizes:

- Object-oriented programming principles
- Sprite-based rendering
- Collision detection
- Event-driven input handling
- State management for different game screens

## Dependencies

- Python 3.x
- Pygame library

## License

This project is available for educational and personal use.
