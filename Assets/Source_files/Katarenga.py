from Sub_class.tile import *
from Sub_class.pawn import *
from Sub_class.player import *
from Board_creation import Delete_region


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

# Exemple d'utilisation
import random
import pygame

# c'est pour des test
def creer_grille_personnalisee():
    """Crée une grille personnalisée avec des cases variées et des pions."""
    noms_cases = ["reine", "roi", "tour", "cavalier", "fou"]
    grille = [[Tile(random.choice(noms_cases), random.choice([None, 'B', 'N'])) for _ in range(8)] for _ in range(8)]
    return grille

grille_perso = creer_grille_personnalisee()

# Create a new board using the Board_creation class
pygame.init()
screen = pygame.display.set_mode((1280, 720))
board_creator = Delete_region(screen)
board_creator.run()

# Combine regions to create the board
new_board = board_creator.combine_regions()

# Initialize the Plateau with the new board
plateau = Plateau(grille=new_board)
plateau.afficher()
