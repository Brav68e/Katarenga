from Source_files.Sub_class.player import *

class Pawn():

    def __init__(self, owner, coordinates):
        
        self.owner = owner                                  #Player object
        self.coordinates = coordinates                      #Tuple with (line, column)

#######################################

    def get_owner(self):
        return self.owner
    
#######################################

    def get_coordinates(self):
        return self.coordinates
    
#######################################

    def set_coordinates(self, coord):
        self.coordinates = coord        
        
#######################################

    def to_dict(self):
        return {
            "owner" : self.owner.to_dict(),
            "coordinates" : self.coordinates
        }

#######################################

    def from_dict(data):
        '''Return a pawn object based on provided data, the input dictionnary may either contain a Player instance or dictionnary format'''

        if isinstance(data["owner"], Player):
            return Pawn(data["owner"], data["coordinates"])
        else:
            return Pawn(Player.from_dict(data["owner"]), data["coordinates"])