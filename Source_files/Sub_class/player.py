class Player():

    def __init__(self, username, pawn_amount = 8):

        self.username = username
        self.pawn_amount = pawn_amount

#######################################

    def get_username(self):
        return self.username
    
#######################################

    def pawns_nbr(self):
        return self.pawn_amount
    
#######################################

    def set_pawns(self, nbr):
        self.pawn_amount = nbr

#######################################

    def to_dict(self):
        '''Return a dictionnary version of all attribut of the instance'''

        return {
            "username" : self.username,
            "pawn_amount" : self.pawn_amount
        }
            
#######################################

    def from_dict(data):
        '''Recreate a Player object based on the data provided'''

        return Player(data["username"], data["pawn_amount"])