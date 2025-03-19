from Sub_class.tile import *
from Sub_class.pawn import *
from Sub_class.player import *
from Board_creation import Delete_region

class Tile:
    def __init__(self, deplacement_pattern, pawn_on=None, collision=None):
        self.deplacement_pattern = deplacement_pattern
        self.pawn_on = pawn_on
        self.collision = collision

    def __repr__(self):
        return f"{self.deplacement_pattern[0].upper() if self.deplacement_pattern != 'vide' else '-'}{self.pawn_on if self.pawn_on else ''}"

    def get_pawn(self):
        return self.pawn_on

    def place_pawn(self, pawn):
        self.pawn_on = pawn

    def get_deplacement(self):
        return self.deplacement_pattern

    def get_collision(self):
        return self.collision

    def to_dict(self):
        '''Return a transformed version of the current object in a dictionary (JSON handling)'''
        tile_dict = {
            "deplacement_pattern": self.deplacement_pattern,
            "pawn_on": self.pawn_on,
            "collision": self.collision
        }
        return tile_dict

    def from_dict(dict):
        '''Return a Tile object based on the dictionary version given (JSON handling)'''
        return Tile(dict["deplacement_pattern"], dict["pawn_on"], dict["collision"])

class Plateau:
    def __init__(self, taille: int = None, grille=None):
        """
        Initialise un plateau soit en créant une grille vide, soit en utilisant une grille existante de Tile.
        """
        if grille:
            self.taille = len(grille)
            self.grille = grille
        elif taille:
            self.taille = taille
            self.grille = [[Tile() for _ in range(taille)] for _ in range(taille)]
        else:
            raise ValueError("Il faut soit fournir une taille, soit une grille existante.")
        self.first_turn = True
        self.camps = {"B": [False, False], "N": [False, False]}  # Track if camps are occupied
    
    def afficher(self):
        """Affiche le plateau sous forme de liste de listes avec des caractères."""
        tableau = [[str(case) for case in ligne] for ligne in self.grille]
        for ligne in tableau:
            print(ligne)
    
    def placer_pion(self, x: int, y: int, pion: str):
        """Place un pion sur le plateau à la position donnée."""
        if pion not in ('B', 'N'):
            raise ValueError("Le pion doit être 'B' (blanc) ou 'N' (noir)")
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].pion = pion
        else:
            raise IndexError("Coordonnées hors du plateau")
    
    def retirer_pion(self, x: int, y: int):
        """Retire un pion d'une case du plateau."""
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].pion = None
        else:
            raise IndexError("Coordonnées hors du plateau")
    
    def definir_type_case(self, x: int, y: int, nom: str):
        """Définit le type d'une case (ex: reine, roi, tour, cavalier, etc.)."""
        if 0 <= x < self.taille and 0 <= y < self.taille:
            self.grille[x][y].nom = nom
        else:
            raise IndexError("Coordonnées hors du plateau")

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
                return tile.get_possible_moves(x, y, self.grille)
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
        if all(self.camps['B']):
            return 'B'
        elif all(self.camps['N']):
            return 'N'
        return None

# Exemple d'utilisation
import random
import pygame

def creer_grille_personnalisee():
    """Crée une grille personnalisée avec des cases variées et des pions."""
    noms_cases = ["King", "Knight", "Rook", "Bishop", "Queen"]
    grille = [[Tile(random.choice(noms_cases), random.choice([None, 'B', 'N'])) for _ in range(8)] for _ in range(8)]
    return grille

# Création d'un plateau à partir d'une grille personnalisée
grille_perso = creer_grille_personnalisee()

# Create a new board using the Board_creation class
#pygame.init()
#screen = pygame.display.set_mode((1280, 720))
#board_creator = Delete_region(screen)
#board_creator.run()

# Combine regions to create the board
#new_board = board_creator.combine_regions()

# Initialize the Plateau with the new board
plateau = Plateau(grille=grille_perso)
plateau.afficher()
