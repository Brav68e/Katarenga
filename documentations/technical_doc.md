# Technical Documentation – Katarenga

## 1. General Introduction

Katarenga is a board game application inspired by chess, developed in Python. This technical document is intended for developers who want to understand, maintain, or extend the project. It details the architecture, modules, features, user interface, network management, assets, and game rules. Each component and button of the application is explained in depth to facilitate onboarding and code maintenance.

## 2. Project Architecture

The application is structured into several main modules, each responsible for a specific part of the functionality: board management, user interface, game logic, network management, assets, and subclasses for game entities. The project follows a modular architecture to facilitate maintenance and extension. It uses Python and his sets of library to allow more dynamic changes and ease to use. With Pygame used for the graphical part, we improve the overall possibilities for development and enhance greatly user experience.

### 2.1 Class Diagram

![alt text](<Class_Diagram/small_diagram.png>)

Here is a diagram that shows the main class used for this project (thus we use OOP).
If you want a more detailed version of this diagram, you can found one in documentations/Class_Diagram/class_diagram.svg
The diagram above should be enough to understand the main ideas and below stand more explanation.

## 3. Folder and File Structure

- `main.py`: Application entry point.
- `README.md`: User documentation.
- `documentations/technical_doc.md`: This technical document.
- `Source_files/`: Contains the main application logic.
  - `application.py`: Application and main loop management.
  - `Game_UI.py`: Graphical interface and screen management.
  - `Games.py`: Logic for different game modes.
  - `Assets/`: Images, sounds, fonts, rules.
  - `Board_handling/`: Creation, modification, and deletion of boards and regions.
  - `Menu/`: Management of various menus and welcome screens.
  - `Network/`: Online multiplayer management (client, server, hub).
  - `Sub_class/`: Definitions of game entities (pawn, player, button, etc.).

---

## 4. Detailed Description of Main Modules

### 4.1 application.py

This module manages the initialization of the application, it acts as a launcher to the first interfaces

#### Main Functions:
- Display the small introduction
- Initialization of the main window

### 4.2 Game_UI.py

This module manages the graphical interface: the board, buttons, and game information. It uses graphical assets to provide a pleasant and intuitive user experience.

#### Main Functions:
- Display of different screens (Is the extention of the Games class but handle the grapical part)
- Placement and management of interactive buttons
- Dynamic display of information (score, current player, etc.)
- Management of animations and transitions

### 4.3 Games.py

This module contains the logic for the different game modes (Katarenga, Isolation, Congress). It manages the specific rules for each mode, victory detection, and game progression.

#### Main Functions:
- Game initialization according to the selected mode
- Application of game rules
- Turn management
- Detection of victory or draw conditions
- Contain the overall logic of the games

This is where belong each win condition method. Here is a glimpse of how they work :

- Katarenga : This win condition keep track of the amount of pawn each player got (this info is stored in the player) and check if camps are occupied looping through a specific dictionnary.
- Congress : The hardest one, need to keep track of each pawn and try to cross all nodes of a graph using Breadth First Search algorithm
- Isolation : A special set is create and keep track of available tiles, once none are available, the game is over

---

## 5. Board Management (Board_handling)

The `Board_handling` folder contains modules responsible for creating, modifying, and deleting the game board and its regions. These modules are essential for board flexibility and adaptation to different game modes.

### 5.1 Board_creation.py
This module manages the generation of the game board. It allows dynamic creation of boards of various sizes and shapes depending on the selected game mode.

#### Main Functions:
- Generation of the tile grid
- Initial placement of regions and pawns
- Initialization of each tile's properties (color, type, region)
- Read all the available regions stored on our local JSON ressource file

#### Usage Example:
When starting a new game, the main function of this module is called to generate the board adapted to the chosen mode.

### 5.2 Create_region.py
This module allows the creation and assignment of regions on the board. Regions are sets of tiles sharing a color or common property.

#### Main Functions:
- Definition of regions by coordinates
- Assignment of colors and properties to regions
- Persistence management for regions (save/load using JSON)

### 5.3 Region_deletion.py
This module manages the dynamic deletion or modification of regions on the board, useful for certain game modes or board editing.

#### Main Functions:
- Deletion of a region by its identifier (aka his position in an array)
- Real-Time update of the region's deletion and dynamic visual
- Reassignment of properties if necessary

---

## 6. Subclass Management (Sub_class)

The `Sub_class` folder contains the definitions of the game's basic entities: buttons, pawns, players, regions, and tiles. Each subclass encapsulates the properties and behaviors associated with its entity.
It contain the widely used button class for graphical purpose (Pygame doesn't provide button Object) and variety of in-game Object

### 6.1 button.py
Manages the creation and behavior of interactive UI buttons. 
It can be used with either text, image or both and allow easy hovering animation

#### Main Properties:
- Position (x, y)
- Dimensions (width, height)
- Displayed text and/or image
- State (active, inactive, hovered)

#### Main Methods:
- `update(screen)`: Displays the button on screen
- `is_clicked(x,y)`: Detects a click on the button
- `change_color(color)`: Updates the visual state based on interaction

### 6.2 pawn.py
Defines the game pawns, their properties, and their movements.

#### Main Properties:
- Board position
- Owner
- Pawn type (king, queen, etc.)

### 6.3 player.py
Represents a player (human or AI).

#### Main Properties:
- Name
- Pawn_amount

### 6.4 region.py
Defines a board region (set of tiles sharing a property).

#### Main Properties:
- region (basically a list of list with Tiles Object)

#### Main Methods:
- flip()
- rotate()
- display(screen, imgs, pos, tile_size) : Allow to blit the region on a surface, need a screen, a dict of imgs and initial top-left corner as well as tile-size

### 6.5 tile.py
Defines an individual board tile.

#### Main Properties:
- pawn_on (pawn or empty)
- deplacement_pattern (king, bishop, knight, ...)

### Notes :
- You have to know that all the object that might need to be transfert (mainly in-game Object) have a method to be either transform into dictionnary or transform back from it.
The main purpose of this is to allow registration in JSON files and to either read, delete or write in those files.
- Those class are primarly used together, which means we use composition alot. For instance, a Region object contain a 2D list of Tiles Object which may contain a Pawn Object (who has his turn refer a Player Object)

---

## 7. User Interface (UI)

Katarenga's user interface is designed to be intuitive and responsive. It consists of several screens: main menu, game mode selection, game board, in-game menus, victory/defeat screens, and settings. Each screen is managed by dedicated modules and uses interactive graphical elements and buttons.

### 7.1 Main Menu
The main menu is the application's entry point. It offers several buttons:
- **Solo**: Launches the game mode selection in solo vs AI.
- **Local Multiplayer**: Launches the game mode selection in local 1vs1. 
- **Multiplayer**: Accesses the online hub or local network connection.
- **Rules**: Displays the rules for the selected game mode.
- **Options**: Allows modification of graphical and sound options.
- **Create Tiles**: Redirect to the Create tiles interface
- **Quit**: Closes the application.

Each button is instantiated via the `button` class and provides visual (color or icon change on hover/click) and audio feedback (sound played on activation).
The buttons used in the selection bar below are a special kind of buttons only used here, you can find more informations about them in this specific file

#### Button Functionality:
- **Event Handling**: Each button listens for mouse events (hover, click) and adapts its visual state.
- **Callback Triggering**: When a button is clicked, it triggers an associated function (e.g., start a game, open a menu).
- **Accessibility**: Buttons are sized for easy access, even on small screens.

### 7.2 Game Mode Selection
In the menu allow the game selection with a bottom bar with games logo:
- **Katarenga**
- **Isolation**
- **Congress**

Each mode is presented with a selection button. The choice configures the board and rules via the `Games.py` module.
`Games.py` receive the informations he needs such as usernames and board configuration and handle the rest.

### 7.3 In-game Menus
The in-game menu allows:
- Resuming the game
- Quitting the game

### 7.4 Victory/Defeat Screens
At the end of a game, a screen displays the result (player `x` won the game) with a summary of scores and buttons to replay or return to the main menu.
This small pop-up is handle via a method in `Games_UI`

### 7.5 Settings
The settings screen allows adjustment of:
- Sound volume
- Screen resolution (fullscreen, windowed)

---

## 8. Button and Interaction Details

Each application button is an instance of the `button` class and has:
- A unique identifier (We're using his reference since we don't need much more)
- Text or an icon
- Position and size
- State (normal, hovered, clicked, disabled)

### 8.1 Button Lifecycle
1. **Creation**: Instantiated with its properties (label, position, callback)
2. **Interaction**: Monitors mouse events
3. **Activation**: Triggers the callback on click
4. **Update**: Changes state based on interaction

### 8.2 Button Examples
- **Next button**: allow to continue when pressed
- **Gamemode button**: allow to choose the gamemode(Solo, Online...)
- **Navigation Buttons** (arrows, back, next): Used in menus and rules navigation

Each button can be styled with an image (e.g., `Assets/Images/Utility/button.png`) or text, and has a sound effect (e.g., `Assets/Sounds/bouton.mp3`).

---

## 9. Asset Management (Images, Sounds, Fonts, Rules)

The `Assets/` folder centralizes all multimedia resources used by the application. Good asset management ensures visual and audio consistency, as well as ease of maintenance and extension.
You have to note that all of those assets are either hand-made or free to use. For more informations about sources, consider contacting us.

### 9.1 Images
Images are organized by usage:
- `Images/Board/`: Board pieces (e.g., `king.png`, `queen.png`, `region.png`)
- `Images/Game/`: Pawns, game backgrounds, move indicators
- `Images/Menu/`: Menu illustrations and backgrounds
- `Images/Utility/`: Buttons, arrows, various icons

Each image is loaded at startup of a UI related Object and referenced by its relative path. Images are used to:
- Display pawns and pieces on the board
- Style buttons and menus
- Illustrate regions and possible actions

### 9.2 Sounds
Sounds are stored in `Assets/Sounds/`:
- Button effects (`bouton.mp3`)
- Background music (`soundtrack.mp3`)
- Victory sounds (`win.mp3`)

Python scripts (`button_sound.py`, `win_sound.py`) handle sound playback during interactions. Sounds are played when:
- Clicking a button
- An important event occurs (win, loss)
- Background music during the game

### 9.3 Fonts
Fonts are in `Assets/Fonts/`:
- `font.ttf`, `font2.ttf` for UI text display

Fonts are loaded at launch and used for:
- Titles and menus
- Scores and game information
- Button text

### 9.4 Rules
Rules for each game mode are stored in `Assets/Rules/`:
- `katarenga_rules.txt`
- `isolation_rules.txt`
- `congress_rules.txt`

They are displayed on demand in the UI, allowing quick consultation and possible modification without touching the source code.

### 9.5 Data
The `Assets/Data_files/` folder contains structured data files (e.g., `region.json`) for region configuration or board state saving.
Those files are JSON formatted which means it's easy to read and modify. They contain an array of Region Object (for more information about the formatting check in the `/sub_class`

---

## 10. Network Management (Multiplayer)

The `Network/` folder contains modules for online or local network play. The network architecture is designed to support multiple connection modes and ensure game synchronization.

### 10.1 Client.py
This module manages a player's connection to an online or local network game.
- Connects to a server via IP/port
- Sends and receives player actions
- Handles disconnections and reconnections

### 10.2 Server.py
This module allows hosting a multiplayer game.
- Accepts multiple clients
- Synchronizes game state between all players
- Manages turns and action validation

### 10.3 Online_hub.py
This module acts as a centralized lobby to find or create online games.
- Lists available games
- Creates and manages rooms
- Assigns players to games

#### Security and Robustness
- Validates received actions
- Handles network errors and connection losses
- Handling errors with try... catch

All of the network is based on Socket and Thread concepts and associated libraries in Python. 
Multiple Thread are used to handle :
- Communication with the server
- Send information to everyone
- Receiving information and return response 
---

## 11. Game Rules Management and Implementation

Rules are managed at two levels: in rule files (for display) and in code (for enforcement during the game).

### 11.1 Rules in Code
Each game mode (Katarenga, Isolation, Congress) has its own functions for move validation, victory detection, and turn management in `Games.py`.
- Allowed moves based on pawn type and region
- Win/loss/draw conditions
- Special actions (e.g., undo, capture)

### 11.2 Rules Displayed to the User
Text files in `Assets/Rules/` are read and displayed in the UI by accessing it in the settings section of the menu, allowing players to consult the rules at any time.

### 11.3 Adding or Modifying Rules
To add a new game mode or modify a rule:
- Add/modify the rule text file
- Implement the logic in `Games.py` (move validation, win conditions, etc.)
- Adapt the UI if necessary (new buttons, new information)


---

## 12. Development Best Practices

- **Modularity**: Keep each feature in a dedicated module.
- **Explicit Naming**: Use clear and consistent names for variables, functions, and files.
- **Comments**: Document complex functions and key algorithms.
- **Error Handling**: Provide explicit error messages and logs for debugging.
- **UI/Logic Separation**: Do not mix game logic and display.
- **Asset Management**: Centralize paths and avoid duplicates.
- **Version Control**: Use a version control system (e.g., Git) and clear commits.

---

### 14. Contribution Guidelines
- Read the technical documentation before any major modification.
- Discuss important changes with the team.
- Respect the folder structure and existing logic.
- Document any new feature in this file.

---

# End of Katarenga Technical Documentation
