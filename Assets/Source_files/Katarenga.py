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
        """Display the board as a list of lists with characters."""
        tableau = [[str(case) for case in ligne] for ligne in self.grille]
        for ligne in tableau:
            print(ligne)
    
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
                if (tile.pawn_on == 'B' and x == self.taille - 1) or (tile.pawn_on == 'N' and x == 0):
                    for i, camp_used in enumerate(self.camps[tile.pawn_on]):
                        if not camp_used:
                            # Add a special move to the camp
                            moves.append((x, f"camp_{i}"))

                return moves
            else:
                raise ValueError("No pawn on the specified tile.")
        else:
            raise IndexError("Coordinates out of bounds.")

    def move_pawn(self, x: int, y: int, new_x: int, new_y: int):
        """
        Move a pawn from (x, y) to (new_x, new_y) according to the game rules.
        :param x: Current x-coordinate of the pawn.
        :param y: Current y-coordinate of the pawn.
        :param new_x: New x-coordinate of the pawn.
        :param new_y: New y-coordinate of the pawn.
        """
        if 0 <= x < self.taille and 0 <= y < self.taille and 0 <= new_x < self.taille and 0 <= new_y < self.taille:
            tile = self.grille[x][y]
            if tile.pawn_on:
                possible_moves = self.get_possible_moves(x, y)
                if (new_x, new_y) in possible_moves:
                    target_tile = self.grille[new_x][new_y]
                    if target_tile.pawn_on:
                        if self.first_turn:
                            raise ValueError("Captures are not allowed on the first turn.")
                        else:
                            # Capture the opponent's pawn
                            target_tile.pawn_on = None
                    # Move the pawn
                    target_tile.pawn_on = tile.pawn_on
                    tile.pawn_on = None
                    self.first_turn = False

                    # Check if the pawn reaches the opponent's line
                    if (target_tile.pawn_on == 'B' and new_x == self.taille - 1) or (target_tile.pawn_on == 'N' and new_x == 0):
                        if not any(self.camps[target_tile.pawn_on]):
                            raise ValueError("No free camps available for this pawn.")
                        self.enter_camp(target_tile.pawn_on)
                else:
                    raise ValueError("Invalid move.")
            else:
                raise ValueError("No pawn on the specified tile.")
        else:
            raise IndexError("Coordinates out of bounds.")

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
    """Create a custom grid with varied tiles and pawns."""
    noms_cases = ["King", "Knight", "Rook", "Bishop", "Queen"]
    grille = [[Tile(random.choice(noms_cases), random.choice([None, 'B', 'N'])) for _ in range(8)] for _ in range(8)]
    return grille

# Create a board from a custom grid
grille_perso = creer_grille_personnalisee()

# Initialize the Plateau with the new board
plateau = Plateau(grille=grille_perso)
plateau.afficher()
