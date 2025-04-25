from pawn import *

class Tile:
    def __init__(self, deplacement_pattern, pawn_on=None, collision=None):
        self.deplacement_pattern = deplacement_pattern 
        self.pawn_on = pawn_on
        self.collision = collision

    def __repr__(self):
        """
        Return a string representation of the tile.
        - If the tile has a pawn, show the pawn and the tile type separately.
        - If the tile is empty, show the tile type only.
        """
        pawn = self.pawn_on if self.pawn_on else "-"
        pattern = self.deplacement_pattern if self.deplacement_pattern else "-"
        return f"{pawn}({pattern})"

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
        return {
            "deplacement_pattern": self.deplacement_pattern,
            "pawn_on": self.pawn_on.to_dict() if self.pawn_on else self.pawn_on,
            "collision": self.collision
        }

    def from_dict(data):
        '''Return a Tile object based on the dictionary version given (JSON handling)'''
        return Tile(data["deplacement_pattern"], data["pawn_on"], data["collision"])

    
