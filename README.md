# Katarenga
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-latest-green.svg)

## About
Katarenga is a cross-platform board game application developed in Python, featuring multiple game variants and online multiplayer functionality. This project was developed as a final B.Eng1 project by:

- Thomas Dannequin
- Laureen Audin 
- Gabriel Verschatse

## Features

### Game Modes
- **Katarenga**: A strategic board game with unique tile movement rules
- **Congress**: Alternative game variant
- **Isolation**: Additional game variant

### Play Options
- **Solo Play**: Play against AI
- **Local Multiplayer**: Play with a friend on the same device
- **Online Multiplayer**: Connect and play against other players over network

### Board and Game Customization
- **Region Creation Tool**: Design your own game regions with customizable tiles
- **Board Creation**: Combine regions to create complete game boards

## Project Structure

### Main Components
- `main.py`: Entry point of the application
- `Assets/application.py`: Main application controller

### Game Logic
- `Assets/Source_files/Games.py`: Core game logic implementation
- `Assets/Source_files/Game_template.py`: Template class for game implementations
- `Assets/Source_files/Game_UI.py`: User interface for game interactions

### Multiplayer Components
- `Assets/Source_files/Server.py`: Server-side implementation for online play
- `Assets/Source_files/Client.py`: Client-side networking
- `Assets/Source_files/Online_hub.py`: Online lobby and matchmaking

### Creation Tools
- `Assets/Source_files/Create_region.py`: Tool for creating custom game regions
- `Assets/Source_files/Board_creation.py`: Interface for building game boards
- `Assets/Source_files/Region_deletion.py`: Management of created regions

### User Interface
- `Assets/Source_files/Menu.py`: Main menu and navigation

### Game Resources
- `Assets/Source_files/Data_files/`: Game data storage
- `Assets/Source_files/Images/`: Game graphics
- `Assets/Source_files/fonts/`: Text fonts
- `Assets/Source_files/Sounds/`: Game audio
- `Assets/Source_files/rules/`: Game rules documentation

## Requirements
- Python 3.x
- Pygame
- OpenCV (for video playback)
- Socket library (for networking)

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/brav68e/Katarenga.git


2. Install the required dependencies:

pip install pygame opencv-python

3. Run the game:

python main.py
```

## How to Play

### Main Menu
Navigate through the game modes using the bottom menu icons:
- Katarenga
- Congress
- Isolation
- Settings (includes options, rules, and tile creation)

### Game Controls
- Click to select a piece
- Click again on a valid tile to move
- Game rules are accessible from the Settings menu

### Online Play
1. Choose "Online Multiplayer" from the main menu
2. Host a game or join an existing server
3. Select a game mode
4. Wait for an opponent to connect

### Creating Custom Content
1. Access "Create tiles" from the Settings menu
2. Design your custom region layouts
3. Save your designs to use them in games
4. Use the Board Creation tool to combine regions into a full game board

## Contributing
This project was developed as an educational exercise. If you wish to contribute or report issues, please contact the original developers.

## License
All rights reserved. This project is provided for educational purposes only.