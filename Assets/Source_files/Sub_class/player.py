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

