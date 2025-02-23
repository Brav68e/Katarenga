class Tile():

    def __init__(self, deplacement_pattern, pawn_on = None, collision = None):
        
        self.deplacement_pattern = deplacement_pattern              # A basic string that contain the "piece", ex: "rook", "king" ...
        self.pawn_on = pawn_on                                      # Pawn object / None
        self.collision = collision                                  # A Rect object (basically a surface)

#######################################

    def get_pawn(self):
        return self.pawn_on
    
#######################################

    def place_pawn(self, pawn):
        self.pawn_on = pawn
    
#######################################

    def get_deplacement(self):
        return self.deplacement_pattern
    
#######################################

    def get_collision(self):
        return self.collision
    
#######################################

    def to_dict(self):
        '''Return a transformed version of the current object in a dictionnary (JSON handling)'''

        tile_dict = {
            "deplacement_pattern": self.deplacement_pattern,
            "pawn_on": self.pawn_on,
            "collision": self.collision 
        }
        
        return tile_dict
    
#######################################

    def from_dict(dict):
        '''Return a Tile object based on the dictionnary version given (JSON handling)'''

        return Tile(dict["deplacement_pattern"], dict["pawn_on"], dict["collision"])