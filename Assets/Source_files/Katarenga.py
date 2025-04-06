from Sub_class.tile import *
from Sub_class.pawn import *
from Sub_class.player import *
from Board_creation import Delete_region


class Plateau:
    
    def __init__(self, taille: int = None, grille=None):
        """
        Initialize a board either by creating an empty grid or using an existing grid of Tile objects.
        """
        if grille:
            self.taille = len(grille)
            self.grille = grille
        elif taille:
            self.taille = taille
            self.grille = [[Tile() for _ in range(taille)] for _ in range(taille)]
        else:
            raise ValueError("You must provide either a size or an existing grid.")
        self.camps = {"W": [False, False], "B": [False, False]}  # Track if camps are occupied
    
    def afficher(self):
        """Display the board with row and column numbers for easier testing."""
        print("   " + " ".join(str(i) for i in range(self.taille)))  # Print column numbers
        for i, ligne in enumerate(self.grille):
            print(f"{i} " + " ".join(str(case) for case in ligne))  # Print row number and row content
    
    def place_pawn(self, x: int, y: int, pawn: str):
        """Place a pawn on the board at the given position."""
        if pawn not in ('W', 'B'):
            raise ValueError("The pawn must be 'B' or 'W'.")
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].place_pawn(pawn)  # Use the Tile's place_pawn method
        else:
            raise IndexError("Coordinates out of bounds.")
    
    def remove_pawn(self, x: int, y: int):
        """Remove a pawn from a tile on the board."""
        if 0 <= x < self.taille and 0 <= y < self.taille:
            if self.grille[x][y].get_pawn() is not None:  # Check if a pawn exists
                self.grille[x][y].place_pawn(None)  # Use the Tile's place_pawn method to remove the pawn
            else:
                raise ValueError("No pawn to remove at the specified position.")
        else:
            raise IndexError("Coordinates out of bounds.")
    
    def get_possible_moves(self, x: int, y: int):
        """
        Get possible moves for the pawn on the tile at (x, y).
        :param x: x-coordinate of the tile.
        :param y: y-coordinate of the tile.
        :return: List of valid moves [(new_x, new_y), ...].
        """
        if 0 <= x < self.taille and 0 <= y < self.taille:
            tile = self.grille[x][y]
            if tile.pawn_on:
                moves = tile.get_possible_moves(x, y, self.grille)

                # Add camp movement if the pawn is on the opponent's line
                if tile.pawn_on == 'B' and x == 0:  # Player B's pawns can move into Player W's camps
                    for i, camp_used in enumerate(self.camps['W']):
                        if not camp_used:
                            moves.append((x, f"camp_{i}"))
                elif tile.pawn_on == 'W' and x == self.taille - 1:  # Player W's pawns can move into Player B's camps
                    for i, camp_used in enumerate(self.camps['B']):
                        if not camp_used:
                            moves.append((x, f"camp_{i}"))

                return moves
            else:
                raise ValueError("No pawn on the specified tile.")
        else:
            raise IndexError("Coordinates out of bounds.")

    def validate_move(self, x: int, y: int, new_x: int, new_y: int, current_player: str):
        """
        Validate a move before executing it.
        :param x: Current x-coordinate of the pawn.
        :param y: Current y-coordinate of the pawn.
        :param new_x: New x-coordinate of the pawn.
        :param new_y: New y-coordinate of the pawn.
        :param current_player: The player ('B' or 'W') attempting to move the pawn.
        :raises ValueError or IndexError if the move is invalid.
        """
        if not (0 <= x < self.taille and 0 <= y < self.taille and 0 <= new_x < self.taille and 0 <= new_y < self.taille):
            raise IndexError("Coordinates out of bounds.")

        tile = self.grille[x][y]
        target_tile = self.grille[new_x][new_y]

        if not tile.pawn_on:
            raise ValueError("No pawn on the specified tile.")

        if tile.pawn_on != current_player:
            raise ValueError(f"Player {current_player} cannot move pawn at ({x}, {y}) owned by {tile.pawn_on}.")

        # Get possible moves from the starting tile
        possible_moves = self.get_possible_moves(x, y)
        if (new_x, new_y) not in possible_moves:
            raise ValueError("Invalid move.")

    def move_pawn(self, x: int, y: int, new_x: int, new_y: int):
        """
        Move a pawn from (x, y) to (new_x, new_y).
        :param x: Current x-coordinate of the pawn.
        :param y: Current y-coordinate of the pawn.
        :param new_x: New x-coordinate of the pawn.
        :param new_y: New y-coordinate of the pawn.
        """
        tile = self.grille[x][y]
        target_tile = self.grille[new_x][new_y]

        # If the target tile has a pawn, capture it
        if target_tile.pawn_on:
            target_tile.pawn_on = None

        # Move the pawn
        target_tile.pawn_on = tile.pawn_on
        tile.pawn_on = None

        print(f"Pawn moved from ({x}, {y}) to ({new_x}, {new_y}).")

    def enter_camp(self, pion: str):
        """
        Handle a pawn entering the opponent's camp.
        :param pion: The pawn ('B' or 'W').
        """
        if pion in self.camps and not all(self.camps[pion]):
            for i in range(2):
                if not self.camps[pion][i]:
                    self.camps[pion][i] = True
                    break
        else:
            raise ValueError("Both camps are already occupied.")

    def check_winner(self):
        """
        Check if there is a winner.
        :return: The winner ('B' or 'W') or None if there is no winner yet.
        """
        if all(self.camps['W']):  # If both camps of 'W' are occupied, 'B' wins
            return 'B'
        elif all(self.camps['B']):  # If both camps of 'B' are occupied, 'W' wins
            return 'W'
        return None

    def bot_move(self, bot_player: str):
        """
        Perform a random move for the bot.
        :param bot_player: The bot's player ('B' or 'W').
        """
        possible_moves = []

        # Collect all possible moves for the bot's pawns
        for x in range(self.taille):
            for y in range(self.taille):
                tile = self.grille[x][y]
                if tile.pawn_on == bot_player:
                    moves = self.get_possible_moves(x, y)
                    for move in moves:
                        possible_moves.append((x, y, move[0], move[1]))

        # If no moves are possible, the bot cannot play
        if not possible_moves:
            print(f"No possible moves for bot ({bot_player}).")
            return

        # Randomly select a move
        selected_move = random.choice(possible_moves)
        x, y, new_x, new_y = selected_move

        # Validate and execute the move
        try:
            self.validate_move(x, y, new_x, new_y, bot_player)
            self.move_pawn(x, y, new_x, new_y)
            print(f"Bot ({bot_player}) moved pawn from ({x}, {y}) to ({new_x}, {new_y}).")
        except Exception as e:
            print(f"Bot move failed: {e}")

# Example usage
import random
import pygame

def creer_grille_personnalisee():
    """
    Create a custom grid with specific tile types for each row and place pawns on their base lines.
    """
    taille = 8
    grille = []

    # Define specific tile types for each row
    tile_types = [
        ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],  # Top row
        ["Rook"] * taille,  # Second row
        ["Bishop"] * taille,  # Third row
        ["Knight"] * taille,  # Fourth row
        ["Knight"] * taille,  # Fifth row
        ["Bishop"] * taille,  # Sixth row
        ["Rook"] * taille,  # Seventh row
        ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"],  # Bottom row
    ]

    # Create the grid with the specified tile types
    for i in range(taille):
        row = [Tile(deplacement_pattern=tile_types[i][j].lower()) for j in range(taille)]
        grille.append(row)

    # Place pawns for both players on their base lines
    for i in range(taille):
        grille[1][i].place_pawn('B')  # Player B's pawns on the second row
        grille[6][i].place_pawn('W')  # Player W's pawns on the second-to-last row

    # Debugging: Print the grid after initialization
    print("Grid after initialization:")
    for row in grille:
        print([str(tile) for tile in row])

    return grille

def creer_plateau_depuis_board_creation():
    """
    Create a game board using the combined regions from Board_creation.py and initialize pawns.
    """
    print("Initializing board using Board_creation...")
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    board_creator = Delete_region(screen)
    board_creator.run()

    # Combine regions to create the board
    combined_board = board_creator.combine_regions()

    # Initialize pawns for both players
    taille = len(combined_board)
    for i in range(taille):
        combined_board[0][i].place_pawn('B')  # Player B's pawns on the second row
        combined_board[7][i].place_pawn('W')  # Player W's pawns on the second-to-last row

    # Debugging: Print the combined board with pawns
    print("Combined board with pawns initialized:")
    for row in combined_board:
        print([str(tile) for tile in row])

    return combined_board

def play_game():
    """
    Play the game in a functional mode without a graphical interface.
    """
    print("Welcome to Katarenga!")

    # Create the board using Board_creation
    grille = creer_plateau_depuis_board_creation()

    # Initialize the Plateau with the new board
    plateau = Plateau(grille=grille)
    plateau.afficher()

    current_player = 'W'
    while True:
        print(f"\nPlayer {current_player}'s turn.")
        print("Enter your move in the format: x y new_x new_y")
        print("Example: 1 0 2 0 to move the pawn at (1, 0) to (2, 0).")
        plateau.afficher()

        try:
            move = input("Your move: ").strip()
            print(f"Received input: {move}")
            if move.lower() == "quit":
                print("Game ended.")
                break

            x, y, new_x, new_y = map(int, move.split())
            plateau.validate_move(x, y, new_x, new_y, current_player)
            plateau.move_pawn(x, y, new_x, new_y)

            # Check for a winner
            winner = plateau.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                break

            # Switch player
            current_player = 'B' if current_player == 'W' else 'W'

        except ValueError as e:
            print(f"Invalid input or move: {e}")
        except IndexError as e:
            print(f"Move out of bounds: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    play_game()

