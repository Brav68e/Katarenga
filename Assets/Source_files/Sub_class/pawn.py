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
        