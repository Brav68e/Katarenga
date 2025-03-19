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
        self.first_turn = True
        self.camps = {"B": [False, False], "N": [False, False]}  # Track if camps are occupied
    
    def afficher(self):
        """Display the board with row and column numbers for easier testing."""
        print("   " + " ".join(str(i) for i in range(self.taille)))  # Print column numbers
        for i, ligne in enumerate(self.grille):
            print(f"{i} " + " ".join(str(case) for case in ligne))  # Print row number and row content
    
    def placer_pion(self, x: int, y: int, pion: str):
        """Place a pawn on the board at the given position."""
        if pion not in ('B', 'N'):
            raise ValueError("The pawn must be 'B' (white) or 'N' (black).")
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].pion = pion
        else:
            raise IndexError("Coordinates out of bounds.")
    
    def retirer_pion(self, x: int, y: int):
        """Remove a pawn from a tile on the board."""
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].pion = None
        else:
            raise IndexError("Coordinates out of bounds.")
    
    def definir_type_case(self, x: int, y: int, nom: str):
        """Define the type of a tile (e.g., king, knight, rook, bishop, etc.)."""
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].nom = nom
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
                if tile.pawn_on == 'B' and x == 0:  # Player B's pawns can move into Player N's camps
                    for i, camp_used in enumerate(self.camps['N']):
                        if not camp_used:
                            moves.append((x, f"camp_{i}"))
                elif tile.pawn_on == 'N' and x == self.taille - 1:  # Player N's pawns can move into Player B's camps
                    for i, camp_used in enumerate(self.camps['B']):
                        if not camp_used:
                            moves.append((x, f"camp_{i}"))

                return moves
            else:
                raise ValueError("No pawn on the specified tile.")
        else:
            raise IndexError("Coordinates out of bounds.")

    def move_pawn(self, x: int, y: int, new_x: int, new_y: int, current_player: str):
        """
        Move a pawn from (x, y) to (new_x, new_y) according to the game rules.
        :param x: Current x-coordinate of the pawn.
        :param y: Current y-coordinate of the pawn.
        :param new_x: New x-coordinate of the pawn.
        :param new_y: New y-coordinate of the pawn.
        :param current_player: The player ('B' or 'N') attempting to move the pawn.
        """
        print(f"Player {current_player} attempting to move pawn from ({x}, {y}) to ({new_x}, {new_y})")
        if not (0 <= x < self.taille and 0 <= y < self.taille and 0 <= new_x < self.taille and 0 <= new_y < self.taille):
            print("Move out of bounds.")
            raise IndexError("Coordinates out of bounds.")

        tile = self.grille[x][y]
        target_tile = self.grille[new_x][new_y]

        if not tile.pawn_on:
            print(f"No pawn on the tile at ({x}, {y}).")
            raise ValueError("No pawn on the specified tile.")

        if tile.pawn_on != current_player:
            print(f"Player {current_player} cannot move pawn at ({x}, {y}) owned by {tile.pawn_on}.")
            raise ValueError(f"Player {current_player} cannot move pawn at ({x}, {y}) owned by {tile.pawn_on}.")

        # Get possible moves from the starting tile
        possible_moves = self.get_possible_moves(x, y)
        print(f"Possible moves for pawn at ({x}, {y}): {possible_moves}")

        # Check if the requested move is valid
        if (new_x, new_y) not in possible_moves:
            print(f"Move to ({new_x}, {new_y}) is not valid.")
            raise ValueError("Invalid move.")

        # If the target tile has a pawn, capture it
        if target_tile.pawn_on:
            print(f"Capturing pawn at ({new_x}, {new_y}).")
            target_tile.pawn_on = None

        # Move the pawn
        print(f"Moving pawn from ({x}, {y}) to ({new_x}, {new_y}).")
        target_tile.pawn_on = tile.pawn_on
        tile.pawn_on = None

        # Check if the pawn reaches the opponent's line
        if (target_tile.pawn_on == 'B' and new_x == 0) or (target_tile.pawn_on == 'N' and new_x == self.taille - 1):
            print(f"Pawn at ({new_x}, {new_y}) reached the opponent's line.")
            if not any(self.camps[target_tile.pawn_on]):
                print("No free camps available for this pawn.")
                raise ValueError("No free camps available for this pawn.")
            self.enter_camp(target_tile.pawn_on)

    def enter_camp(self, pion: str):
        """
        Handle a pawn entering the opponent's camp.
        :param pion: The pawn ('B' or 'N').
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
        :return: The winner ('B' or 'N') or None if there is no winner yet.
        """
        if all(self.camps['N']):  # If both camps of 'N' are occupied, 'B' wins
            return 'B'
        elif all(self.camps['B']):  # If both camps of 'B' are occupied, 'N' wins
            return 'N'
        return None

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
        row = [Tile(deplacement_pattern=tile_types[i][j]) for j in range(taille)]
        grille.append(row)

    # Place pawns for both players on their base lines
    for i in range(taille):
        grille[1][i].place_pawn('N')  # Player N's pawns on the second row
        grille[6][i].place_pawn('B')  # Player B's pawns on the second-to-last row

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
        combined_board[0][i].place_pawn('N')  # Player N's pawns on the second row
        combined_board[7][i].place_pawn('B')  # Player B's pawns on the second-to-last row

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

    current_player = 'B'
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
            plateau.move_pawn(x, y, new_x, new_y, current_player)

            # Check for a winner
            winner = plateau.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                break

            # Switch player
            current_player = 'N' if current_player == 'B' else 'B'

        except ValueError as e:
            print(f"Invalid input or move: {e}")
        except IndexError as e:
            print(f"Move out of bounds: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    play_game()
